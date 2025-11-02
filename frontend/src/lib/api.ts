/**
 * API client for backend communication
 * Currently mocked for frontend-only development
 */

import type { CompanyData } from './types';

// API_URL will be used when connecting to real backend
// Using import.meta.env directly when needed instead of storing in constant

/**
 * Mock API client - will be replaced with real implementation
 */
export const api = {
  /**
   * Start a new investment analysis
   */
  startAnalysis: async (companyData: CompanyData): Promise<{ session_id: string; status: string; message: string }> => {
    // Mock implementation - simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    return {
      session_id: sessionId,
      status: 'started',
      message: `Analysis started for ${companyData.company_name}`
    };
  },

  /**
   * Get analysis status and results
   */
  getAnalysisStatus: async (sessionId: string): Promise<any> => {
    // Mock implementation
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return {
      session_id: sessionId,
      status: 'running',
      company_data: {},
      result: null,
      error: null
    };
  }
};

// For future real implementation:
/*
export const api = {
  startAnalysis: async (companyData: CompanyData) => {
    const response = await fetch(`${API_URL}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(companyData)
    });
    return response.json();
  },

  getAnalysisStatus: async (sessionId: string) => {
    const response = await fetch(`${API_URL}/api/analysis/${sessionId}`);
    return response.json();
  }
};
*/

