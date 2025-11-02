#!/usr/bin/env python3
"""
Test your multi-agent investment analysis system against W20 outcomes.

This script:
1. Loads the test dataset
2. Runs your multi-agent system on each company
3. Compares predictions to actual outcomes
4. Calculates accuracy metrics
"""

import json
from pathlib import Path
from typing import Dict, List


def test_multi_agent_system(test_dataset_file: str = "test_dataset_w20.json"):
    """
    Test your multi-agent system against ground truth outcomes.
    
    Args:
        test_dataset_file: Path to test dataset JSON
    
    Returns:
        Dict with test results and metrics
    """
    
    # Load test dataset
    dataset_path = Path(test_dataset_file)
    if not dataset_path.exists():
        print(f"❌ Test dataset not found: {test_dataset_file}")
        print("   Run: python create_test_dataset.py first")
        return None
    
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    
    companies = dataset.get('companies', [])
    print(f"\n📊 Testing on {len(companies)} companies from {dataset.get('batch', 'W20')}")
    
    # Test results
    results = []
    
    for i, company in enumerate(companies, 1):
        company_name = company['company_name']
        input_data = company['input_data']
        outcome = company['outcome']
        
        print(f"\n[{i}/{len(companies)}] Testing: {company_name}")
        
        # ============================================
        # TODO: Replace this with your actual system
        # ============================================
        # Your multi-agent system should be called like:
        # decision = your_multi_agent_system.analyze(input_data)
        # For now, using placeholder
        
        # PLACEHOLDER - Replace with your system
        decision = "INVEST"  # This should come from your multi-agent system
        
        # Determine if company is actually successful
        is_successful = (
            outcome.get('further_funding', False) or
            outcome.get('acquired', False) or
            outcome.get('ipo', False) or
            outcome.get('status') in ['active', 'funded']
        )
        
        # Compare prediction to reality
        correct = (
            (decision == "INVEST" and is_successful) or
            (decision == "PASS" and not is_successful) or
            (decision == "MAYBE" and True)  # MAYBE is neutral
        )
        
        result = {
            'company': company_name,
            'predicted': decision,
            'actual_status': outcome.get('status', 'unknown'),
            'actually_successful': is_successful,
            'correct': correct,
            'outcome_details': outcome,
        }
        
        results.append(result)
        
        # Print result
        status_icon = "✅" if correct else "❌"
        print(f"  Prediction: {decision}")
        print(f"  Reality: {outcome.get('status')} (successful: {is_successful})")
        print(f"  {status_icon} {'Correct' if correct else 'Incorrect'}")
    
    # Calculate metrics
    total = len(results)
    correct_predictions = sum(1 for r in results if r['correct'])
    accuracy = correct_predictions / total if total > 0 else 0
    
    # Precision: Of companies you said "INVEST", how many actually succeeded?
    invest_predictions = [r for r in results if r['predicted'] == "INVEST"]
    invest_correct = sum(1 for r in invest_predictions if r['actually_successful'])
    precision = invest_correct / len(invest_predictions) if invest_predictions else 0
    
    # Recall: Of companies that actually succeeded, how many did you identify?
    actually_successful = [r for r in results if r['actually_successful']]
    successful_identified = sum(1 for r in actually_successful if r['predicted'] == "INVEST")
    recall = successful_identified / len(actually_successful) if actually_successful else 0
    
    # False Positive Rate
    false_positives = sum(1 for r in invest_predictions if not r['actually_successful'])
    false_positive_rate = false_positives / len(invest_predictions) if invest_predictions else 0
    
    # Print summary
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"\n📊 Metrics:")
    print(f"   Total companies tested: {total}")
    print(f"   Correct predictions: {correct_predictions}")
    print(f"   Accuracy: {accuracy:.2%}")
    print(f"\n🎯 Precision (Investment Accuracy):")
    print(f"   Companies you said 'INVEST': {len(invest_predictions)}")
    print(f"   Actually successful: {invest_correct}")
    print(f"   Precision: {precision:.2%}")
    print(f"\n📈 Recall (Catch Rate):")
    print(f"   Actually successful companies: {len(actually_successful)}")
    print(f"   Identified correctly: {successful_identified}")
    print(f"   Recall: {recall:.2%}")
    print(f"\n⚠️  False Positive Rate:")
    print(f"   Failed companies you marked as 'good': {false_positives}")
    print(f"   False Positive Rate: {false_positive_rate:.2%}")
    
    # Save results
    results_file = "test_results_w20.json"
    with open(results_file, 'w') as f:
        json.dump({
            'metrics': {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'false_positive_rate': false_positive_rate,
            },
            'results': results,
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to {results_file}")
    
    return {
        'metrics': {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'false_positive_rate': false_positive_rate,
        },
        'results': results,
    }


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test multi-agent system against W20 outcomes")
    parser.add_argument('--dataset', type=str, default='test_dataset_w20.json',
                       help='Test dataset file')
    
    args = parser.parse_args()
    
    print("="*60)
    print("Multi-Agent System Test")
    print("="*60)
    print("\n⚠️  NOTE: This script uses a placeholder for your multi-agent system.")
    print("   Replace the 'decision = ...' line with your actual system call.")
    print()
    
    test_multi_agent_system(args.dataset)


if __name__ == "__main__":
    main()

