/**
 * Type definitions for VC Council application
 */

export interface Agent {
  id: string;
  name: string;
  color: string;
}

export interface AgentMessage {
  agent: string;
  message: string;
  timestamp: string;
  phase: 'research' | 'debate' | 'decision';
}

export interface CompanyData {
  company_name: string;
  website?: string;
  industry?: string;
  product_description?: string;
  founder_github?: string;
  financial_metrics?: {
    arpu?: number;
    gross_margin?: number;
    cac?: number;
    monthly_burn?: number;
    active_users?: number;
  };
}

export interface Decision {
  decision: 'PASS' | 'MAYBE' | 'INVEST';
  reasoning: string;
  investment_memo: string;
  calendar_events: CalendarEvent[];
}

export interface CalendarEvent {
  title: string;
  start_time: string;
  end_time: string;
  attendees: string[];
  description: string;
}

export interface WebSocketMessage {
  type: 'phase_change' | 'agent_message' | 'decision' | 'error';
  data: any;
}

