#!/usr/bin/env python3
"""
Extract just company names from the rejected companies JSON file.
Simple extraction - just gets the 'name' field from each entry.
"""

import json
from pathlib import Path
from typing import List


def extract_names(input_file: str, output_file: str = None) -> List[str]:
    """
    Extract unique company names from the rejected companies JSON.
    
    Args:
        input_file: Path to rejected_companies_reddit.json (or similar)
        output_file: Optional output file (default: company_names_only.json)
    
    Returns:
        List of unique company names
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        return []
    
    print(f"📖 Reading {input_file}...")
    
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    # Handle different JSON structures
    if isinstance(data, list):
        companies = data
    elif isinstance(data, dict) and 'companies' in data:
        companies = data['companies']
    else:
        companies = [data] if isinstance(data, dict) else []
    
    # Extract unique names (simple - just get the name field)
    names = set()
    for item in companies:
        if isinstance(item, dict):
            name = item.get('name', '').strip()
            if name:
                names.add(name)
        elif isinstance(item, str):
            names.add(item.strip())
    
    unique_names = sorted(list(names))
    
    print(f"✅ Extracted {len(unique_names)} unique company names")
    
    # Save to output file
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(unique_names, f, indent=2)
        print(f"💾 Saved to {output_file}")
    else:
        # Default output file
        default_output = input_path.parent / "company_names_only.json"
        with open(default_output, 'w') as f:
            json.dump(unique_names, f, indent=2)
        print(f"💾 Saved to {default_output}")
    
    # Also save as simple text file (one name per line)
    txt_output = input_path.parent / "company_names.txt"
    with open(txt_output, 'w') as f:
        for name in unique_names:
            f.write(f"{name}\n")
    print(f"💾 Also saved as text file: {txt_output}")
    
    return unique_names


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract company names from rejected companies JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract names from default file
  python extract_company_names.py
  
  # Specify input file
  python extract_company_names.py rejected_companies_reddit.json
  
  # Custom output file
  python extract_company_names.py -i input.json -o output.json
        """
    )
    
    parser.add_argument('-i', '--input', type=str, 
                       default='rejected_companies_reddit.json',
                       help='Input JSON file with company data')
    parser.add_argument('-o', '--output', type=str, default=None,
                       help='Output JSON file (default: company_names_only.json)')
    
    args = parser.parse_args()
    
    names = extract_names(args.input, args.output)
    
    if names:
        print(f"\n📋 Sample names (first 20):")
        for name in names[:20]:
            print(f"  - {name}")
        if len(names) > 20:
            print(f"  ... and {len(names) - 20} more")
        print(f"\n💡 Tip: Review company_names.txt to see all names and filter manually")
    else:
        print("\n⚠️  No company names found")


if __name__ == "__main__":
    main()
