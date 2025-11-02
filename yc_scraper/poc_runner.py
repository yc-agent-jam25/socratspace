#!/usr/bin/env python3
"""
POC Runner for Multi-Agent System with Date-Aware Fast Research.

This is a LITE version optimized for speed:
- Only uses info available BEFORE YC batch date
- Makes fast decisions
- Integrates with multi-modal setup
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fast_date_aware_research import FastDateAwareResearcher


class LiteMultiAgentPOC:
    """Lite POC version of multi-agent system - optimized for speed."""
    
    def __init__(self):
        """Initialize POC runner."""
        self.researcher = FastDateAwareResearcher()
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string."""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except:
                return None
    
    def analyze_company_fast(self, company: Dict, research_data: Dict) -> Dict:
        """
        Fast analysis based on pre-YC information only.
        
        Returns: {
            'decision': 'INVEST' | 'PASS' | 'MAYBE',
            'confidence': 0.0-1.0,
            'reasoning': '...',
            'risk_factors': [...],
            'positive_signals': [...],
        }
        """
        # Extract cutoff date
        cutoff_date = self.parse_date(company.get('yc_batch_date'))
        
        # Get research data (already filtered to pre-cutoff)
        website = research_data.get('website', {})
        founders = research_data.get('founders', {})
        product = research_data.get('product', {})
        pre_yc_funding = research_data.get('pre_yc_funding', {})
        
        # Fast decision logic (lite version)
        risk_score = 0
        positive_score = 0
        risk_factors = []
        positive_signals = []
        
        # Risk factors (negative signals)
        if not website.get('active', False):
            risk_score += 0.3
            risk_factors.append('Website not active before YC')
        
        if not founders.get('founders_checked', 0):
            risk_score += 0.1
            risk_factors.append('No founder info available')
        
        if not product.get('product_description'):
            risk_score += 0.2
            risk_factors.append('No product description')
        
        # Positive signals
        if product.get('founding_year'):
            founding_year = product['founding_year']
            if cutoff_date and founding_year:
                # Company existed before YC (shows traction)
                if founding_year < cutoff_date.year:
                    positive_score += 0.3
                    positive_signals.append(f'Founded in {founding_year} (before YC)')
        
        if website.get('active', False):
            positive_score += 0.2
            positive_signals.append('Website active before YC')
        
        if founders.get('founders_checked', 0) > 0:
            positive_score += 0.1
            positive_signals.append('Founder info available')
        
        # Decision logic
        net_score = positive_score - risk_score
        
        if net_score >= 0.2:
            decision = 'INVEST'
            confidence = min(0.9, 0.5 + abs(net_score))
        elif net_score <= -0.2:
            decision = 'PASS'
            confidence = min(0.9, 0.5 + abs(net_score))
        else:
            decision = 'MAYBE'
            confidence = 0.4
        
        return {
            'decision': decision,
            'confidence': round(confidence, 2),
            'reasoning': f'Net score: {net_score:.2f} (pos: {positive_score:.2f}, risk: {risk_score:.2f})',
            'risk_factors': risk_factors,
            'positive_signals': positive_signals,
            'net_score': round(net_score, 2),
        }
    
    async def run_poc(self, test_companies_file: str = "poc_test_companies.json") -> Dict:
        """
        Run POC on test companies.
        
        Returns evaluation results.
        """
        # Load test companies
        with open(test_companies_file, 'r') as f:
            data = json.load(f)
        
        companies = data['companies']
        
        print("="*80)
        print("LITE MULTI-AGENT POC - DATE-AWARE FAST MODE")
        print("="*80)
        print(f"Companies to analyze: {len(companies)}")
        print(f"Mode: FAST (lower quality, date-aware)")
        print()
        
        results = []
        
        for i, company in enumerate(companies, 1):
            company_name = company['company_name']
            expected_outcome = company.get('expected_outcome', 'unknown')
            label = company.get('label', 'unknown')
            
            print(f"[{i}/{len(companies)}] {company_name}")
            print(f"  Expected: {label.upper()} | Cutoff: {company.get('yc_batch_date', 'N/A')}")
            
            # Fast research (pre-YC info only)
            research_data = self.researcher.research_company(company)
            
            # Fast analysis
            analysis = self.analyze_company_fast(company, research_data)
            
            # Compare to expected
            is_correct = False
            if label == 'failed':
                is_correct = analysis['decision'] in ['PASS', 'MAYBE']
            elif label == 'successful':
                is_correct = analysis['decision'] in ['INVEST', 'MAYBE']
            
            result = {
                'company_name': company_name,
                'yc_batch': company.get('yc_batch', 'N/A'),
                'yc_batch_date': company.get('yc_batch_date', 'N/A'),
                'expected_label': label,
                'expected_outcome': expected_outcome,
                'decision': analysis['decision'],
                'confidence': analysis['confidence'],
                'reasoning': analysis['reasoning'],
                'risk_factors': analysis['risk_factors'],
                'positive_signals': analysis['positive_signals'],
                'net_score': analysis['net_score'],
                'correct': is_correct,
                'research_data': research_data,
            }
            
            results.append(result)
            
            status_icon = "✅" if is_correct else "❌"
            print(f"  Decision: {analysis['decision']} (confidence: {analysis['confidence']:.2f})")
            print(f"  {status_icon} {'Correct' if is_correct else 'Incorrect'} prediction")
            print()
        
        # Calculate metrics
        total = len(results)
        correct = sum(1 for r in results if r['correct'])
        accuracy = correct / total if total > 0 else 0
        
        failed_companies = [r for r in results if r['expected_label'] == 'failed']
        successful_companies = [r for r in results if r['expected_label'] == 'successful']
        
        failed_correct = sum(1 for r in failed_companies if r['correct'])
        successful_correct = sum(1 for r in successful_companies if r['correct'])
        
        failed_accuracy = failed_correct / len(failed_companies) if failed_companies else 0
        successful_accuracy = successful_correct / len(successful_companies) if successful_companies else 0
        
        print("="*80)
        print("POC RESULTS")
        print("="*80)
        print(f"Total Accuracy: {correct}/{total} ({accuracy*100:.1f}%)")
        print(f"\nFailed Companies:")
        print(f"  Accuracy: {failed_correct}/{len(failed_companies)} ({failed_accuracy*100:.1f}%)")
        print(f"\nSuccessful Companies:")
        print(f"  Accuracy: {successful_correct}/{len(successful_companies)} ({successful_accuracy*100:.1f}%)")
        print()
        
        # Decision breakdown
        decisions = {}
        for r in results:
            dec = r['decision']
            decisions[dec] = decisions.get(dec, 0) + 1
        
        print("Decision Breakdown:")
        for decision, count in sorted(decisions.items()):
            print(f"  {decision}: {count}")
        
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
        }
    
    def close(self):
        """Close resources."""
        self.researcher.close()


async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run POC on test companies")
    parser.add_argument('--input', type=str, default='poc_test_companies.json',
                       help='Input test companies file')
    parser.add_argument('--output', type=str, default='poc_results.json',
                       help='Output results file')
    
    args = parser.parse_args()
    
    poc = LiteMultiAgentPOC()
    
    try:
        results = await poc.run_poc(args.input)
        
        # Save results
        output_data = {
            'description': 'POC Results - Lite Multi-Agent System',
            'generated_at': datetime.now().isoformat(),
            'metrics': {
                'total_accuracy': results['accuracy'],
                'failed_accuracy': results['failed']['accuracy'],
                'successful_accuracy': results['successful']['accuracy'],
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
        
    finally:
        poc.close()


if __name__ == "__main__":
    asyncio.run(main())

