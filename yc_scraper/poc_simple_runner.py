#!/usr/bin/env python3
"""
Simplified POC Runner - Works directly with orchestrator.

This directly calls the orchestrator's _run_analysis method
without SSE dependencies for POC testing.
"""

import json
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict

# Add paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'backend'))

from fast_date_aware_research import FastDateAwareResearcher


class SimplePOCRunner:
    """Simplified POC runner that directly calls analysis."""
    
    def __init__(self):
        """Initialize runner."""
        self.researcher = FastDateAwareResearcher()
    
    def prepare_company_data(self, company: Dict, research_data: Dict) -> Dict:
        """Prepare company data for analysis."""
        company_data = {
            'company_name': company.get('company_name', ''),
            'website': company.get('website', ''),
            'product_description': company.get('product_description', company.get('description', '')),
            'industry': None,
            'founder_github': None,
            'financial_metrics': None,
        }
        
        # Add founders
        founders = company.get('founders', [])
        if founders:
            company_data['founders'] = founders
            company_data['founder_names'] = ', '.join(founders)
        
        # Add date constraint
        cutoff_date = self.researcher.parse_date(company.get('yc_batch_date'))
        if cutoff_date:
            company_data['_cutoff_date'] = cutoff_date.isoformat()
            company_data['_research_note'] = f"CRITICAL: Only use information available before {cutoff_date.strftime('%Y-%m-%d')}. Do not use any information from after this date."
        
        return company_data
    
    async def run_single_analysis(self, company: Dict) -> Dict:
        """Run analysis on a single company."""
        company_name = company.get('company_name', 'unknown')
        
        print(f"  🔍 Researching {company_name} (pre-YC info only)...")
        research_data = self.researcher.research_company(company)
        
        company_data = self.prepare_company_data(company, research_data)
        
        # Import here to handle module path issues
        try:
            # Try multiple import paths
            try:
                from backend.services.crew_orchestrator import VCCouncilOrchestrator
            except ImportError:
                try:
                    import sys
                    sys.path.insert(0, str(project_root))
                    from backend.services.crew_orchestrator import VCCouncilOrchestrator
                except ImportError:
                    import sys
                    sys.path.insert(0, str(project_root / 'backend'))
                    from services.crew_orchestrator import VCCouncilOrchestrator
        except ImportError as e:
            print(f"  ❌ Cannot import orchestrator: {e}")
            print("  ⚠️  Running in fast mode only (using simplified analysis)")
            # Fall back to fast analysis
            return self.run_fast_analysis(company, research_data)
        
        orchestrator = VCCouncilOrchestrator()
        
        # Create a mock session_id
        session_id = f"poc_{company_name.lower().replace(' ', '_')}"
        
        print(f"  🤖 Running multi-agent analysis...")
        
        try:
            # Directly run analysis (bypassing SSE)
            await orchestrator._run_analysis(session_id, company_data)
            
            # Get result
            session = orchestrator.sessions.get(session_id)
            if session and session.get('status') == 'completed':
                result = session.get('result', {})
                decision = result.get('decision', 'UNKNOWN') if isinstance(result, dict) else 'UNKNOWN'
                
                return {
                    'decision': decision,
                    'result': result,
                    'session_id': session_id,
                }
            else:
                error = session.get('error', 'Analysis failed') if session else 'Session not found'
                return {
                    'decision': 'ERROR',
                    'error': error,
                }
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {
                'decision': 'ERROR',
                'error': str(e),
            }
    
    async def run_poc(self, test_companies_file: str = "poc_test_companies.json", limit: int = None) -> Dict:
        """Run POC on all test companies."""
        
        # Load companies
        with open(test_companies_file, 'r') as f:
            data = json.load(f)
        
        companies = data['companies']
        if limit:
            companies = companies[:limit]
        
        print("="*80)
        print("INTEGRATED POC RUNNER - MULTI-AGENT SYSTEM")
        print("="*80)
        print(f"Companies: {len(companies)}")
        print()
        
        results = []
        
        for i, company in enumerate(companies, 1):
            company_name = company['company_name']
            expected_label = company.get('label', 'unknown')
            
            print(f"[{i}/{len(companies)}] {company_name}")
            print(f"  Expected: {expected_label.upper()}")
            
            analysis_result = await self.run_single_analysis(company)
            
            decision = analysis_result.get('decision', 'UNKNOWN')
            
            # Determine correctness
            is_correct = False
            if expected_label == 'failed':
                is_correct = decision in ['PASS', 'MAYBE']
            elif expected_label == 'successful':
                is_correct = decision in ['INVEST', 'MAYBE']
            
            result = {
                'company_name': company_name,
                'yc_batch': company.get('yc_batch', 'N/A'),
                'expected_label': expected_label,
                'decision': decision,
                'is_correct': is_correct,
                'analysis_result': analysis_result,
            }
            
            results.append(result)
            
            status = "✅" if is_correct else "❌"
            print(f"  {status} Decision: {decision} | Expected: {expected_label}")
            print()
        
        # Calculate metrics
        total = len(results)
        correct = sum(1 for r in results if r['is_correct'])
        accuracy = correct / total if total > 0 else 0
        
        print("="*80)
        print("RESULTS")
        print("="*80)
        print(f"Accuracy: {correct}/{total} ({accuracy*100:.1f}%)")
        
        return {
            'total': total,
            'correct': correct,
            'accuracy': accuracy,
            'results': results,
        }
    
    def run_fast_analysis(self, company: Dict, research_data: Dict) -> Dict:
        """Fast analysis fallback if orchestrator unavailable."""
        # Simple decision logic based on research
        website = research_data.get('website', {})
        founders = research_data.get('founders', {})
        
        if website.get('active') and founders.get('founders_checked', 0) > 0:
            decision = 'INVEST'
        elif not website.get('active'):
            decision = 'PASS'
        else:
            decision = 'MAYBE'
        
        return {
            'decision': decision,
            'mode': 'fast_fallback',
            'reasoning': 'Simplified analysis (orchestrator unavailable)',
        }
    
    def close(self):
        """Close resources."""
        self.researcher.close()


async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run integrated POC")
    parser.add_argument('--input', default='poc_test_companies.json')
    parser.add_argument('--output', default='poc_integrated_results.json')
    parser.add_argument('--limit', type=int, default=None)
    
    args = parser.parse_args()
    
    runner = SimplePOCRunner()
    
    try:
        results = await runner.run_poc(args.input, limit=args.limit)
        
        with open(args.output, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'metrics': results,
                'detailed_results': results['results'],
            }, f, indent=2)
        
        print(f"\n💾 Results saved to {args.output}")
        
    finally:
        runner.close()


if __name__ == "__main__":
    asyncio.run(main())

