import { useState } from 'react';
import {
  Snackbar,
  Paper,
  Typography,
  IconButton,
  Button,
  Box,
} from '@mui/material';
import {
  Close as CloseIcon,
  ContentCopy as CopyIcon,
  CheckCircle as CheckIcon,
  Work as WorkIcon
} from '@mui/icons-material';

interface FreelancerJobNotificationProps {
  content: string;
  company: string;
  onClose: () => void;
}

export function FreelancerJobNotification({
  content,
  company,
  onClose
}: FreelancerJobNotificationProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Snackbar
      open={true}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      sx={{ mt: 8, maxWidth: '450px' }}
    >
      <Paper
        elevation={8}
        sx={{
          p: 2.5,
          background: 'linear-gradient(135deg, #29B2FE 0%, #1a8cd8 100%)',
          color: 'white',
          borderRadius: 2,
          maxWidth: '450px',
          position: 'relative'
        }}
      >
        {/* Close button */}
        <IconButton
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: 'white'
          }}
          size="small"
        >
          <CloseIcon fontSize="small" />
        </IconButton>

        {/* Header */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 2, pr: 3 }}>
          <WorkIcon sx={{ fontSize: 32 }} />
          <Box>
            <Typography variant="h6" fontWeight="bold" sx={{ lineHeight: 1.2 }}>
              Freelancer Job Post Ready
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.9 }}>
              Market Research for {company}
            </Typography>
          </Box>
        </Box>

        {/* Content preview */}
        <Box
          sx={{
            bgcolor: 'rgba(255,255,255,0.15)',
            p: 2,
            borderRadius: 1,
            mb: 2,
            maxHeight: '200px',
            overflowY: 'auto',
            fontSize: '0.875rem',
            lineHeight: 1.6,
            fontFamily: 'monospace',
            whiteSpace: 'pre-wrap',
            border: '1px solid rgba(255,255,255,0.2)'
          }}
        >
          <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
            {content}
          </Typography>
        </Box>

        {/* Copy button */}
        <Button
          fullWidth
          variant="contained"
          onClick={handleCopy}
          startIcon={copied ? <CheckIcon /> : <CopyIcon />}
          sx={{
            bgcolor: 'white',
            color: '#29B2FE',
            fontWeight: 'bold',
            '&:hover': {
              bgcolor: 'rgba(255,255,255,0.9)'
            }
          }}
        >
          {copied ? 'Copied!' : 'Copy to Clipboard'}
        </Button>

        {/* Instructions */}
        <Typography
          variant="caption"
          sx={{
            display: 'block',
            mt: 1.5,
            opacity: 0.85,
            textAlign: 'center'
          }}
        >
          Paste directly into Freelancer.com job posting
        </Typography>
      </Paper>
    </Snackbar>
  );
}

export default FreelancerJobNotification;
