/**
 * Agent Message List Component
 * Dialog showing full message history for a selected agent
 */

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemText,
  Typography,
  IconButton,
  Box
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import type { Agent, AgentMessage } from '../lib/types';

interface AgentMessageListProps {
  agent: Agent | null;
  messages: AgentMessage[];
  open: boolean;
  onClose: () => void;
}

const AgentMessageList: React.FC<AgentMessageListProps> = ({ agent, messages, open, onClose }) => {
  if (!agent) return null;

  const formatTimestamp = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderLeft: `4px solid ${agent.color}`
        }
      }}
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        borderBottom: 1,
        borderColor: 'divider'
      }}>
        <Box>
          <Typography variant="h6" sx={{ color: agent.color, fontWeight: 600 }}>
            {agent.name}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {messages.length} message{messages.length !== 1 ? 's' : ''}
          </Typography>
        </Box>
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers sx={{ p: 0 }}>
        {messages.length > 0 ? (
          <List sx={{ p: 0 }}>
            {messages.map((message, index) => (
              <ListItem 
                key={index}
                sx={{
                  borderBottom: index < messages.length - 1 ? 1 : 0,
                  borderColor: 'divider',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  py: 2,
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                <Typography 
                  variant="caption" 
                  color="text.secondary"
                  sx={{ mb: 1, fontWeight: 500 }}
                >
                  {formatTimestamp(message.timestamp)}
                </Typography>
                <ListItemText
                  primary={message.message}
                  primaryTypographyProps={{
                    variant: 'body2',
                    sx: { whiteSpace: 'pre-wrap', lineHeight: 1.6 }
                  }}
                />
              </ListItem>
            ))}
          </List>
        ) : (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              No messages yet
            </Typography>
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} variant="contained">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AgentMessageList;

