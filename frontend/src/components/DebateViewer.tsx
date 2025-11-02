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
  Grid,
  Tabs,
  Tab
} from '@mui/material';
import type { CompanyData, Agent } from '../lib/types';
import { useSimulation } from '../hooks/useSimulation';
import PhaseIndicator from './PhaseIndicator';
import DecisionPanelEnhanced from './DecisionPanelEnhanced';
import LiveActivityFeed from './debate/LiveActivityFeed';
import CouncilProgress from './debate/CouncilProgress';
import CouncilAvatarBar from './debate/CouncilAvatarBar';
import BullBearArena from './debate/BullBearArena';

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

const agents: Agent[] = [
  { id: 'system', name: 'System', color: '#6b7280' }, // System messages from orchestrator
  { id: 'unknown', name: '⚠️ Unknown Agent', color: '#dc2626' }, // Debug: backend failed to extract agent
  { id: 'market_researcher', name: 'Market Researcher', color: '#3b82f6' },
  { id: 'founder_evaluator', name: 'Founder Evaluator', color: '#10b981' },
  { id: 'product_critic', name: 'Product Critic', color: '#f59e0b' },
  { id: 'financial_analyst', name: 'Financial Analyst', color: '#8b5cf6' },
  { id: 'risk_assessor', name: 'Risk Assessor', color: '#ef4444' },
  { id: 'bull_agent', name: 'Bull Agent', color: '#10b981' },
  { id: 'bear_agent', name: 'Bear Agent', color: '#ef4444' },
  { id: 'lead_partner', name: 'Lead Partner', color: '#3b82f6' }
];

const DebateViewer: React.FC<DebateViewerProps> = ({ sessionId, companyData, onReset }) => {
  // Check if we should use SSE (when backend is ready, set VITE_USE_SSE=true)
  const useSSE = import.meta.env.VITE_USE_SSE === 'true';
  
  const {
    phase,
    messages,
    decision,
    isRunning,
    elapsedTime,
    connectionStatus,
    error,
    startSimulation,
    reconnect,
  } = useSimulation({ sessionId, useSSE });
  const [activeTab, setActiveTab] = useState<'chamber' | 'decision'>('chamber');

  // Start simulation when component mounts
  useEffect(() => {
    startSimulation();
  }, [startSimulation]);

  // Switch to decision tab when decision is ready
  useEffect(() => {
    if (decision) {
      setActiveTab('decision');
    }
  }, [decision]);

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
      {/* Header Section */}
      <Paper 
        elevation={3}
        sx={{ 
          p: 3, 
          mb: 3,
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 2 }}>
          <Box sx={{ flex: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <BusinessIcon sx={{ color: 'primary.main' }} />
              <Typography variant="h4" sx={{ fontWeight: 700, letterSpacing: '-0.02em' }}>
                {companyData.company_name}
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {companyData.industry} • {companyData.website}
            </Typography>
            
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              <Chip
                label={getPhaseLabel()}
                color="primary"
                size="small"
                sx={{ fontWeight: 600 }}
              />
              <Chip
                icon={<AccessTimeIcon />}
                label={formatElapsedTime(elapsedTime)}
                variant="outlined"
                size="small"
              />
              <Chip
                label={`Session: ${String(sessionId).slice(0, 8)}...`}
                variant="outlined"
                size="small"
              />
              {/* SSE Connection Status */}
              {connectionStatus && (
                <Chip
                  icon={
                    connectionStatus === 'connected' ? (
                      <CloudDoneIcon />
                    ) : connectionStatus === 'error' ? (
                      <ErrorOutlineIcon />
                    ) : (
                      <CloudOffIcon />
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
                  }}
                />
              )}
            </Stack>
          </Box>
          
          <Button 
            variant="outlined" 
            onClick={onReset}
            disabled={isRunning}
            sx={{ 
              fontWeight: 600,
              minWidth: 140,
            }}
          >
            New Analysis
          </Button>
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
            mb: 3,
            height: 6,
            borderRadius: 3,
          }} 
        />
      )}

      {/* Tabs Navigation (shown when decision is available) */}
      {decision && (
        <Box sx={{ mb: 3 }}>
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

      {/* Main Content - Council Progress + Live Activity Feed */}
      {activeTab === 'chamber' && !decision && (
        <Box>
          {/* Show Bull vs Bear Arena during debate phase, otherwise show Council Avatar Bar */}
          {phase === 'debate' ? (
            <BullBearArena
              agents={agents}
              messages={messages}
              activeAgents={getActiveAgents()}
            />
          ) : (
            <CouncilAvatarBar
              agents={agents}
              messages={messages}
              activeAgents={getActiveAgents()}
            />
          )}

          <Grid container spacing={3} sx={{ mb: 3 }}>
            {/* Council Progress */}
            <Grid item xs={12} lg={5}>
            <Box
              sx={{
                background: 'rgba(255, 255, 255, 0.02)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: 3,
                p: 3,
              }}
            >
              <CouncilProgress
                phase={phase}
                agents={agents}
                messages={messages}
                activeAgents={getActiveAgents()}
              />
            </Box>
          </Grid>

          {/* Live Activity Feed */}
          <Grid item xs={12} lg={7}>
            <Box
              sx={{
                background: 'rgba(255, 255, 255, 0.02)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: 3,
                height: 700,
                overflow: 'hidden',
                position: 'relative',
              }}
            >
              <LiveActivityFeed
                messages={messages}
                agents={agents}
                activeAgents={getActiveAgents()}
              />
            </Box>
          </Grid>
          </Grid>
        </Box>
      )}

      {/* Council Progress + Live Activity Feed (when decision is available) */}
      {activeTab === 'chamber' && decision && (
        <Box>
          {/* Show final Bull vs Bear Arena after debate completes */}
          <BullBearArena
            agents={agents}
            messages={messages}
            activeAgents={[]}
          />

          <Grid container spacing={3} sx={{ mb: 3 }}>
            {/* Council Progress (completed state) */}
            <Grid item xs={12} lg={5}>
            <Box
              sx={{
                background: 'rgba(255, 255, 255, 0.02)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: 3,
                p: 3,
              }}
            >
              <CouncilProgress
                phase="completed"
                agents={agents}
                messages={messages}
                activeAgents={[]}
              />
            </Box>
          </Grid>

          {/* Live Activity Feed (all messages) */}
          <Grid item xs={12} lg={7}>
            <Box
              sx={{
                background: 'rgba(255, 255, 255, 0.02)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: 3,
                height: 700,
                overflow: 'hidden',
                position: 'relative',
              }}
            >
              <LiveActivityFeed
                messages={messages}
                agents={agents}
                activeAgents={[]}
              />
            </Box>
          </Grid>
          </Grid>
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

    </Box>
  );
};

export default DebateViewer;
