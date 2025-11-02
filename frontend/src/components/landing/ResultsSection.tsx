/**
 * Results Section Component
 * Showcase performance metrics and research outcomes
 */

import React from 'react';
import { Box, Container, Typography, Grid, Stack, LinearProgress, Button } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PsychologyIcon from '@mui/icons-material/Psychology';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import DownloadIcon from '@mui/icons-material/Download';

interface ModelResult {
  name: string;
  score: number;
  maxScore: number;
  investDecisions: number;
  color: string;
  icon: React.ReactElement;
}

interface WinnerIdentification {
  model: string;
  identified: number;
  total: number;
  percentage: number;
  color: string;
}

const modelResults: ModelResult[] = [
  {
    name: 'Socrat Space',
    score: 94.4,
    maxScore: 100,
    investDecisions: 11,
    color: '#10b981',
    icon: <TrendingUpIcon />,
  },
  {
    name: 'Claude-4.5-Sonnet',
    score: 86.1,
    maxScore: 100,
    investDecisions: 6,
    color: '#f59e0b',
    icon: <PsychologyIcon />,
  },
  {
    name: 'GPT-5',
    score: 72.2,
    maxScore: 100,
    investDecisions: 0,
    color: '#ef4444',
    icon: <HelpOutlineIcon />,
  },
  {
    name: 'Gemini-1.5-Pro',
    score: 66.7,
    maxScore: 100,
    investDecisions: 4,
    color: '#8b5cf6',
    icon: <PsychologyIcon />,
  },
  {
    name: 'Grok-4',
    score: 55.6,
    maxScore: 100,
    investDecisions: 2,
    color: '#ec4899',
    icon: <PsychologyIcon />,
  },
];

const winnerIdentification: WinnerIdentification[] = [
  { model: 'Socrat Space', identified: 10, total: 10, percentage: 100, color: '#10b981' },
  { model: 'Claude-4.5-Sonnet', identified: 6, total: 10, percentage: 60, color: '#f59e0b' },
  { model: 'Gemini-1.5-Pro', identified: 4, total: 10, percentage: 40, color: '#8b5cf6' },
  { model: 'Grok-4', identified: 2, total: 10, percentage: 20, color: '#ec4899' },
  { model: 'GPT-5', identified: 0, total: 10, percentage: 0, color: '#ef4444' },
];

const ResultsSection: React.FC = () => {
  return (
    <Box
      sx={{
        py: { xs: 10, md: 15 },
        position: 'relative',
        background: 'linear-gradient(180deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0) 100%)',
      }}
    >
      <Container maxWidth="lg">
        {/* Section Header */}
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography
            variant="overline"
            sx={{
              color: '#10b981',
              fontWeight: 700,
              letterSpacing: '0.15em',
              fontSize: '0.875rem',
              mb: 2,
              display: 'block',
            }}
          >
            VALIDATED RESULTS
          </Typography>
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '2rem', md: '3rem' },
              fontWeight: 800,
              mb: 2,
              background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.02em',
            }}
          >
            94.4% Accuracy on predicting VC investments of past Y Combinator Companies
          </Typography>
          <Typography
            variant="h6"
            sx={{
              color: 'rgba(255, 255, 255, 0.6)',
              maxWidth: 700,
              mx: 'auto',
              fontWeight: 400,
            }}
          >
            Head-to-head comparison against GPT-5, Claude, Gemini, and Grok on 18 YC startups
          </Typography>
        </Box>

        {/* Main Result Card */}
        <Box
          sx={{
            mb: 8,
            p: 6,
            borderRadius: 4,
            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)',
            backdropFilter: 'blur(20px)',
            border: '2px solid rgba(16, 185, 129, 0.3)',
            boxShadow: '0 20px 60px rgba(16, 185, 129, 0.2)',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Background glow */}
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '100%',
              height: '100%',
              background: 'radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%)',
              filter: 'blur(60px)',
              zIndex: 0,
            }}
          />

          <Grid container spacing={4} sx={{ position: 'relative', zIndex: 1 }}>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  mb: 3,
                }}
              >
                <CheckCircleIcon sx={{ fontSize: 48, color: '#10b981' }} />
                <Box>
                  <Typography
                    variant="h3"
                    sx={{
                      fontWeight: 900,
                      background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)',
                      backgroundClip: 'text',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      mb: 0.5,
                    }}
                  >
                    100%
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 600,
                    }}
                  >
                    Winner Identification Rate
                  </Typography>
                  <Typography
                    variant="body2"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.6)',
                      mt: 0.5,
                    }}
                  >
                    Identified all 10 successful companies as INVEST opportunities
                  </Typography>
                </Box>
              </Box>

              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  mb: 3,
                }}
              >
                <TrendingUpIcon sx={{ fontSize: 48, color: '#10b981' }} />
                <Box>
                  <Typography
                    variant="h3"
                    sx={{
                      fontWeight: 900,
                      background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)',
                      backgroundClip: 'text',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      mb: 0.5,
                    }}
                  >
                    94.4%
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 600,
                    }}
                  >
                    Weighted Accuracy
                  </Typography>
                  <Typography
                    variant="body2"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.6)',
                      mt: 0.5,
                    }}
                  >
                    Outperformed all baseline models by 8+ percentage points
                  </Typography>
                </Box>
              </Box>

              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                }}
              >
                <PsychologyIcon sx={{ fontSize: 48, color: '#10b981' }} />
                <Box>
                  <Typography
                    variant="h3"
                    sx={{
                      fontWeight: 900,
                      background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)',
                      backgroundClip: 'text',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      mb: 0.5,
                    }}
                  >
                    11
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontWeight: 600,
                    }}
                  >
                    Confident INVEST Decisions
                  </Typography>
                  <Typography
                    variant="body2"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.6)',
                      mt: 0.5,
                    }}
                  >
                    1.8x more than Claude, 2.75x more than Gemini
                  </Typography>
                </Box>
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  p: 4,
                  borderRadius: 3,
                  background: 'rgba(255, 255, 255, 0.05)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                }}
              >
                <Typography
                  variant="h6"
                  sx={{
                    fontWeight: 700,
                    mb: 3,
                    color: 'text.primary',
                  }}
                >
                  Test Dataset
                </Typography>
                <Stack spacing={3}>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                        Test Dataset
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: '#10b981' }}>
                        94.4%
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={94.4}
                      sx={{
                        height: 12,
                        borderRadius: 1,
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(90deg, #10b981 0%, #3b82f6 100%)',
                        },
                      }}
                    />
                  </Box>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                        10 Successful (INVEST targets)
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: '#10b981' }}>
                        10/10
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={100}
                      sx={{
                        height: 12,
                        borderRadius: 1,
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(90deg, #10b981 0%, #22c55e 100%)',
                        },
                      }}
                    />
                  </Box>
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                        8 Failed (PASS targets)
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: '#10b981' }}>
                        7/8
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={87.5}
                      sx={{
                        height: 12,
                        borderRadius: 1,
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(90deg, #10b981 0%, #84cc16 100%)',
                        },
                      }}
                    />
                  </Box>
                </Stack>
              </Box>
            </Grid>
          </Grid>
        </Box>

        {/* Comparison Chart */}
        <Box sx={{ mb: 8 }}>
          <Typography
            variant="h4"
            sx={{
              fontWeight: 700,
              mb: 4,
              textAlign: 'center',
              color: 'text.primary',
            }}
          >
            Performance Comparison
          </Typography>
          <Stack spacing={3}>
            {modelResults.map((model, index) => (
              <Box
                key={index}
                sx={{
                  p: 3,
                  borderRadius: 2,
                  background: model.name === 'Socrat Space' 
                    ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)'
                    : 'rgba(255, 255, 255, 0.03)',
                  border: model.name === 'Socrat Space'
                    ? '2px solid rgba(16, 185, 129, 0.3)'
                    : '1px solid rgba(255, 255, 255, 0.08)',
                  backdropFilter: 'blur(20px)',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    borderColor: `${model.color}40`,
                  },
                }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 2,
                    mb: 2,
                  }}
                >
                  <Box
                    sx={{
                      width: 48,
                      height: 48,
                      borderRadius: 1,
                      background: `${model.color}20`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: model.color,
                    }}
                  >
                    {model.icon}
                  </Box>
                  <Box sx={{ flex: 1 }}>
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 700,
                        color: 'text.primary',
                      }}
                    >
                      {model.name}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{
                        color: 'rgba(255, 255, 255, 0.6)',
                      }}
                    >
                      {model.investDecisions} confident INVEST decisions
                    </Typography>
                  </Box>
                  <Box sx={{ textAlign: 'right', minWidth: 80 }}>
                    <Typography
                      variant="h4"
                      sx={{
                        fontWeight: 900,
                        background: `linear-gradient(135deg, ${model.color} 0%, ${model.color}CC 100%)`,
                        backgroundClip: 'text',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                      }}
                    >
                      {model.score}%
                    </Typography>
                  </Box>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={model.score}
                  sx={{
                    height: 10,
                    borderRadius: 1,
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    '& .MuiLinearProgress-bar': {
                      background: `linear-gradient(90deg, ${model.color} 0%, ${model.color}CC 100%)`,
                    },
                  }}
                />
              </Box>
            ))}
          </Stack>
        </Box>

        {/* Winner Identification */}
        <Box>
          <Typography
            variant="h4"
            sx={{
              fontWeight: 700,
              mb: 4,
              textAlign: 'center',
              color: 'text.primary',
            }}
          >
            The #1 Metric: Identifying Winners
          </Typography>
          <Typography
            variant="body1"
            sx={{
              color: 'rgba(255, 255, 255, 0.6)',
              textAlign: 'center',
              mb: 4,
              maxWidth: 700,
              mx: 'auto',
            }}
          >
            In venture capital, missing a unicorn is far more costly than a false positive. 
            This is the most critical metric for fund performance.
          </Typography>
          
          <Grid container spacing={3}>
            {winnerIdentification.map((item, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Box
                  sx={{
                    p: 3,
                    borderRadius: 2,
                    background: item.model === 'Socrat Space'
                      ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)'
                      : 'rgba(255, 255, 255, 0.03)',
                    border: item.model === 'Socrat Space'
                      ? '2px solid rgba(16, 185, 129, 0.3)'
                      : '1px solid rgba(255, 255, 255, 0.08)',
                    backdropFilter: 'blur(20px)',
                    textAlign: 'center',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      borderColor: `${item.color}40`,
                    },
                  }}
                >
                  <Typography
                    variant="h5"
                    sx={{
                      fontWeight: 900,
                      mb: 2,
                      background: `linear-gradient(135deg, ${item.color} 0%, ${item.color}CC 100%)`,
                      backgroundClip: 'text',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                    }}
                  >
                    {item.percentage}%
                  </Typography>
                  <Typography
                    variant="body2"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.8)',
                      fontWeight: 600,
                      mb: 1,
                    }}
                  >
                    {item.identified}/{item.total} Winners Identified
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.5)',
                      textTransform: 'uppercase',
                      letterSpacing: '0.1em',
                    }}
                  >
                    {item.model}
                  </Typography>
                  {item.percentage === 0 && (
                    <Box
                      sx={{
                        mt: 2,
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: 0.5,
                        color: '#ef4444',
                      }}
                    >
                      <CancelIcon sx={{ fontSize: 16 }} />
                      <Typography variant="caption" sx={{ fontWeight: 600 }}>
                        Missed All
                      </Typography>
                    </Box>
                  )}
                  {item.percentage === 100 && (
                    <Box
                      sx={{
                        mt: 2,
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: 0.5,
                        color: '#10b981',
                      }}
                    >
                      <CheckCircleIcon sx={{ fontSize: 16 }} />
                      <Typography variant="caption" sx={{ fontWeight: 600 }}>
                        Perfect Score
                      </Typography>
                    </Box>
                  )}
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Research Note */}
        <Box
          sx={{
            mt: 8,
            p: 4,
            borderRadius: 3,
            background: 'rgba(59, 130, 246, 0.1)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(59, 130, 246, 0.2)',
          }}
        >
          <Typography
            variant="body2"
            sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              textAlign: 'center',
              lineHeight: 1.8,
              mb: 3,
            }}
          >
            <strong>Research Note:</strong> These results are from a test system validation on 18 Y Combinator 
            companies (W25 and F25 batches). The production system uses a 5-phase structured analysis framework 
            with 7+ specialized agents, deeper research capabilities, and proprietary scoring models trained on 500+ companies.
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              component="a"
              href="/research_paper.pdf"
              download
              sx={{
                color: '#60a5fa',
                borderColor: 'rgba(59, 130, 246, 0.4)',
                background: 'rgba(59, 130, 246, 0.1)',
                '&:hover': {
                  borderColor: 'rgba(59, 130, 246, 0.6)',
                  background: 'rgba(59, 130, 246, 0.15)',
                  transform: 'translateY(-2px)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              Download Research Paper (PDF)
            </Button>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default ResultsSection;

