/**
 * Main Application Component
 * Socrat Space - AI Investment Intelligence
 */

import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { Container, Box, Fade } from '@mui/material';
import { theme } from './theme';
import ErrorBoundary from './components/ErrorBoundary';
import LandingPage from './components/landing/LandingPage';
import InputFormEnhanced from './components/InputFormEnhanced';
import DebateViewer from './components/DebateViewer';
import type { CompanyData } from './lib/types';

type AppView = 'landing' | 'input' | 'analysis';

function App() {
  const [view, setView] = useState<AppView>('landing');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [companyData, setCompanyData] = useState<CompanyData | null>(null);

  const handleGetStarted = () => {
    setView('input');
  };

  const handleAnalysisStart = (session: string, data: CompanyData) => {
    setSessionId(session);
    setCompanyData(data);
    setView('analysis');
  };

  const handleReset = () => {
    setView('landing');
    setSessionId(null);
    setCompanyData(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <ErrorBoundary>
        <Box 
          sx={{ 
            minHeight: '100vh', 
            position: 'relative',
            zIndex: 1,
          }}
        >
          {/* Landing Page */}
          {view === 'landing' && (
            <Fade in timeout={600}>
              <Box>
                <LandingPage onGetStarted={handleGetStarted} />
              </Box>
            </Fade>
          )}

          {/* Input Form */}
          {view === 'input' && (
            <Fade in timeout={600}>
              <Container maxWidth="xl">
                <Box sx={{ py: 8 }}>
                  <InputFormEnhanced onAnalysisStart={handleAnalysisStart} />
                </Box>
              </Container>
            </Fade>
          )}

          {/* Analysis View */}
          {view === 'analysis' && sessionId && companyData && (
            <Fade in timeout={600}>
              <Container maxWidth="xl">
                <Box sx={{ py: 4 }}>
                  <DebateViewer
                    sessionId={sessionId}
                    companyData={companyData}
                    onReset={handleReset}
                  />
                </Box>
              </Container>
            </Fade>
          )}
        </Box>
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;
