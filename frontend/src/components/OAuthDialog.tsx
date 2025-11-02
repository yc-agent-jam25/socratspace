/**
 * OAuth Dialog Component
 * Handles OAuth authentication via popup window for GitHub, Google Calendar, etc.
 */

import React, { useEffect, useState, useRef } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

interface OAuthDialogProps {
  open: boolean;
  mcpName: string;
  mcpDisplayName: string;
  onComplete: (oauthSessionId: string) => void;
  onCancel: () => void;
  initialSessionId?: string | null; // Optional: use existing session from SSE
  initialAuthUrl?: string | null; // Optional: use existing auth URL from SSE
}

const OAuthDialog: React.FC<OAuthDialogProps> = ({
  open,
  mcpName,
  mcpDisplayName,
  onComplete,
  onCancel,
  initialSessionId,
  initialAuthUrl,
}) => {
  const [oauthSessionId, setOauthSessionId] = useState<string | null>(initialSessionId || null);
  const [authUrl, setAuthUrl] = useState<string | null>(initialAuthUrl || null);
  const [status, setStatus] = useState<'idle' | 'initiating' | 'pending' | 'checking' | 'completed' | 'failed'>('idle');
  const [error, setError] = useState<string | null>(null);
  const popupWindowRef = useRef<Window | null>(null);
  const pollIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  // Update state when initial values change
  useEffect(() => {
    if (initialSessionId) {
      setOauthSessionId(initialSessionId);
    }
    if (initialAuthUrl) {
      setAuthUrl(initialAuthUrl);
    }
  }, [initialSessionId, initialAuthUrl]);

  // Initiate OAuth when dialog opens (if not already provided)
  useEffect(() => {
    if (open && status === 'idle') {
      if (initialSessionId && initialAuthUrl) {
        // Use existing session from SSE
        setStatus('pending');
        openPopup(initialAuthUrl);
        startPolling(initialSessionId);
      } else {
        // Create new session
        initiateOAuth();
      }
    }

    // Cleanup on unmount or close
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
      if (popupWindowRef.current && !popupWindowRef.current.closed) {
        popupWindowRef.current.close();
      }
    };
  }, [open]);

  // Cleanup on dialog close
  useEffect(() => {
    if (!open) {
      // Reset state
      setStatus('idle');
      setOauthSessionId(null);
      setAuthUrl(null);
      setError(null);
      
      // Close popup if open
      if (popupWindowRef.current && !popupWindowRef.current.closed) {
        popupWindowRef.current.close();
      }
      
      // Clear polling
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    }
  }, [open]);

  const initiateOAuth = async () => {
    try {
      setStatus('initiating');
      setError(null);

      const response = await fetch(`${API_URL}/api/oauth/initiate/${mcpName}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to initiate OAuth' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setOauthSessionId(data.oauth_session_id);
      setAuthUrl(data.auth_url || null);
      
      // Check if OAuth is already completed (e.g., existing session)
      if (data.status === 'completed') {
        setStatus('completed');
        // Immediately call completion callback
        setTimeout(() => {
          onComplete(data.oauth_session_id);
        }, 500);
        return;
      }
      
      // OAuth is pending - need user action
      setStatus('pending');
      
      // Open popup window only if we have an auth URL
      if (data.auth_url) {
        openPopup(data.auth_url);
        // Start polling for completion
        startPolling(data.oauth_session_id);
      } else {
        setError('No authentication URL provided');
        setStatus('failed');
      }
    } catch (err: any) {
      console.error('OAuth initiation error:', err);
      setError(err.message || 'Failed to initiate OAuth authentication');
      setStatus('failed');
    }
  };

  const openPopup = (url: string) => {
    // Calculate centered position
    const width = 600;
    const height = 700;
    const left = (window.screen.width - width) / 2;
    const top = (window.screen.height - height) / 2;

    popupWindowRef.current = window.open(
      url,
      'oauth',
      `width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes`
    );

    if (!popupWindowRef.current) {
      setError('Popup blocked. Please allow popups for this site and try again.');
      setStatus('failed');
    }
  };

  const startPolling = (sessionId: string) => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }

    pollIntervalRef.current = setInterval(async () => {
      try {
        setStatus('checking');

        const response = await fetch(
          `${API_URL}/api/oauth/status/${sessionId}?mcp_name=${mcpName}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

        if (!response.ok) {
          // Continue polling on error (might be transient)
          setStatus('pending');
          return;
        }

        const data = await response.json();

        if (data.status === 'completed') {
          // Success!
          setStatus('completed');
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
          if (popupWindowRef.current && !popupWindowRef.current.closed) {
            popupWindowRef.current.close();
          }

          // Ensure session is cached by calling status one more time
          // This helps ensure backend has the session cached when calendar creation runs
          await fetch(
            `${API_URL}/api/oauth/status/${sessionId}?mcp_name=${mcpName}`,
            { method: 'GET' }
          ).catch(() => {}); // Ignore errors - just ensure cache is set

          // Call completion callback
          setTimeout(() => {
            onComplete(sessionId);
          }, 1000); // Small delay to show success state
        } else if (data.status === 'failed') {
          setError(data.message || 'OAuth authentication failed');
          setStatus('failed');
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }
        } else {
          // Still pending, continue polling
          setStatus('pending');
        }
      } catch (err: any) {
        console.error('OAuth status check error:', err);
        // Continue polling on error (might be transient)
        setStatus('pending');
      }
    }, 2000); // Poll every 2 seconds
  };

  const handleOpenUrl = () => {
    if (authUrl) {
      window.open(authUrl, '_blank');
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onCancel}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: {
          background: 'rgba(20, 20, 32, 0.95)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
      }}
    >
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <LockIcon sx={{ color: 'primary.main' }} />
        <Typography variant="h6" sx={{ fontWeight: 700 }}>
          Authenticate with {mcpDisplayName}
        </Typography>
      </DialogTitle>

      <DialogContent>
        {status === 'idle' || status === 'initiating' ? (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 3 }}>
            <CircularProgress sx={{ mb: 2 }} />
            <Typography variant="body2" color="text.secondary">
              Preparing authentication...
            </Typography>
          </Box>
        ) : status === 'pending' || status === 'checking' ? (
          <Box>
            <Alert severity="info" sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ mb: 1 }}>
                A popup window should have opened. If not, click the button below.
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Please complete the authentication in the popup window.
              </Typography>
            </Alert>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
              {authUrl && (
                <Button
                  variant="outlined"
                  startIcon={<OpenInNewIcon />}
                  onClick={handleOpenUrl}
                  fullWidth
                >
                  Open Authentication Page
                </Button>
              )}

              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, justifyContent: 'center', mt: 1 }}>
                <CircularProgress size={16} />
                <Typography variant="caption" color="text.secondary">
                  Waiting for authentication...
                </Typography>
              </Box>
            </Box>
          </Box>
        ) : status === 'completed' ? (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 2 }}>
            <CheckCircleIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 1 }}>
              Authentication Successful!
            </Typography>
            <Typography variant="body2" color="text.secondary">
              You can now use {mcpDisplayName} features.
            </Typography>
          </Box>
        ) : status === 'failed' ? (
          <Box>
            <Alert severity="error" sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ fontWeight: 700, mb: 0.5 }}>
                Authentication Failed
              </Typography>
              <Typography variant="caption">
                {error || 'An error occurred during authentication.'}
              </Typography>
            </Alert>

            {authUrl && (
              <Button
                variant="outlined"
                startIcon={<OpenInNewIcon />}
                onClick={handleOpenUrl}
                fullWidth
                sx={{ mt: 2 }}
              >
                Try Again
              </Button>
            )}
          </Box>
        ) : null}
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 2 }}>
        {status === 'completed' ? (
          <Button onClick={() => onComplete(oauthSessionId || '')} variant="contained" fullWidth>
            Continue
          </Button>
        ) : status === 'failed' ? (
          <>
            <Button onClick={onCancel} variant="outlined">
              Cancel
            </Button>
            <Button onClick={initiateOAuth} variant="contained">
              Retry
            </Button>
          </>
        ) : (
          <Button onClick={onCancel} variant="outlined" disabled={status === 'pending' || status === 'checking'}>
            Cancel
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default OAuthDialog;

