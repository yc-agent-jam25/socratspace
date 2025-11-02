/**
 * Debate Viewer Component
 * Main component that orchestrates the debate visualization with Council Chamber
 */

import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Chip,
  Stack,
  Tabs,
  Tab,
  Avatar,
  Tooltip
} from '@mui/material';
import type { CompanyData, Agent } from '../lib/types';
import { useSimulation } from '../hooks/useSimulation';
import PhaseIndicator from './PhaseIndicator';
import DecisionPanelEnhanced from './DecisionPanelEnhanced';
import LiveActivityFeed from './debate/LiveActivityFeed';
import BullBearArena from './debate/BullBearArena';
// Notification components for different features
import FreelancerJobNotification from './FreelancerJobNotification';  // External research jobs
import OAuthDialog from './OAuthDialog';  // OAuth authentication flow

// Icons
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import BusinessIcon from '@mui/icons-material/Business';
import PsychologyIcon from '@mui/icons-material/Psychology';
import AssessmentIcon from '@mui/icons-material/Assessment';
import CloudDoneIcon from '@mui/icons-material/CloudDone';
import CloudOffIcon from '@mui/icons-material/CloudOff';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import Alert from '@mui/material/Alert';

interface DebateViewerProps {
  sessionId: string;
  companyData: CompanyData;
  onReset: () => void;
}

// All agents (system messages use a default fallback)
const allAgents: Agent[] = [
  { id: 'system', name: 'System', color: '#6b7280' }, // System messages from orchestrator (only for feed)
  { id: 'market_researcher', name: 'Market Researcher', color: '#3b82f6' },
  { id: 'founder_evaluator', name: 'Founder Evaluator', color: '#10b981' },
  { id: 'product_critic', name: 'Product Critic', color: '#f59e0b' },
  { id: 'financial_analyst', name: 'Financial Analyst', color: '#8b5cf6' },
  { id: 'risk_assessor', name: 'Risk Assessor', color: '#ef4444' },
  { id: 'bull_agent', name: 'Bull Agent', color: '#10b981' },
  { id: 'bear_agent', name: 'Bear Agent', color: '#ef4444' },
  { id: 'lead_partner', name: 'Lead Partner', color: '#3b82f6' }
];

// Agents to display in header (exclude system)
const agents = allAgents.filter(a => a.id !== 'system');

const DebateViewer: React.FC<DebateViewerProps> = ({ sessionId, companyData, onReset }) => {
  // Check if we should use SSE (when backend is ready, set VITE_USE_SSE=true)
  const useSSE = import.meta.env.VITE_USE_SSE === 'true';
  
  const {
    phase,
    messages,
    decision,
    freelancerJob,
    isRunning,
    elapsedTime,
    connectionStatus,
    error,
    oauthRequest,
    startSimulation,
    reconnect,
  } = useSimulation({ sessionId, useSSE });
  const [activeTab, setActiveTab] = useState<'chamber' | 'decision'>('chamber');

  // Freelancer job notification state (for MAYBE decisions with uncertainty)
  const [showFreelancerJob, setShowFreelancerJob] = useState(false);

  // OAuth authentication state (for GitHub/Calendar integrations)
  const [showOAuthDialog, setShowOAuthDialog] = useState(false);
  const [oauthMcpName, setOauthMcpName] = useState<string>('github');

  // Start simulation when component mounts
  useEffect(() => {
    startSimulation();
  }, [startSimulation]);

  // Handle OAuth requests from SSE (e.g., during calendar creation)
  useEffect(() => {
    if (oauthRequest) {
      console.log('[DebateViewer] OAuth request received:', oauthRequest);
      setOauthMcpName(oauthRequest.mcp_name);
      setShowOAuthDialog(true);
    }
  }, [oauthRequest]);

  // Switch to decision tab when decision is ready
  useEffect(() => {
    if (decision) {
      setActiveTab('decision');
    }
  }, [decision]);

  // ==========================================
  // FREELANCER FEATURE: Show job notification for MAYBE decisions
  // ==========================================
  useEffect(() => {
    if (freelancerJob) {
      setShowFreelancerJob(true);
    }
  }, [freelancerJob]);

  // ==========================================
  // OAUTH FEATURE: Handle authentication requests during analysis
  // ==========================================
  useEffect(() => {
    if (oauthRequest) {
      console.log('[DebateViewer] OAuth request received:', oauthRequest);
      setOauthMcpName(oauthRequest.mcp_name);
      setShowOAuthDialog(true);
    }
  }, [oauthRequest]);

  // Check for OAuth errors in messages or error state
  useEffect(() => {
    // Check error message for OAuth requirements
    if (error && (error.includes('OAuth') || error.includes('authentication') || error.includes('GitHub'))) {
      // Check if GitHub is mentioned
      if (error.toLowerCase().includes('github')) {
        setOauthMcpName('github');
        setShowOAuthDialog(true);
      }
    }

    // Also check recent messages for OAuth errors
    const recentMessages = messages.slice(-5);
    for (const msg of recentMessages) {
      if (msg.message && (msg.message.includes('OAuth') || msg.message.includes('authentication required'))) {
        if (msg.message.toLowerCase().includes('github')) {
          setOauthMcpName('github');
          setShowOAuthDialog(true);
          break;
        }
      }
    }
  }, [error, messages]);

  const handleOAuthComplete = (_sessionId: string) => {
    setShowOAuthDialog(false);
    // After OAuth completes, backend will continue calendar creation automatically
  };

  const handleOAuthCancel = () => {
    setShowOAuthDialog(false);
  };

  // Determine which agents are active based on current phase
  const getActiveAgents = (): string[] => {
    if (phase === 'research') {
      return ['market_researcher', 'founder_evaluator', 'product_critic', 'financial_analyst', 'risk_assessor'];
    } else if (phase === 'debate') {
      return ['bull_agent', 'bear_agent'];
    } else if (phase === 'decision') {
      return ['lead_partner'];
    }
    return [];
  };

  const formatElapsedTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getPhaseLabel = (): string => {
    switch (phase) {
      case 'research': return 'Research Phase';
      case 'debate': return 'Debate Phase';
      case 'decision': return 'Decision Phase';
      default: return 'Initializing';
    }
  };

  return (
    <Box
      sx={{
        animation: 'fadeInUp 0.6s ease-out',
      }}
    >
              {/* Compact Header with Integrated Council Chamber */}
              <Paper 
                elevation={3}
                sx={{ 
                  p: 2, 
                  mb: 2,
                  background: 'rgba(255, 255, 255, 0.05)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  overflow: 'visible', // Allow status indicators to show outside paper
                }}
              >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: { xs: 'wrap', md: 'nowrap' } }}>
          {/* Left: Company Info & Status */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flex: '0 0 auto', flexWrap: 'wrap' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <BusinessIcon sx={{ color: 'primary.main', fontSize: '1.25rem' }} />
              <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: '-0.02em', fontSize: { xs: '1rem', sm: '1.25rem' } }}>
                {companyData.company_name}
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ display: { xs: 'none', sm: 'block' }, fontSize: '0.8rem' }}>
              {companyData.industry} • {companyData.website}
            </Typography>
            <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap>
              <Chip
                label={getPhaseLabel()}
                color="primary"
                size="small"
                sx={{ fontWeight: 600, fontSize: '0.7rem', height: 24 }}
              />
              <Chip
                icon={<AccessTimeIcon sx={{ fontSize: '0.9rem !important' }} />}
                label={formatElapsedTime(elapsedTime)}
                variant="outlined"
                size="small"
                sx={{ fontSize: '0.7rem', height: 24 }}
              />
              {connectionStatus && (
                <Chip
                  icon={
                    connectionStatus === 'connected' ? (
                      <CloudDoneIcon sx={{ fontSize: '0.9rem !important' }} />
                    ) : connectionStatus === 'error' ? (
                      <ErrorOutlineIcon sx={{ fontSize: '0.9rem !important' }} />
                    ) : (
                      <CloudOffIcon sx={{ fontSize: '0.9rem !important' }} />
                    )
                  }
                  label={
                    connectionStatus === 'connected'
                      ? 'Connected'
                      : connectionStatus === 'connecting'
                      ? 'Connecting...'
                      : connectionStatus === 'error'
                      ? 'Error'
                      : 'Disconnected'
                  }
                  color={
                    connectionStatus === 'connected'
                      ? 'success'
                      : connectionStatus === 'error'
                      ? 'error'
                      : 'default'
                  }
                  size="small"
                  variant={connectionStatus === 'connected' ? 'filled' : 'outlined'}
                  onClick={connectionStatus === 'error' && reconnect ? reconnect : undefined}
                  sx={{
                    cursor: connectionStatus === 'error' && reconnect ? 'pointer' : 'default',
                    fontSize: '0.7rem',
                    height: 24,
                  }}
                />
              )}
            </Stack>
          </Box>

          {/* Middle: Council Chamber Avatars (Single Row) */}
          <Box sx={{ 
            flex: 1, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: { xs: 'flex-start', md: 'center' },
            gap: 1, 
            minWidth: 0,
            overflowX: 'auto',
            overflowY: 'visible', // Allow status indicators to show
            scrollbarWidth: 'none',
            '&::-webkit-scrollbar': { display: 'none' },
            py: 0.5, // Add vertical padding to prevent clipping
          }}>
            <Chip
              label="🏛️ Council"
              size="small"
              sx={{
                background: 'rgba(139, 92, 246, 0.2)',
                color: '#a78bfa',
                fontWeight: 600,
                fontSize: '0.7rem',
                height: 24,
                flexShrink: 0,
              }}
            />
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 0.75,
                overflowX: 'auto',
                overflowY: 'visible', // Allow status indicators to show
                scrollbarWidth: 'none',
                '&::-webkit-scrollbar': { display: 'none' },
                flex: 1,
                justifyContent: { xs: 'flex-start', md: 'center' },
                py: 1, // Add padding to prevent clipping
              }}
            >
              {agents.map((agent) => {
                const status = (() => {
                  const hasMessages = messages.some(m => m.agent === agent.id);
                  const isActive = getActiveAgents().includes(agent.id);
                  if (hasMessages && !isActive) return 'complete';
                  if (isActive) return 'active';
                  return 'pending';
                })();
                const messageCount = messages.filter(m => m.agent === agent.id).length;
                const isActive = status === 'active';
                const isComplete = status === 'complete';

                return (
                  <Tooltip
                    key={agent.id}
                    title={
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 700 }}>
                          {agent.name}
                        </Typography>
                        <Typography variant="caption" sx={{ display: 'block', mt: 0.5 }}>
                          {isActive && '🟢 Currently analyzing'}
                          {isComplete && `✅ Complete (${messageCount} insights)`}
                          {status === 'pending' && '⏳ Waiting'}
                        </Typography>
                      </Box>
                    }
                    arrow
                  >
                    <Box sx={{ 
                      position: 'relative', 
                      flexShrink: 0,
                      overflow: 'visible', // Ensure status indicator isn't clipped
                      pb: 1, // Add padding bottom to give space for status indicator
                    }}>
                      <Avatar
                        sx={{
                          width: 36,
                          height: 36,
                          bgcolor: agent.color,
                          fontWeight: 700,
                          fontSize: '0.75rem',
                          opacity: status === 'pending' ? 0.4 : 1,
                          border: isActive ? `2px solid ${agent.color}` : `1px solid ${agent.color}40`,
                          transition: 'all 0.3s ease',
                          cursor: 'pointer',
                          boxShadow: isActive ? `0 0 12px ${agent.color}60` : 'none',
                          '&:hover': {
                            transform: 'scale(1.15)',
                            boxShadow: `0 0 15px ${agent.color}80`,
                          },
                        }}
                      >
                        {agent.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
                      </Avatar>
                      {/* Status indicator */}
                      <Box
                        sx={{
                          position: 'absolute',
                          bottom: -4, // Position slightly outside for badge effect
                          right: -4,
                          width: 14, // Slightly larger to be more visible
                          height: 14,
                          borderRadius: '50%',
                          background: isActive ? '#10b981' : isComplete ? '#3b82f6' : '#6b7280',
                          border: '2px solid #141420',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '0.6rem',
                          zIndex: 10, // Ensure it's above other elements
                        }}
                      >
                        {isActive && '●'}
                        {isComplete && '✓'}
                        {status === 'pending' && '○'}
                      </Box>
                      {/* Message count badge */}
                      {messageCount > 0 && (
                        <Box
                          sx={{
                            position: 'absolute',
                            top: -6,
                            right: -6,
                            minWidth: 16,
                            height: 16,
                            borderRadius: '8px',
                            background: agent.color,
                            color: 'white',
                            fontSize: '0.6rem',
                            fontWeight: 700,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            px: 0.5,
                            boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
                          }}
                        >
                          {messageCount}
                        </Box>
                      )}
                    </Box>
                  </Tooltip>
                );
              })}
            </Box>
          </Box>

          {/* Right: New Analysis Button */}
          <Box sx={{ flex: '0 0 auto' }}>
            <Button 
              variant="outlined" 
              onClick={onReset}
              disabled={isRunning}
              size="small"
              sx={{ 
                fontWeight: 600,
                minWidth: 120,
              }}
            >
              New Analysis
            </Button>
          </Box>
        </Box>
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert
          severity="error"
          action={
            reconnect && (
              <Button color="inherit" size="small" onClick={reconnect}>
                Reconnect
              </Button>
            )
          }
          sx={{ mb: 2 }}
        >
          {error}
        </Alert>
      )}

      {/* Phase Indicator */}
      <PhaseIndicator currentPhase={phase} />

      {/* Progress Bar */}
      {isRunning && !decision && (
        <LinearProgress 
          sx={{ 
            mb: 2,
            height: 4,
            borderRadius: 2,
          }} 
        />
      )}

      {/* Tabs Navigation (shown when decision is available) */}
      {decision && (
        <Box sx={{ mb: 2 }}>
          <Tabs
            value={activeTab}
            onChange={(_, newValue) => setActiveTab(newValue)}
            sx={{
              '& .MuiTabs-indicator': {
                background: 'linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%)',
                height: 3,
              },
            }}
          >
            <Tab
              value="chamber"
              icon={<PsychologyIcon />}
              iconPosition="start"
              label="Agent Reasoning"
              sx={{
                fontWeight: 600,
                textTransform: 'none',
                fontSize: '1rem',
              }}
            />
            <Tab
              value="decision"
              icon={<AssessmentIcon />}
              iconPosition="start"
              label="Final Decision"
              sx={{
                fontWeight: 600,
                textTransform: 'none',
                fontSize: '1rem',
              }}
            />
          </Tabs>
        </Box>
      )}

      {/* Main Content - Full Screen Live Activity Feed */}
      {activeTab === 'chamber' && (
        <Box>
          {/* Show Bull vs Bear Arena during debate phase (compact, above feed) */}
          {phase === 'debate' && (
            <Box sx={{ mb: 2 }}>
              <BullBearArena
                agents={allAgents.filter(a => a.id !== 'system')}
                messages={messages}
                activeAgents={getActiveAgents()}
              />
            </Box>
          )}

          {/* Full Screen Live Activity Feed */}
          <Box
            sx={{
              background: 'rgba(255, 255, 255, 0.02)',
              backdropFilter: 'blur(20px)',
              WebkitBackdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              borderRadius: 3,
              height: { xs: 'calc(100vh - 320px)', sm: 'calc(100vh - 280px)', md: 'calc(100vh - 260px)' },
              minHeight: 600,
              overflow: 'hidden',
              position: 'relative',
            }}
          >
            <LiveActivityFeed
              messages={messages}
              agents={allAgents}
              activeAgents={decision ? [] : getActiveAgents()}
            />
          </Box>
        </Box>
      )}

      {/* Decision Panel */}
      {activeTab === 'decision' && decision && (
        <DecisionPanelEnhanced decision={decision} companyData={companyData} />
      )}

      {/* Initialization State */}
      {!isRunning && !decision && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 1 }}>
            Initializing Council Chamber...
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Preparing agents for analysis
          </Typography>
        </Box>
      )}

      {/* ==========================================
          FREELANCER JOB NOTIFICATION
          Shown when MAYBE decision requires external research
          ========================================== */}
      {showFreelancerJob && freelancerJob && (
        <FreelancerJobNotification
          content={freelancerJob.content}
          company={freelancerJob.company}
          onClose={() => setShowFreelancerJob(false)}
        />
      )}

      {/* ==========================================
          OAUTH AUTHENTICATION DIALOG
          Shown when GitHub/Calendar access is needed
          ========================================== */}
      <OAuthDialog
        open={showOAuthDialog}
        mcpName={oauthMcpName}
        mcpDisplayName={oauthMcpName === 'github' ? 'GitHub' : oauthMcpName === 'gcalendar' ? 'Google Calendar' : 'Service'}
        onComplete={handleOAuthComplete}
        onCancel={handleOAuthCancel}
        initialSessionId={oauthRequest?.oauth_session_id || null}
        initialAuthUrl={oauthRequest?.auth_url || null}
      />
    </Box>
  );
};

export default DebateViewer;
