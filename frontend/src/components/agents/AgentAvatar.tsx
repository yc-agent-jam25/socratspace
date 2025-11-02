/**
 * AgentAvatar Component
 * Circular avatar with gradient border and status indicators
 */

import React from 'react';
import { Box, Avatar, Typography, Tooltip } from '@mui/material';
import { keyframes } from '@mui/system';

// Status icons
import CircleIcon from '@mui/icons-material/Circle';

interface AgentAvatarProps {
  name: string;
  color: string;
  status: 'idle' | 'thinking' | 'speaking' | 'done';
  size?: 'small' | 'medium' | 'large';
  showLabel?: boolean;
  onClick?: () => void;
}

// Pulse animation for active agents
const pulseAnimation = keyframes`
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
`;

// Rotate animation for gradient border
const rotateGradient = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;

const AgentAvatar: React.FC<AgentAvatarProps> = ({
  name,
  color,
  status,
  size = 'medium',
  showLabel = true,
  onClick,
}) => {
  // Get initials from name
  const getInitials = (name: string): string => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  // Size mapping
  const sizeMap = {
    small: { avatar: 48, container: 56, fontSize: '0.875rem' },
    medium: { avatar: 72, container: 84, fontSize: '1rem' },
    large: { avatar: 96, container: 112, fontSize: '1.25rem' },
  };

  const dimensions = sizeMap[size];
  const isActive = status === 'thinking' || status === 'speaking';

  // Status indicator
  const getStatusIcon = () => {
    const iconSize = size === 'small' ? 8 : size === 'medium' ? 10 : 12;
    
    switch (status) {
      case 'thinking':
        return <CircleIcon sx={{ fontSize: iconSize, color: '#f59e0b', animation: `${pulseAnimation} 1.5s infinite` }} />;
      case 'speaking':
        return <CircleIcon sx={{ fontSize: iconSize, color: '#10b981', animation: `${pulseAnimation} 1s infinite` }} />;
      case 'done':
        return <CircleIcon sx={{ fontSize: iconSize, color: '#3b82f6' }} />;
      default:
        return <CircleIcon sx={{ fontSize: iconSize, color: 'rgba(255,255,255,0.3)' }} />;
    }
  };

  return (
    <Tooltip title={`${name} - ${status}`} arrow>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 1,
          cursor: onClick ? 'pointer' : 'default',
          userSelect: 'none',
        }}
        onClick={onClick}
      >
        {/* Avatar container with gradient border */}
        <Box
          sx={{
            position: 'relative',
            width: dimensions.container,
            height: dimensions.container,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {/* Animated gradient border */}
          {isActive && (
            <Box
              sx={{
                position: 'absolute',
                inset: 0,
                borderRadius: '50%',
                padding: '3px',
                background: `linear-gradient(135deg, ${color}, ${color}99, ${color}66)`,
                animation: `${rotateGradient} 3s linear infinite`,
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  inset: '3px',
                  borderRadius: '50%',
                  background: '#141420',
                },
              }}
            />
          )}

          {/* Static border for inactive agents */}
          {!isActive && (
            <Box
              sx={{
                position: 'absolute',
                inset: 0,
                borderRadius: '50%',
                border: `2px solid ${color}40`,
              }}
            />
          )}

          {/* Avatar */}
          <Avatar
            sx={{
              width: dimensions.avatar,
              height: dimensions.avatar,
              bgcolor: color,
              fontSize: dimensions.fontSize,
              fontWeight: 600,
              zIndex: 1,
              boxShadow: isActive ? `0 0 30px ${color}60` : 'none',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: onClick ? 'scale(1.05)' : 'none',
              },
            }}
          >
            {getInitials(name)}
          </Avatar>

          {/* Status indicator */}
          <Box
            sx={{
              position: 'absolute',
              bottom: 4,
              right: 4,
              zIndex: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: size === 'small' ? 16 : size === 'medium' ? 20 : 24,
              height: size === 'small' ? 16 : size === 'medium' ? 20 : 24,
              borderRadius: '50%',
              bgcolor: 'rgba(20, 20, 32, 0.9)',
              border: '2px solid rgba(255, 255, 255, 0.1)',
            }}
          >
            {getStatusIcon()}
          </Box>
        </Box>

        {/* Label */}
        {showLabel && (
          <Typography
            variant="caption"
            sx={{
              textAlign: 'center',
              color: isActive ? 'text.primary' : 'text.secondary',
              fontWeight: isActive ? 600 : 400,
              maxWidth: 100,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              transition: 'all 0.3s ease',
            }}
          >
            {name}
          </Typography>
        )}
      </Box>
    </Tooltip>
  );
};

export default AgentAvatar;

