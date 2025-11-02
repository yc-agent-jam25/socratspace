/**
 * Enhanced Company Input Form Component
 * Engaging, visual, interactive form experience
 */

import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Stack,
  Alert,
  CircularProgress,
  LinearProgress,
  Grid,
} from '@mui/material';
import type { CompanyData } from '../lib/types';
import { api } from '../lib/api';

// Icons
import BusinessIcon from '@mui/icons-material/Business';
import PublicIcon from '@mui/icons-material/Public';
import CategoryIcon from '@mui/icons-material/Category';
import DescriptionIcon from '@mui/icons-material/Description';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

interface InputFormEnhancedProps {
  onAnalysisStart: (sessionId: string, companyData: CompanyData) => void;
}

const InputFormEnhanced: React.FC<InputFormEnhancedProps> = ({ onAnalysisStart }) => {
  const [formData, setFormData] = useState<CompanyData>({
    company_name: '',
    website: '',
    founder_github: '',
    industry: '',
    product_description: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Calculate form completion
  const requiredFields = ['company_name', 'website', 'industry', 'product_description'];
  const completedFields = requiredFields.filter(field => {
    const value = formData[field as keyof CompanyData];
    return typeof value === 'string' && value.trim().length > 0;
  }).length;
  const progress = (completedFields / requiredFields.length) * 100;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.company_name || !formData.website || !formData.industry || !formData.product_description) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await api.startAnalysis(formData);
      const sessionId = response.session_id;
      onAnalysisStart(sessionId, formData);
    } catch (err) {
      setError('Failed to start analysis. Please try again.');
      setLoading(false);
    }
  };

  const handleFieldChange = (
    field: keyof CompanyData,
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }));
    setError(null);
  };

  return (
    <Box
      sx={{
        maxWidth: 1200,
        mx: 'auto',
        animation: 'fadeInUp 0.6s ease-out',
      }}
    >
      {/* Compact Header */}
      <Box sx={{ textAlign: 'center', mb: 3 }}>
        <Typography
          variant="h4"
          sx={{
            fontWeight: 800,
            mb: 1,
            background: 'linear-gradient(135deg, #ffffff 0%, #a78bfa 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '-0.02em',
          }}
        >
          Tell Us About Your Startup
        </Typography>
        
        {/* Progress bar - inline with header */}
        <Box sx={{ maxWidth: 500, mx: 'auto', mb: 2 }}>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{
              height: 6,
              borderRadius: 3,
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              '& .MuiLinearProgress-bar': {
                background: 'linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%)',
                borderRadius: 3,
              },
            }}
          />
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 0.5 }}>
            <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.7rem' }}>
              {completedFields} of {requiredFields.length} complete
            </Typography>
            <Typography variant="caption" sx={{ color: '#8b5cf6', fontWeight: 700, fontSize: '0.7rem' }}>
              {Math.round(progress)}%
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Form - 2 Column Layout */}
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          p: 3,
          background: 'rgba(255, 255, 255, 0.04)',
          backdropFilter: 'blur(24px)',
          WebkitBackdropFilter: 'blur(24px)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: 3,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
        }}
      >
        <Grid container spacing={2}>
          {/* Row 1: Company Name & Website */}
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                position: 'relative',
                '&::after': formData.company_name ? {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  right: 0,
                  width: 3,
                  height: '100%',
                  background: '#10b981',
                  borderRadius: '0 8px 8px 0',
                } : {},
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <BusinessIcon sx={{ fontSize: 20, color: formData.company_name ? '#8b5cf6' : 'rgba(255, 255, 255, 0.4)' }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>
                  Company Name *
                </Typography>
              </Box>
              <TextField
                fullWidth
                value={formData.company_name}
                onChange={(e) => handleFieldChange('company_name', e)}
                placeholder="e.g., Stripe, Notion, Figma"
                variant="outlined"
                size="small"
                inputProps={{
                  style: { 
                    color: 'rgba(255, 255, 255, 0.9) !important',
                    WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                  },
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: 'rgba(0, 0, 0, 0.2)',
                    color: 'rgba(255, 255, 255, 0.9) !important',
                    '& .MuiInputBase-input': {
                      color: 'rgba(255, 255, 255, 0.9) !important',
                      WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                    },
                    '& input': {
                      color: 'rgba(255, 255, 255, 0.9) !important',
                      WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                    },
                    '& fieldset': {
                      borderColor: formData.company_name ? 'rgba(139, 92, 246, 0.3)' : 'rgba(255, 255, 255, 0.1)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(139, 92, 246, 0.4)',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#8b5cf6',
                    },
                  },
                  '& .MuiInputBase-input::placeholder': {
                    color: 'rgba(255, 255, 255, 0.5) !important',
                    opacity: 1,
                    WebkitTextFillColor: 'rgba(255, 255, 255, 0.5) !important',
                  },
                }}
              />
            </Box>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                position: 'relative',
                '&::after': formData.website ? {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  right: 0,
                  width: 3,
                  height: '100%',
                  background: '#10b981',
                  borderRadius: '0 8px 8px 0',
                } : {},
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <PublicIcon sx={{ fontSize: 20, color: formData.website ? '#8b5cf6' : 'rgba(255, 255, 255, 0.4)' }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>
                  Website *
                </Typography>
              </Box>
              <TextField
                fullWidth
                value={formData.website}
                onChange={(e) => handleFieldChange('website', e)}
                placeholder="https://example.com"
                variant="outlined"
                size="small"
                inputProps={{
                  style: { 
                    color: 'rgba(255, 255, 255, 0.9) !important',
                    WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                  },
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: 'rgba(0, 0, 0, 0.2)',
                    color: 'rgba(255, 255, 255, 0.9)',
                    '& input': {
                      color: 'rgba(255, 255, 255, 0.9)',
                    },
                    '& fieldset': {
                      borderColor: formData.website ? 'rgba(139, 92, 246, 0.3)' : 'rgba(255, 255, 255, 0.1)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(139, 92, 246, 0.4)',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#8b5cf6',
                    },
                  },
                  '& .MuiInputBase-input::placeholder': {
                    color: 'rgba(255, 255, 255, 0.5)',
                    opacity: 1,
                  },
                }}
              />
            </Box>
          </Grid>

          {/* Row 2: Industry & Founder GitHub */}
          <Grid item xs={12} md={6}>
            <Box
              sx={{
                position: 'relative',
                '&::after': formData.industry ? {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  right: 0,
                  width: 3,
                  height: '100%',
                  background: '#10b981',
                  borderRadius: '0 8px 8px 0',
                } : {},
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <CategoryIcon sx={{ fontSize: 20, color: formData.industry ? '#8b5cf6' : 'rgba(255, 255, 255, 0.4)' }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>
                  Industry *
                </Typography>
              </Box>
              <TextField
                fullWidth
                value={formData.industry}
                onChange={(e) => handleFieldChange('industry', e)}
                placeholder="e.g., FinTech, SaaS, Healthcare"
                variant="outlined"
                size="small"
                inputProps={{
                  style: { 
                    color: 'rgba(255, 255, 255, 0.9) !important',
                    WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                  },
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: 'rgba(0, 0, 0, 0.2)',
                    color: 'rgba(255, 255, 255, 0.9)',
                    '& input': {
                      color: 'rgba(255, 255, 255, 0.9)',
                    },
                    '& fieldset': {
                      borderColor: formData.industry ? 'rgba(139, 92, 246, 0.3)' : 'rgba(255, 255, 255, 0.1)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(139, 92, 246, 0.4)',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#8b5cf6',
                    },
                  },
                  '& .MuiInputBase-input::placeholder': {
                    color: 'rgba(255, 255, 255, 0.5)',
                    opacity: 1,
                  },
                }}
              />
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <CheckCircleIcon sx={{ fontSize: 20, color: 'rgba(255, 255, 255, 0.4)' }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600, fontSize: '0.875rem', color: 'rgba(255, 255, 255, 0.6)' }}>
                  Founder GitHub (Optional)
                </Typography>
              </Box>
              <TextField
                fullWidth
                value={formData.founder_github}
                onChange={(e) => handleFieldChange('founder_github', e)}
                placeholder="https://github.com/username"
                variant="outlined"
                size="small"
                inputProps={{
                  style: { 
                    color: 'rgba(255, 255, 255, 0.9) !important',
                    WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                  },
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: 'rgba(0, 0, 0, 0.2)',
                    color: 'rgba(255, 255, 255, 0.9)',
                    '& input': {
                      color: 'rgba(255, 255, 255, 0.9)',
                    },
                    '& fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.1)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(139, 92, 246, 0.3)',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#8b5cf6',
                    },
                  },
                  '& .MuiInputBase-input::placeholder': {
                    color: 'rgba(255, 255, 255, 0.5)',
                    opacity: 1,
                  },
                }}
              />
            </Box>
          </Grid>

          {/* Row 3: Product Description - Full Width */}
          <Grid item xs={12}>
            <Box
              sx={{
                position: 'relative',
                '&::after': formData.product_description ? {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  right: 0,
                  width: 3,
                  height: '100%',
                  background: '#10b981',
                  borderRadius: '0 8px 8px 0',
                } : {},
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <DescriptionIcon sx={{ fontSize: 20, color: formData.product_description ? '#8b5cf6' : 'rgba(255, 255, 255, 0.4)' }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600, fontSize: '0.875rem' }}>
                  Product Description *
                </Typography>
              </Box>
              <TextField
                fullWidth
                multiline
                rows={4}
                value={formData.product_description}
                onChange={(e) => handleFieldChange('product_description', e)}
                placeholder="Describe what your company does, the problem it solves, and your target market..."
                variant="outlined"
                inputProps={{
                  style: { 
                    color: 'rgba(255, 255, 255, 0.9) !important',
                    WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                  },
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: 'rgba(0, 0, 0, 0.2)',
                    color: 'rgba(255, 255, 255, 0.9) !important',
                    '& .MuiInputBase-input': {
                      color: 'rgba(255, 255, 255, 0.9) !important',
                      WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                    },
                    '& textarea': {
                      color: 'rgba(255, 255, 255, 0.9) !important',
                      WebkitTextFillColor: 'rgba(255, 255, 255, 0.9) !important',
                    },
                    '& fieldset': {
                      borderColor: formData.product_description ? 'rgba(139, 92, 246, 0.3)' : 'rgba(255, 255, 255, 0.1)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(139, 92, 246, 0.4)',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#8b5cf6',
                    },
                  },
                  '& .MuiInputBase-input::placeholder': {
                    color: 'rgba(255, 255, 255, 0.5) !important',
                    opacity: 1,
                    WebkitTextFillColor: 'rgba(255, 255, 255, 0.5) !important',
                  },
                }}
              />
            </Box>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {/* Submit Button - Compact */}
        <Stack spacing={1} sx={{ mt: 3 }}>
          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={loading || progress < 100}
            startIcon={loading ? <CircularProgress size={20} /> : <RocketLaunchIcon />}
            fullWidth
            sx={{
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 700,
              borderRadius: 2,
              background: 'linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%)',
              boxShadow: '0 8px 32px rgba(139, 92, 246, 0.4)',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'translateY(-2px)',
                boxShadow: '0 12px 48px rgba(139, 92, 246, 0.6)',
                background: 'linear-gradient(135deg, #7c3aed 0%, #2563eb 100%)',
              },
              '&:disabled': {
                background: 'rgba(255, 255, 255, 0.1)',
                color: 'rgba(255, 255, 255, 0.3)',
              },
            }}
          >
            {loading ? 'Launching Analysis...' : 'Start Analysis'}
          </Button>
          
          <Typography
            variant="caption"
            sx={{
              textAlign: 'center',
              color: 'rgba(255, 255, 255, 0.5)',
              fontSize: '0.75rem',
            }}
          >
            {progress < 100 
              ? `Complete ${requiredFields.length - completedFields} more field${requiredFields.length - completedFields !== 1 ? 's' : ''} to continue`
              : '✨ Ready to analyze!'}
          </Typography>
        </Stack>
      </Box>
    </Box>
  );
};

export default InputFormEnhanced;

