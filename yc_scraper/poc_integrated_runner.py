#!/usr/bin/env python3
"""
Integrated POC Runner - Connects to actual multi-agent system.

This runs your full multi-agent system on test companies with:
- Date-aware research (only pre-YC info)
- Fast execution mode
- Full 17-task analysis
- Results comparison
"""

import json
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fast_date_aware_research import FastDateAwareResearcher

# Import orchestrator
try:
    from backend.services.crew_orchestrator import VCCouncilOrchestrator
    from backend.api.sse import sse_manager
except ImportError:
    # Try alternate import paths
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
        from services.crew_orchestrator import VCCouncilOrchestrator
        from api.sse import sse_manager
    except ImportError as e:
        print(f"❌ Error importing orchestrator: {e}")
        print("   Make sure you're running from the project root")
        sys.exit(1)


class IntegratedPOCRunner:
    """POC runner integrated with actual multi-agent system."""
    
    def __init__(self):
        """Initialize runner."""
        self.researcher = FastDateAwareResearcher()
        self.orchestrator = VCCouncilOrchestrator()
        self.results_cache = {}
    
    def prepare_company_data(self, company: Dict, research_data: Dict) -> Dict:
        """
        Prepare company data for multi-agent system.
        
        Only includes information available BEFORE yc_batch_date.
        """
        cutoff_date = self.researcher.parse_date(company.get('yc_batch_date'))
        
        # Build company data dict for orchestrator
        company_data = {
            'company_name': company.get('company_name', ''),
            'website': company.get('website', ''),
            'product_description': company.get('product_description', company.get('description', '')),
            'industry': None,  # Extract from tags if available
            'founder_github': None,  # Would need to research
            'financial_metrics': None,  # Would need to research (pre-YC only)
        }
        
        # Add founder info if available (pre-YC)
        founders = company.get('founders', [])
        if founders:
            company_data['founders'] = founders
            company_data['founder_names'] = ', '.join(founders)
        
        # Add date constraint info
        if cutoff_date:
            company_data['_cutoff_date'] = cutoff_date.isoformat()
            company_data['_research_note'] = f"Only use information available before {cutoff_date.strftime('%Y-%m-%d')}"
        
        # Add research data (pre-YC info)
        company_data['_research_data'] = {
            'website_status': research_data.get('website', {}),
            'founders_info': research_data.get('founders', {}),
            'product_info': research_data.get('product', {}),
        }
        
        return company_data
    
    async def analyze_with_multi_agent(self, company: Dict, research_data: Dict) -> Dict:
        """
        Run full multi-agent analysis on a company.
        
        Returns decision and analysis result.
        """
        company_name = company.get('company_name', 'unknown')
        
        # Prepare company data
        company_data = self.prepare_company_data(company, research_data)
        
        print(f"  🤖 Starting multi-agent analysis for {company_name}...")
        
        try:
            # Start analysis (returns session_id)
            session_id = await self.orchestrator.start_analysis(company_data)
            
            # Wait for analysis to complete (poll for result)
            max_wait = 600  # 10 minutes max
            wait_interval = 2  # Check every 2 seconds
            elapsed = 0
            
            while elapsed < max_wait:
                await asyncio.sleep(wait_interval)
                elapsed += wait_interval
                
                # Check if analysis is complete
                session = self.orchestrator.sessions.get(session_id)
                if not session:
                    break
                
                if session.get('status') == 'completed':
                    result = session.get('result')
                    if result:
                        # Extract decision from result
                        decision = self.extract_decision(result)
                        print(f"  ✅ Analysis complete: {decision}")
                        return {
                            'decision': decision,
                            'result': result,
                            'session_id': session_id,
                            'analysis_time': elapsed,
                        }
                
                if session.get('status') == 'error':
                    error = session.get('error', 'Unknown error')
                    print(f"  ❌ Analysis error: {error}")
                    return {
                        'decision': 'ERROR',
                        'error': error,
                        'session_id': session_id,
                    }
            
            # Timeout
            print(f"  ⏱️  Analysis timed out after {max_wait}s")
            return {
                'decision': 'TIMEOUT',
                'error': 'Analysis did not complete in time',
                'session_id': session_id,
            }
            
        except Exception as e:
            print(f"  ❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            return {
                'decision': 'ERROR',
                'error': str(e),
            }
    
    def extract_decision(self, result: any) -> str:
        """Extract decision from analysis result."""
        if isinstance(result, dict):
            return result.get('decision', 'UNKNOWN')
        elif hasattr(result, 'decision'):
            return result.decision
        elif hasattr(result, 'model_dump'):
            return result.model_dump().get('decision', 'UNKNOWN')
        elif hasattr(result, 'dict'):
            return result.dict().get('decision', 'UNKNOWN')
        else:
            # Try to parse as JSON string
            try:
                if isinstance(result, str):
                    parsed = json.loads(result)
                    return parsed.get('decision', 'UNKNOWN')
            except:
                pass
        
        return 'UNKNOWN'
    
    async def run_poc(self, test_companies_file: str = "poc_test_companies.json") -> Dict:
        """Run full POC with integrated multi-agent system."""
        
        # Load test companies
        with open(test_companies_file, 'r') as f:
            data = json.load(f)
        
        companies = data['companies']
        
        print("="*80)
        print("INTEGRATED MULTI-AGENT POC RUNNER")
        print("="*80)
        print(f"Companies to analyze: {len(companies)}")
        print(f"Mode: FULL multi-agent system (17 tasks, 8 agents)")
        print(f"Date-aware: Only using pre-YC information")
        print()
        
        results = []
        
        for i, company in enumerate(companies, 1):
            company_name = company['company_name']
            expected_label = company.get('label', 'unknown')
            cutoff_date = company.get('yc_batch_date', 'N/A')
            
            print(f"[{i}/{len(companies)}] {company_name}")
            print(f"  Expected: {expected_label.upper()} | Cutoff: {cutoff_date}")
            
            # Fast research (pre-YC info only)
            print(f"  🔍 Researching (pre-YC info only)...")
            research_data = self.researcher.research_company(company)
            
            # Run full multi-agent analysis
            analysis_result = await self.analyze_with_multi_agent(company, research_data)
            
            # Compare to expected
            decision = analysis_result.get('decision', 'UNKNOWN')
            is_correct = False
            
            if expected_label == 'failed':
                is_correct = decision in ['PASS', 'MAYBE']  # Correctly identified as failed
            elif expected_label == 'successful':
                is_correct = decision in ['INVEST', 'MAYBE']  # Correctly identified as successful
            
            result = {
                'company_name': company_name,
                'yc_batch': company.get('yc_batch', 'N/A'),
                'yc_batch_date': cutoff_date,
                'expected_label': expected_label,
                'decision': decision,
                'confidence': analysis_result.get('confidence', None),
                'is_correct': is_correct,
                'analysis_time': analysis_result.get('analysis_time', None),
                'analysis_result': analysis_result,
                'research_data': research_data,
            }
            
            results.append(result)
            
            status_icon = "✅" if is_correct else "❌"
            print(f"  {status_icon} Prediction: {decision} | Expected: {expected_label}")
            print()
        
        # Calculate metrics
        total = len(results)
        correct = sum(1 for r in results if r['is_correct'])
        accuracy = correct / total if total > 0 else 0
        
        failed_companies = [r for r in results if r['expected_label'] == 'failed']
        successful_companies = [r for r in results if r['expected_label'] == 'successful']
        
        failed_correct = sum(1 for r in failed_companies if r['is_correct'])
        successful_correct = sum(1 for r in successful_companies if r['is_correct'])
        
        failed_accuracy = failed_correct / len(failed_companies) if failed_companies else 0
        successful_accuracy = successful_correct / len(successful_companies) if successful_companies else 0
        
        # Decision breakdown
        decisions = {}
        for r in results:
            dec = r['decision']
            decisions[dec] = decisions.get(dec, 0) + 1
        
        print("="*80)
        print("POC RESULTS - FULL MULTI-AGENT SYSTEM")
        print("="*80)
        print(f"Total Accuracy: {correct}/{total} ({accuracy*100:.1f}%)")
        print(f"\nFailed Companies:")
        print(f"  Accuracy: {failed_correct}/{len(failed_companies)} ({failed_accuracy*100:.1f}%)")
        print(f"\nSuccessful Companies:")
        print(f"  Accuracy: {successful_correct}/{len(successful_companies)} ({successful_accuracy*100:.1f}%)")
        print(f"\nDecision Breakdown:")
        for decision, count in sorted(decisions.items()):
            print(f"  {decision}: {count}")
        
        # Average analysis time
        avg_time = sum(r.get('analysis_time', 0) for r in results if r.get('analysis_time')) / len([r for r in results if r.get('analysis_time')])
        if avg_time:
            print(f"\nAverage Analysis Time: {avg_time:.1f}s per company")
        
        return {
            'total': total,
            'correct': correct,
            'accuracy': accuracy,
            'failed': {
                'total': len(failed_companies),
                'correct': failed_correct,
                'accuracy': failed_accuracy,
            },
            'successful': {
                'total': len(successful_companies),
                'correct': successful_correct,
                'accuracy': successful_accuracy,
            },
            'decisions': decisions,
            'results': results,
            'avg_analysis_time': avg_time,
        }
    
    def close(self):
        """Close resources."""
        self.researcher.close()


async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run integrated POC with multi-agent system")
    parser.add_argument('--input', type=str, default='poc_test_companies.json',
                       help='Input test companies file')
    parser.add_argument('--output', type=str, default='poc_integrated_results.json',
                       help='Output results file')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of companies (for testing)')
    
    args = parser.parse_args()
    
    # Load and optionally limit companies
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    if args.limit:
        data['companies'] = data['companies'][:args.limit]
        print(f"⚠️  Limited to {args.limit} companies for testing")
    
    # Save limited version if needed
    if args.limit:
        temp_file = 'poc_test_companies_limited.json'
        with open(temp_file, 'w') as f:
            json.dump(data, f)
        args.input = temp_file
    
    runner = IntegratedPOCRunner()
    
    try:
        results = await runner.run_poc(args.input)
        
        # Save results
        output_data = {
            'description': 'Integrated POC Results - Full Multi-Agent System',
            'generated_at': datetime.now().isoformat(),
            'metrics': {
                'total_accuracy': results['accuracy'],
                'failed_accuracy': results['failed']['accuracy'],
                'successful_accuracy': results['successful']['accuracy'],
                'avg_analysis_time': results.get('avg_analysis_time', 0),
            },
            'summary': {
                'total': results['total'],
                'correct': results['correct'],
                'decisions': results['decisions'],
            },
            'detailed_results': results['results'],
        }
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Results saved to {args.output}")
        print(f"\n✅ POC Complete!")
        
    finally:
        runner.close()


if __name__ == "__main__":
    asyncio.run(main())

