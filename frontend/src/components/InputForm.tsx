/**
 * Company Input Form Component
 * Collects company information before starting analysis
 */

import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Stack,
  Alert,
  CircularProgress
} from '@mui/material';
import type { CompanyData } from '../lib/types';
import { api } from '../lib/api';

interface InputFormProps {
  onAnalysisStart: (sessionId: string, companyData: CompanyData) => void;
}

const InputForm: React.FC<InputFormProps> = ({ onAnalysisStart }) => {
  const [formData, setFormData] = useState<CompanyData>({
    company_name: '',
    website: '',
    founder_github: '',
    industry: '',
    product_description: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateUrl = (url: string): boolean => {
    if (!url) return true; // Optional field
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!formData.company_name?.trim()) {
      setError('Company name is required');
      return;
    }

    if (!formData.website?.trim()) {
      setError('Website URL is required');
      return;
    }

    if (!validateUrl(formData.website)) {
      setError('Please enter a valid website URL (e.g., https://example.com)');
      return;
    }

    setLoading(true);

    try {
      const response = await api.startAnalysis(formData);
      onAnalysisStart(response.session_id, formData);
    } catch (err: any) {
      setError(err.message || 'Failed to start analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof CompanyData) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }));
  };

  return (
    <Box
      sx={{ 
        p: 4, 
        maxWidth: 800, 
        mx: 'auto',
        animation: 'fadeInUp 0.6s ease-out',
        background: 'rgba(255, 255, 255, 0.06)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: 3,
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
      }}
    >
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Company Information
      </Typography>

      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Enter the details of the company you want to analyze. Our 8 AI agents will conduct 
        comprehensive research and debate the investment decision.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        <Stack spacing={3}>
          <TextField
            required
            label="Company Name"
            value={formData.company_name}
            onChange={handleChange('company_name')}
            fullWidth
            placeholder="e.g., AI Safety Labs"
            disabled={loading}
          />

          <TextField
            required
            label="Website URL"
            type="url"
            value={formData.website}
            onChange={handleChange('website')}
            fullWidth
            placeholder="https://example.com"
            disabled={loading}
          />

          <TextField
            label="Founder GitHub Username"
            value={formData.founder_github}
            onChange={handleChange('founder_github')}
            fullWidth
            placeholder="e.g., johndoe"
            disabled={loading}
          />

          <TextField
            label="Industry"
            value={formData.industry}
            onChange={handleChange('industry')}
            fullWidth
            placeholder="e.g., AI Safety, FinTech, SaaS"
            disabled={loading}
          />

          <TextField
            label="Product Description"
            value={formData.product_description}
            onChange={handleChange('product_description')}
            fullWidth
            multiline
            rows={4}
            placeholder="Brief description of the product or service..."
            disabled={loading}
          />

          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={loading}
            fullWidth
            sx={{ 
              mt: 2,
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600
            }}
          >
            {loading ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} color="inherit" />
                Starting Analysis...
              </>
            ) : (
              'Start 8-Agent Analysis'
            )}
          </Button>
        </Stack>
      </form>
    </Box>
  );
};

export default InputForm;
