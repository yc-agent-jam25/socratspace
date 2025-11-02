/**
 * API client for backend communication
 * Currently mocked for frontend-only development
 */

import type { CompanyData } from './types';

// API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Real API client - connected to backend
 */
export const api = {
  /**
   * Start a new investment analysis
   */
  startAnalysis: async (companyData: CompanyData): Promise<{ session_id: string; status: string; message: string }> => {
    const response = await fetch(`${API_URL}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(companyData)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  /**
   * Get analysis status and results
   */
  getAnalysisStatus: async (sessionId: string): Promise<any> => {
    const response = await fetch(`${API_URL}/api/analysis/${sessionId}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
};

// Mock implementation (disabled):
/*
export const api = {
  startAnalysis: async (companyData: CompanyData): Promise<{ session_id: string; status: string; message: string }> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    return {
      session_id: sessionId,
      status: 'started',
      message: `Analysis started for ${companyData.company_name}`
    };
  },
  getAnalysisStatus: async (sessionId: string): Promise<any> => {
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
*/

