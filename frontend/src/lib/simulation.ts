/**
 * Simulation service for auto-progression through debate phases
 */

import type { Phase, AgentMessage, Decision } from './types';
import { generateMockMessages, getMockDecision } from './mockData';

export type SimulationCallback = {
  onPhaseChange: (phase: Phase) => void;
  onMessage: (message: AgentMessage) => void;
  onDecision: (decision: Decision) => void;
  onComplete: () => void;
};

class SimulationService {
  private timers: ReturnType<typeof setTimeout>[] = [];
  private isRunning = false;
  private callbacks: SimulationCallback | null = null;

  // Agent IDs for each phase
  private researchAgents = [
    'market_researcher',
    'founder_evaluator',
    'product_critic',
    'financial_analyst',
    'risk_assessor'
  ];

  private debateAgents = ['bull_agent', 'bear_agent'];

  private decisionAgent = 'lead_partner';

  /**
   * Start the simulation
   */
  start(callbacks: SimulationCallback) {
    if (this.isRunning) {
      this.stop();
    }

    this.isRunning = true;
    this.callbacks = callbacks;

    // Start with research phase
    this.callbacks.onPhaseChange('research');
    this.simulateResearchPhase();
  }

  /**
   * Stop the simulation and clear all timers
   */
  stop() {
    this.isRunning = false;
    this.timers.forEach(timer => clearTimeout(timer));
    this.timers = [];
  }

  /**
   * Reset the simulation
   */
  reset() {
    this.stop();
    this.callbacks = null;
  }

  /**
   * Simulate the research phase (0-8 seconds)
   * 5 research agents working in parallel
   */
  private simulateResearchPhase() {
    if (!this.isRunning || !this.callbacks) return;

    const phaseDuration = 8000; // 8 seconds
    const messagesPerAgent = 3;

    // Emit messages from each research agent
    this.researchAgents.forEach((agentId, agentIndex) => {
      const messages = generateMockMessages(agentId, messagesPerAgent);
      
      messages.forEach((message, msgIndex) => {
        const delay = (agentIndex * 400) + (msgIndex * 1800); // Stagger messages
        
        if (delay < phaseDuration) {
          const timer = setTimeout(() => {
            if (this.callbacks && this.isRunning) {
              this.callbacks.onMessage({
                ...message,
                timestamp: Date.now()
              });
            }
          }, delay);
          
          this.timers.push(timer);
        }
      });
    });

    // Transition to debate phase after research completes
    const timer = setTimeout(() => {
      if (this.callbacks && this.isRunning) {
        this.callbacks.onPhaseChange('debate');
        this.simulateDebatePhase();
      }
    }, phaseDuration);
    
    this.timers.push(timer);
  }

  /**
   * Simulate the debate phase (8-16 seconds)
   * Bull and Bear agents arguing
   */
  private simulateDebatePhase() {
    if (!this.isRunning || !this.callbacks) return;

    const phaseDuration = 7000; // 7 seconds
    const messagesPerAgent = 3;

    // Bull and Bear take turns
    this.debateAgents.forEach((agentId, agentIndex) => {
      const messages = generateMockMessages(agentId, messagesPerAgent);
      
      messages.forEach((message, msgIndex) => {
        const delay = (msgIndex * 2000) + (agentIndex * 800); // Alternate turns
        
        if (delay < phaseDuration) {
          const timer = setTimeout(() => {
            if (this.callbacks && this.isRunning) {
              this.callbacks.onMessage({
                ...message,
                timestamp: Date.now()
              });
            }
          }, delay);
          
          this.timers.push(timer);
        }
      });
    });

    // Transition to decision phase
    const timer = setTimeout(() => {
      if (this.callbacks && this.isRunning) {
        this.callbacks.onPhaseChange('decision');
        this.simulateDecisionPhase();
      }
    }, phaseDuration);
    
    this.timers.push(timer);
  }

  /**
   * Simulate the decision phase (16-20 seconds)
   * Lead Partner makes final decision
   */
  private simulateDecisionPhase() {
    if (!this.isRunning || !this.callbacks) return;

    const messages = generateMockMessages(this.decisionAgent, 3);

    // Emit decision agent messages
    messages.forEach((message, index) => {
      const timer = setTimeout(() => {
        if (this.callbacks && this.isRunning) {
          this.callbacks.onMessage({
            ...message,
            timestamp: Date.now()
          });
        }
      }, index * 1500);
      
      this.timers.push(timer);
    });

    // Final decision after 4.5 seconds
    const decisionTimer = setTimeout(() => {
      if (this.callbacks && this.isRunning) {
        // Randomly select decision type (weighted towards INVEST for demo)
        const rand = Math.random();
        const decisionType = rand < 0.6 ? 'INVEST' : rand < 0.85 ? 'MAYBE' : 'PASS';
        
        const decision = getMockDecision(decisionType);
        this.callbacks.onDecision(decision);
        this.callbacks.onPhaseChange('completed');
        this.callbacks.onComplete();
        this.isRunning = false;
      }
    }, 4500);
    
    this.timers.push(decisionTimer);
  }
}

// Export singleton instance
export const simulationService = new SimulationService();

