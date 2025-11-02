/**
 * Logo Component
 * Displays the Socrat Space logo
 */

import React from 'react';
import { Box } from '@mui/material';
import logoSrc from '../../assets/socrat.space.png';

interface LogoProps {
  size?: number;
  sx?: object;
}

const Logo: React.FC<LogoProps> = ({ size = 120, sx = {} }) => {
  return (
    <Box
      component="img"
      src={logoSrc}
      alt="Socrat Space Logo"
      sx={{
        width: size,
        height: size,
        objectFit: 'contain',
        filter: 'drop-shadow(0 4px 12px rgba(139, 92, 246, 0.3))',
        ...sx,
      }}
    />
  );
};

export default Logo;
