/**
 * Decision Panel Component
 * Displays final investment decision and memo
 */

import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Decision } from '../lib/types';
import EventIcon from '@mui/icons-material/Event';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import CancelIcon from '@mui/icons-material/Cancel';

interface DecisionPanelProps {
  decision: Decision;
}

const DecisionPanel: React.FC<DecisionPanelProps> = ({ decision }) => {
  const getDecisionColor = () => {
    switch (decision.decision) {
      case 'INVEST':
        return 'success';
      case 'MAYBE':
        return 'warning';
      case 'PASS':
        return 'error';
      default:
        return 'default';
    }
  };

  const getDecisionIcon = () => {
    switch (decision.decision) {
      case 'INVEST':
        return <CheckCircleIcon />;
      case 'MAYBE':
        return <WarningIcon />;
      case 'PASS':
        return <CancelIcon />;
      default:
        return <CheckCircleIcon />; // Default icon
    }
  };

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: 4,
        animation: 'fadeIn 0.5s ease-in',
        '@keyframes fadeIn': {
          from: { opacity: 0, transform: 'translateY(20px)' },
          to: { opacity: 1, transform: 'translateY(0)' }
        }
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          Final Decision
        </Typography>
        <Chip
          icon={getDecisionIcon()}
          label={decision.decision}
          color={getDecisionColor()}
          size="medium"
          sx={{ 
            fontWeight: 700,
            fontSize: '1.1rem',
            px: 2,
            py: 3
          }}
        />
      </Box>

      <Divider sx={{ mb: 3 }} />

      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Reasoning
      </Typography>
      <Typography variant="body1" paragraph sx={{ lineHeight: 1.8, color: 'text.secondary' }}>
        {decision.reasoning}
      </Typography>

      <Divider sx={{ my: 3 }} />

      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
        Investment Memo
      </Typography>
      <Box 
        sx={{ 
          '& h1': { fontSize: '1.75rem', fontWeight: 600, mt: 3, mb: 2 },
          '& h2': { fontSize: '1.5rem', fontWeight: 600, mt: 3, mb: 2 },
          '& h3': { fontSize: '1.25rem', fontWeight: 600, mt: 2, mb: 1 },
          '& p': { lineHeight: 1.8, mb: 2 },
          '& ul': { pl: 3, mb: 2 },
          '& li': { mb: 1 },
          '& strong': { fontWeight: 600 },
          '& code': {
            backgroundColor: 'grey.100',
            padding: '2px 6px',
            borderRadius: 1,
            fontSize: '0.875rem'
          },
          '& table': {
            borderCollapse: 'collapse',
            width: '100%',
            margin: '1rem 0',
            fontSize: '0.875rem',
          },
          '& th, & td': {
            border: '1px solid',
            borderColor: 'divider',
            padding: '0.75rem',
            textAlign: 'left',
          },
          '& th': {
            backgroundColor: 'action.hover',
            fontWeight: 600,
          },
          '& tr:hover': {
            backgroundColor: 'action.hover',
          }
        }}
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{decision.investment_memo}</ReactMarkdown>
      </Box>

      {decision.calendar_events.length > 0 && (
        <>
          <Divider sx={{ my: 3 }} />
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            Calendar Events Created
          </Typography>
          <List sx={{ bgcolor: 'background.paper' }}>
            {decision.calendar_events.map((event, idx) => (
              <ListItem 
                key={idx}
                sx={{
                  border: 1,
                  borderColor: 'divider',
                  borderRadius: 1,
                  mb: 1,
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <ListItemIcon>
                  <EventIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {event.title}
                    </Typography>
                  }
                  secondary={
                    <>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(event.start_time).toLocaleString('en-US', {
                          weekday: 'long',
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Attendees: {event.attendees.join(', ')}
                      </Typography>
                      {event.description && (
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                          {event.description}
                        </Typography>
                      )}
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        </>
      )}
    </Paper>
  );
};

export default DecisionPanel;
