/**
 * System Architecture Section Component
 * Visual representation of the test system vs production system
 */

import React, { useState } from 'react';
import { Box, Container, Typography, Grid, Stack, ToggleButtonGroup, ToggleButton, Chip } from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import SpeedIcon from '@mui/icons-material/Speed';
import ScienceIcon from '@mui/icons-material/Science';
import PsychologyIcon from '@mui/icons-material/Psychology';
import StorageIcon from '@mui/icons-material/Storage';
import TimelineIcon from '@mui/icons-material/Timeline';

interface SystemComponent {
  title: string;
  testSystem: string;
  production: string;
  icon: React.ReactElement;
  color: string;
}

const components: SystemComponent[] = [
  {
    title: 'Agent Count',
    testSystem: '3 agents (Signal, Risk, Synthesis)',
    production: '7+ specialized agents (Market, Team, Product, etc.)',
    icon: <PsychologyIcon />,
    color: '#3b82f6',
  },
  {
    title: 'Research Depth',
    testSystem: 'Fast website checks, basic founder search',
    production: 'Web archives, historical funding databases, LinkedIn API',
    icon: <ScienceIcon />,
    color: '#10b981',
  },
  {
    title: 'Deliberation Rounds',
    testSystem: '1 round with simplified scoring',
    production: 'Up to 5 rounds with structured debate protocols',
    icon: <TimelineIcon />,
    color: '#f59e0b',
  },
  {
    title: 'Data Sources',
    testSystem: 'Public web scraping only',
    production: 'Proprietary databases, Crunchbase, news archives',
    icon: <StorageIcon />,
    color: '#8b5cf6',
  },
  {
    title: 'Speed',
    testSystem: '30-60 seconds per company',
    production: '5-10 minutes per company (comprehensive)',
    icon: <SpeedIcon />,
    color: '#ec4899',
  },
  {
    title: 'Evaluation Heuristics',
    testSystem: 'Simple threshold-based rules',
    production: 'Proprietary models trained on 500+ companies',
    icon: <AutoAwesomeIcon />,
    color: '#06b6d4',
  },
];

const phases = [
  {
    number: '01',
    title: 'Submit Company Info',
    description: 'Enter basic details about the startup: name, website, founder GitHub, industry, and product description.',
    icon: '📝',
    color: '#3b82f6',
  },
  {
    number: '02',
    title: 'Market Discussion',
    description: 'Specialized agents research the market, then Bull and Bear debate the opportunity. Risk Assessor flags key concerns.',
    icon: '📊',
    color: '#10b981',
  },
  {
    number: '03',
    title: 'Team & Product Rounds',
    description: 'Agents evaluate founders and products through sequential discussions. Each round has focused debate before moving on.',
    icon: '💬',
    color: '#f59e0b',
  },
  {
    number: '04',
    title: 'Financial Analysis',
    description: 'Financial Analyst reviews metrics, Bull and Bear argue viability, Risk Assessor identifies financial red flags.',
    icon: '💰',
    color: '#8b5cf6',
  },
  {
    number: '05',
    title: 'Final Decision',
    description: 'Lead Partner synthesizes all discussion tasks and delivers: Invest, Maybe, or Pass with comprehensive reasoning.',
    icon: '✅',
    color: '#10b981',
  },
];

const SystemArchitectureSection: React.FC = () => {
  const [view, setView] = useState<'testSystem' | 'production'>('testSystem');

  return (
    <Box
      sx={{
        py: { xs: 8, md: 12 },
        position: 'relative',
        background: 'rgba(255, 255, 255, 0.02)',
      }}
    >
      <Container maxWidth="lg">
        {/* Introduction Section */}
        <Box sx={{ mb: 8 }}>
          <Typography
            variant="h3"
            sx={{
              fontSize: { xs: '1.75rem', md: '2.5rem' },
              fontWeight: 800,
              mb: 3,
              textAlign: 'center',
              background: 'linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.02em',
            }}
          >
            VCDeliberate: Multi-Agent Investment Analysis
          </Typography>
          <Typography
            variant="body1"
            sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              maxWidth: 900,
              mx: 'auto',
              lineHeight: 1.8,
              textAlign: 'center',
              mb: 3,
              fontSize: { xs: '1rem', md: '1.125rem' },
            }}
          >
            Early-stage startup investment decisions are notoriously difficult, with venture capital firms facing high uncertainty and limited information. Traditional single-model AI approaches suffer from inconsistency and over-conservatism, frequently defaulting to "maybe" decisions. We introduce <strong>VCDeliberate</strong>, a multi-agent deliberation framework where multiple AI agents collaborate to evaluate startups and make decisive investment recommendations.
          </Typography>
          <Box
            sx={{
              p: 3,
              borderRadius: 2,
              background: 'rgba(59, 130, 246, 0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(59, 130, 246, 0.2)',
              maxWidth: 900,
              mx: 'auto',
            }}
          >
            <Typography
              variant="body2"
              sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                fontStyle: 'italic',
                textAlign: 'center',
                lineHeight: 1.8,
              }}
            >
              <strong>Note:</strong> This validation presents a <strong>test system</strong> (downscaled version) of our production VCDeliberate system. The full production system incorporates additional agents, deeper research capabilities, real-time data integration, and proprietary evaluation heuristics developed over multiple deployment cycles.
            </Typography>
          </Box>
        </Box>

        {/* Five Phases Section */}
        <Box sx={{ mb: 10 }}>
          <Typography
            variant="h4"
            sx={{
              fontSize: { xs: '1.5rem', md: '2rem' },
              fontWeight: 700,
              mb: 1,
              textAlign: 'center',
              color: 'text.primary',
            }}
          >
            Five Rounds of Structured Analysis
          </Typography>
          <Typography
            variant="body2"
            sx={{
              color: 'rgba(255, 255, 255, 0.6)',
              textAlign: 'center',
              mb: 4,
            }}
          >
            The production system processes investment decisions through sequential deliberation phases
          </Typography>
          
          <Stack spacing={2}>
            {phases.map((phase, index) => (
              <Box key={index}>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: { xs: 2, md: 3 },
                    p: { xs: 2, md: 3 },
                    borderRadius: 2,
                    background: 'rgba(255, 255, 255, 0.03)',
                    backdropFilter: 'blur(20px)',
                    border: `1px solid ${phase.color}40`,
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateX(8px)',
                      background: 'rgba(255, 255, 255, 0.05)',
                      borderColor: `${phase.color}60`,
                    },
                  }}
                >
                  {/* Phase Icon & Number */}
                  <Box
                    sx={{
                      flexShrink: 0,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 2,
                    }}
                  >
                    <Box
                      sx={{
                        width: { xs: 60, md: 80 },
                        height: { xs: 60, md: 80 },
                        borderRadius: 2,
                        background: `linear-gradient(135deg, ${phase.color}20 0%, ${phase.color}10 100%)`,
                        border: `2px solid ${phase.color}40`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: { xs: '2rem', md: '2.5rem' },
                      }}
                    >
                      {phase.icon}
                    </Box>
                    <Typography
                      variant="h2"
                      sx={{
                        fontWeight: 900,
                        color: `${phase.color}40`,
                        fontSize: { xs: '3rem', md: '4rem' },
                        lineHeight: 1,
                        display: { xs: 'none', sm: 'block' },
                      }}
                    >
                      {phase.number}
                    </Typography>
                  </Box>

                  {/* Content */}
                  <Box sx={{ flex: 1 }}>
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: 700,
                        mb: 0.5,
                        color: 'text.primary',
                        fontSize: { xs: '1rem', md: '1.25rem' },
                      }}
                    >
                      Round {phase.number}: {phase.title}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{
                        color: 'rgba(255, 255, 255, 0.7)',
                        lineHeight: 1.6,
                        fontSize: { xs: '0.875rem', md: '1rem' },
                      }}
                    >
                      {phase.description}
                    </Typography>
                  </Box>
                </Box>

                {/* Connecting line */}
                {index < phases.length - 1 && (
                  <Box
                    sx={{
                      width: 2,
                      height: 20,
                      background: `linear-gradient(180deg, ${phase.color}40 0%, ${phases[index + 1].color}40 100%)`,
                      mx: { xs: 2, md: 3 },
                      my: 1,
                    }}
                  />
                )}
              </Box>
            ))}
          </Stack>
        </Box>

        {/* Section Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography
            variant="overline"
            sx={{
              color: '#3b82f6',
              fontWeight: 700,
              letterSpacing: '0.15em',
              fontSize: '0.875rem',
              mb: 2,
              display: 'block',
            }}
          >
            SYSTEM ARCHITECTURE
          </Typography>
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '2rem', md: '3rem' },
              fontWeight: 800,
              mb: 2,
              background: 'linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.02em',
            }}
          >
            Test System vs Production System
          </Typography>
          <Typography
            variant="h6"
            sx={{
              color: 'rgba(255, 255, 255, 0.6)',
              maxWidth: 700,
              mx: 'auto',
              fontWeight: 400,
              mb: 4,
              fontSize: { xs: '1rem', md: '1.25rem' },
            }}
          >
            See how the test system validates core principles while the production system scales for accuracy
          </Typography>

          {/* Toggle View */}
          <ToggleButtonGroup
            value={view}
            exclusive
            onChange={(_, newView) => newView && setView(newView)}
            sx={{
              '& .MuiToggleButton-root': {
                px: 4,
                py: 1.5,
                fontSize: '1rem',
                fontWeight: 600,
                color: 'rgba(255, 255, 255, 0.6)',
                borderColor: 'rgba(255, 255, 255, 0.2)',
                borderRadius: 2,
                '&.Mui-selected': {
                  color: '#3b82f6',
                  backgroundColor: 'rgba(59, 130, 246, 0.15)',
                  borderColor: 'rgba(59, 130, 246, 0.4)',
                  '&:hover': {
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                  },
                },
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                },
              },
            }}
          >
            <ToggleButton value="testSystem">Test System</ToggleButton>
            <ToggleButton value="production">Production System</ToggleButton>
          </ToggleButtonGroup>
        </Box>

        {/* Visual Architecture Diagram */}
        <Box sx={{ mb: 4 }}>
          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              mb: 3,
              textAlign: 'center',
              color: 'text.primary',
              fontSize: { xs: '1.25rem', md: '1.5rem' },
            }}
          >
            {view === 'production' 
              ? 'Production System Architecture (5-Phase Framework)'
              : 'Test System Architecture (3-Phase Framework)'}
          </Typography>
        </Box>
        
        <Box
          sx={{
            mb: 8,
            p: { xs: 3, md: 6 },
            borderRadius: 4,
            background: 'rgba(255, 255, 255, 0.03)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Background for Test System view */}
          {view === 'testSystem' && (
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)',
                zIndex: 0,
              }}
            />
          )}

          {/* Background for Production view */}
          {view === 'production' && (
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)',
                zIndex: 0,
              }}
            />
          )}

          <Grid container spacing={4} sx={{ position: 'relative', zIndex: 1 }}>
            {/* Input */}
            <Grid item xs={12}>
              <Box
                sx={{
                  p: 3,
                  borderRadius: 2,
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '2px solid rgba(59, 130, 246, 0.4)',
                  textAlign: 'center',
                }}
              >
                <Typography variant="h6" sx={{ fontWeight: 700, mb: 1, fontSize: { xs: '1rem', md: '1.25rem' } }}>
                  📥 INPUT
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  Company Information, YC Batch, Founders, Product Details
                </Typography>
              </Box>
            </Grid>

            {/* Phase 1 */}
            <Grid item xs={12}>
              <Box
                sx={{
                  p: 3,
                  borderRadius: 2,
                  background: 'rgba(16, 185, 129, 0.15)',
                  border: '2px solid rgba(16, 185, 129, 0.3)',
                  position: 'relative',
                }}
              >
                <Typography variant="h6" sx={{ fontWeight: 700, mb: 3, fontSize: { xs: '1rem', md: '1.25rem' } }}>
                  🔍 PHASE 1: Date-Aware Research
                </Typography>
                {view === 'testSystem' ? (
                  <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
                    {['Website Check', 'Founder Search', 'Basic Analysis'].map((item, idx) => (
                      <Chip
                        key={idx}
                        label={item}
                        sx={{
                          background: 'rgba(16, 185, 129, 0.2)',
                          color: '#34d399',
                          border: '1px solid rgba(16, 185, 129, 0.4)',
                        }}
                      />
                    ))}
                  </Stack>
                ) : (
                  <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
                    {['Web Archives', 'Funding DBs', 'LinkedIn API', 'News Search', 'Deep Analysis'].map((item, idx) => (
                      <Chip
                        key={idx}
                        label={item}
                        sx={{
                          background: 'rgba(16, 185, 129, 0.2)',
                          color: '#34d399',
                          border: '1px solid rgba(16, 185, 129, 0.4)',
                        }}
                      />
                    ))}
                  </Stack>
                )}
              </Box>
            </Grid>

            {/* Phase 2 */}
            <Grid item xs={12}>
              <Box
                sx={{
                  p: 3,
                  borderRadius: 2,
                  background: 'rgba(245, 158, 11, 0.15)',
                  border: '2px solid rgba(245, 158, 11, 0.3)',
                }}
              >
                <Typography variant="h6" sx={{ fontWeight: 700, mb: 3, fontSize: { xs: '1rem', md: '1.25rem' } }}>
                  ⚖️ PHASE 2: Multi-Agent Deliberation
                </Typography>
                {view === 'testSystem' ? (
                  <Grid container spacing={2}>
                    {['Signal Evaluator', 'Risk Assessor', 'Synthesizer'].map((agent, idx) => (
                      <Grid item xs={12} sm={4} key={idx}>
                        <Box
                          sx={{
                            p: 2,
                            borderRadius: 1,
                            background: 'rgba(245, 158, 11, 0.2)',
                            border: '1px solid rgba(245, 158, 11, 0.4)',
                            textAlign: 'center',
                          }}
                        >
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {agent}
                          </Typography>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>
                ) : (
                  <Grid container spacing={2}>
                    {['Market Analyst', 'Team Evaluator', 'Product Specialist', 'Traction Detective', 'Risk Assessor', 'Synthesizer', 'Meta-Evaluator'].map((agent, idx) => (
                      <Grid item xs={12} sm={6} md={4} key={idx}>
                        <Box
                          sx={{
                            p: 2,
                            borderRadius: 1,
                            background: 'rgba(245, 158, 11, 0.2)',
                            border: '1px solid rgba(245, 158, 11, 0.4)',
                            textAlign: 'center',
                          }}
                        >
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {agent}
                          </Typography>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>
                )}
                <Typography
                  variant="caption"
                  sx={{
                    display: 'block',
                    mt: 2,
                    color: 'rgba(255, 255, 255, 0.5)',
                    textAlign: 'center',
                  }}
                >
                  {view === 'testSystem' ? '1 deliberation round' : 'Up to 5 iteration rounds with feedback loops'}
                </Typography>
              </Box>
            </Grid>

            {/* Phase 3 */}
            <Grid item xs={12}>
              <Box
                sx={{
                  p: 3,
                  borderRadius: 2,
                  background: 'rgba(139, 92, 246, 0.15)',
                  border: '2px solid rgba(139, 92, 246, 0.3)',
                  textAlign: 'center',
                }}
              >
                <Typography variant="h6" sx={{ fontWeight: 700, mb: 2, fontSize: { xs: '1rem', md: '1.25rem' } }}>
                  ✅ PHASE 3: Decision Synthesis
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  Net Score Calculation → INVEST / PASS / MAYBE
                  <br />
                  {view === 'testSystem' 
                    ? 'Simple threshold-based rules'
                    : 'Proprietary scoring models trained on 500+ companies'}
                </Typography>
              </Box>
            </Grid>

            {/* Output */}
            <Grid item xs={12}>
              <Box
                sx={{
                  p: 3,
                  borderRadius: 2,
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '2px solid rgba(59, 130, 246, 0.4)',
                  textAlign: 'center',
                }}
              >
                <Typography variant="h6" sx={{ fontWeight: 700, mb: 1, fontSize: { xs: '1rem', md: '1.25rem' } }}>
                  📊 OUTPUT
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  Decision, Confidence, Reasoning, Risk Factors, Positive Signals
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Box>

        {/* Component Comparison */}
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h4"
            sx={{
              fontSize: { xs: '1.5rem', md: '2rem' },
              fontWeight: 700,
              mb: 4,
              textAlign: 'center',
              color: 'text.primary',
            }}
          >
            Detailed Component Comparison
          </Typography>
          <Grid container spacing={3}>
            {components.map((component, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Box
                  sx={{
                    height: '100%',
                    p: 3,
                    borderRadius: 3,
                    background: 'rgba(255, 255, 255, 0.03)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    transition: 'all 0.4s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      borderColor: `${component.color}40`,
                      background: 'rgba(255, 255, 255, 0.05)',
                      '& .component-icon': {
                        transform: 'scale(1.1)',
                        color: component.color,
                      },
                    },
                  }}
                >
                  <Stack spacing={3}>
                    {/* Icon and Title */}
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 2,
                      }}
                    >
                      <Box
                        className="component-icon"
                        sx={{
                          width: 48,
                          height: 48,
                          borderRadius: 1,
                          background: `${component.color}20`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: component.color,
                          transition: 'all 0.4s ease',
                        }}
                      >
                        {component.icon}
                      </Box>
                      <Typography
                        variant="h6"
                        sx={{
                          fontWeight: 700,
                          color: 'text.primary',
                        }}
                      >
                        {component.title}
                      </Typography>
                    </Box>

                    {/* Test System Description */}
                    <Box>
                      <Chip
                        label="Test System"
                        size="small"
                        sx={{
                          mb: 1,
                          background: 'rgba(139, 92, 246, 0.2)',
                          color: '#a78bfa',
                          border: '1px solid rgba(139, 92, 246, 0.3)',
                        }}
                      />
                      <Typography
                        variant="body2"
                        sx={{
                          color: 'rgba(255, 255, 255, 0.7)',
                          pl: 1,
                        }}
                      >
                        {component.testSystem}
                      </Typography>
                    </Box>

                    {/* Production Description */}
                    <Box>
                      <Chip
                        label="Production System"
                        size="small"
                        sx={{
                          mb: 1,
                          background: 'rgba(16, 185, 129, 0.2)',
                          color: '#34d399',
                          border: '1px solid rgba(16, 185, 129, 0.3)',
                        }}
                      />
                      <Typography
                        variant="body2"
                        sx={{
                          color: 'rgba(255, 255, 255, 0.7)',
                          pl: 1,
                        }}
                      >
                        {component.production}
                      </Typography>
                    </Box>
                  </Stack>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Key Insight */}
        <Box
          sx={{
            p: { xs: 4, md: 5 },
            borderRadius: 3,
            background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(139, 92, 246, 0.3)',
            textAlign: 'center',
          }}
        >
          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              mb: 2,
              background: 'linear-gradient(135deg, #a78bfa 0%, #3b82f6 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontSize: { xs: '1.25rem', md: '1.5rem' },
            }}
          >
            Why This Test System Matters
          </Typography>
          <Typography
            variant="body1"
            sx={{
              color: 'rgba(255, 255, 255, 0.8)',
              lineHeight: 1.8,
              maxWidth: 800,
              mx: 'auto',
              fontSize: { xs: '0.9rem', md: '1rem' },
            }}
          >
            The test system validates that <strong>core architectural principles</strong>—multi-agent 
            deliberation, date-aware research, and consensus-building—deliver superior results even when 
            scaled down for speed. This demonstrates that our approach is fundamentally sound and will 
            only improve with the production system's deeper research and specialized agents.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default SystemArchitectureSection;
