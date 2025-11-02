/**
 * TypeScript type definitions for Socrat Space
 */

export interface CompanyData {
  company_name: string;
  website: string;
  founder_github?: string;
  industry?: string;
  product_description?: string;
}

export interface Agent {
  id: string;
  name: string;
  color: string;
}

export interface AgentMessage {
  agent: string;
  message: string;
  message_type: string;
  timestamp: number;
}

export interface CalendarEvent {
  title: string;
  start_time: string;
  end_time: string;
  attendees: string[];
  description: string;
}

export interface Decision {
  decision: 'PASS' | 'MAYBE' | 'INVEST';
  reasoning: string;
  investment_memo: string;
  calendar_events: CalendarEvent[];
}

export type Phase = 'idle' | 'research' | 'debate' | 'decision' | 'completed';

export interface WebSocketEvent {
  type: 'phase_change' | 'agent_message' | 'decision' | 'error';
  data: any;
}

export interface SimulationState {
  phase: Phase;
  messages: AgentMessage[];
  decision: Decision | null;
  isRunning: boolean;
  startTime: number | null;
}

export interface TimelineEvent {
  id: string;
  agent: string;
  message: string;
  timestamp: number;
  type: 'start' | 'message' | 'complete' | 'phase_change';
}

