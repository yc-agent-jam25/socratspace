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
  Chip,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { keyframes } from '@mui/system';
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

const pulse = keyframes`
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
`;

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
  const completedFields = requiredFields.filter(field => formData[field as keyof CompanyData]?.trim()).length;
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

  const fields = [
    {
      key: 'company_name' as const,
      label: 'Company Name',
      icon: <BusinessIcon />,
      placeholder: 'e.g., Stripe, Notion, Figma',
      required: true,
      multiline: false,
    },
    {
      key: 'website' as const,
      label: 'Website',
      icon: <PublicIcon />,
      placeholder: 'https://example.com',
      required: true,
      multiline: false,
    },
    {
      key: 'founder_github' as const,
      label: 'Founder GitHub (Optional)',
      icon: <CheckCircleIcon />,
      placeholder: 'https://github.com/username',
      required: false,
      multiline: false,
    },
    {
      key: 'industry' as const,
      label: 'Industry',
      icon: <CategoryIcon />,
      placeholder: 'e.g., FinTech, SaaS, Healthcare',
      required: true,
      multiline: false,
    },
    {
      key: 'product_description' as const,
      label: 'Product Description',
      icon: <DescriptionIcon />,
      placeholder: 'Describe what your company does, the problem it solves, and your target market...',
      required: true,
      multiline: true,
    },
  ];

  return (
    <Box
      sx={{
        maxWidth: 1000,
        mx: 'auto',
        animation: 'fadeInUp 0.6s ease-out',
      }}
    >
      {/* Header */}
      <Box sx={{ textAlign: 'center', mb: 5 }}>
        <Typography
          variant="h3"
          sx={{
            fontWeight: 800,
            mb: 2,
            background: 'linear-gradient(135deg, #ffffff 0%, #a78bfa 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '-0.02em',
          }}
        >
          Tell Us About Your Startup
        </Typography>
        <Typography
          variant="h6"
          sx={{
            color: 'rgba(255, 255, 255, 0.7)',
            fontWeight: 400,
            mb: 3,
          }}
        >
          Our 8 AI agents will analyze every aspect in 5 minutes
        </Typography>

        {/* Progress bar */}
        <Box sx={{ maxWidth: 600, mx: 'auto' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 600 }}>
              Completion
            </Typography>
            <Typography variant="caption" sx={{ color: '#8b5cf6', fontWeight: 700 }}>
              {Math.round(progress)}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{
              height: 8,
              borderRadius: 4,
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              '& .MuiLinearProgress-bar': {
                background: 'linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%)',
                borderRadius: 4,
              },
            }}
          />
        </Box>
      </Box>

      {/* Form */}
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          p: 4,
          background: 'rgba(255, 255, 255, 0.04)',
          backdropFilter: 'blur(24px)',
          WebkitBackdropFilter: 'blur(24px)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: 3,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
        }}
      >
        <Grid container spacing={3}>
          {fields.map((field, index) => (
            <Grid item xs={12} key={field.key}>
              <Card
                sx={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  backdropFilter: 'blur(10px)',
                  border: formData[field.key] 
                    ? '1px solid rgba(139, 92, 246, 0.3)' 
                    : '1px solid rgba(255, 255, 255, 0.05)',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    borderColor: 'rgba(139, 92, 246, 0.5)',
                    transform: 'translateY(-2px)',
                  },
                  animation: 'fadeInUp 0.5s ease-out',
                  animationDelay: `${index * 0.1}s`,
                  animationFillMode: 'backwards',
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.5 }}>
                    <Box
                      sx={{
                        width: 40,
                        height: 40,
                        borderRadius: 2,
                        background: formData[field.key]
                          ? 'linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%)'
                          : 'rgba(255, 255, 255, 0.05)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: formData[field.key] ? 'white' : 'rgba(255, 255, 255, 0.4)',
                        transition: 'all 0.3s ease',
                      }}
                    >
                      {field.icon}
                    </Box>
                    <Box sx={{ flex: 1 }}>
                      <Typography
                        variant="subtitle1"
                        sx={{
                          fontWeight: 600,
                          color: 'text.primary',
                        }}
                      >
                        {field.label}
                      </Typography>
                      {field.required && (
                        <Chip
                          label="Required"
                          size="small"
                          sx={{
                            height: 20,
                            fontSize: '0.65rem',
                            background: 'rgba(239, 68, 68, 0.15)',
                            color: '#f87171',
                            fontWeight: 600,
                            border: '1px solid rgba(239, 68, 68, 0.3)',
                          }}
                        />
                      )}
                    </Box>
                    {formData[field.key] && (
                      <CheckCircleIcon
                        sx={{
                          color: '#10b981',
                          animation: `${pulse} 1s ease-in-out`,
                        }}
                      />
                    )}
                  </Box>
                  <TextField
                    fullWidth
                    multiline={field.multiline}
                    rows={field.multiline ? 4 : 1}
                    value={formData[field.key]}
                    onChange={(e) => handleFieldChange(field.key, e)}
                    placeholder={field.placeholder}
                    variant="outlined"
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        backgroundColor: 'rgba(0, 0, 0, 0.2)',
                        '& fieldset': {
                          borderColor: 'transparent',
                        },
                        '&:hover fieldset': {
                          borderColor: 'rgba(139, 92, 246, 0.3)',
                        },
                        '&.Mui-focused fieldset': {
                          borderColor: '#8b5cf6',
                          borderWidth: 2,
                        },
                      },
                    }}
                  />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {error}
          </Alert>
        )}

        {/* Submit Button */}
        <Stack spacing={2} sx={{ mt: 4 }}>
          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={loading || progress < 100}
            startIcon={loading ? <CircularProgress size={20} /> : <RocketLaunchIcon />}
            sx={{
              py: 2,
              fontSize: '1.125rem',
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
            {loading ? 'Launching Analysis...' : 'Start 8-Agent Analysis'}
          </Button>
          
          <Typography
            variant="caption"
            sx={{
              textAlign: 'center',
              color: 'rgba(255, 255, 255, 0.5)',
              fontSize: '0.875rem',
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

