#!/usr/bin/env python3
"""
Structured Credit Card Analyzer
Generates machine-readable output with tables, JSON, and ROI calculations
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from main import generate_content
from user_profile import SpendingProfile


class StructuredAnalyzer:
    """Analyze credit cards with structured output"""
    
    def __init__(self):
        self.analysis_results = []
    
    def analyze_with_profile(self, query: str, profile: SpendingProfile, model: str = "meta-llama/llama-3.2-3b-instruct:free"):
        """Generate analysis with user profile context"""
        
        # Build enhanced prompt with profile context
        enhanced_prompt = self._build_enhanced_prompt(query, profile)
        
        # Get AI response
        print(f"\n🔍 Analyzing with profile: {profile.name}")
        print(f"   Total spend: ₹{profile.get_total_monthly_spend():,.0f}/month")
        
        result = generate_content(enhanced_prompt, model, retry_fallback=True)
        
        if not result['success']:
            return result
        
        # Structure the output
        structured_data = self._structure_output(result, query, profile)
        
        # Save in multiple formats
        self._save_outputs(structured_data)
        
        return {
            'success': True,
            'structured_data': structured_data,
            'model_used': result['model_used']
        }
    
    def _build_enhanced_prompt(self, query: str, profile: SpendingProfile) -> str:
        """Build AI prompt with structured output requirements"""
        
        prompt = f"""You are a credit card expert analyzing Indian credit cards. Provide analysis in this EXACT structured format:

## PRIMARY RECOMMENDATION

**Card Name:** [Full card name]
**Bank:** [Bank name]
**Annual Fee:** ₹[amount]
**Best For:** [Primary use case]
**Reward Rate:** [X% or Y points per ₹100]

**Key Benefits:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**ROI Calculation:**
- Monthly Spend: ₹{profile.get_total_monthly_spend():,.0f}
- Estimated Annual Rewards: ₹[amount]
- Annual Fee: ₹[fee]
- **Net Annual Value: ₹[rewards - fee]**
- **Breakeven Monthly Spend: ₹[amount]**

## SUPPLEMENTARY RECOMMENDATION

[Same format as above for 2nd card]

## CATEGORY-WISE CARD USAGE STRATEGY

| Category | Monthly Spend | Recommended Card | Reward Rate | Est. Monthly Rewards |
|----------|---------------|------------------|-------------|----------------------|
| Dining | ₹{profile.monthly_spend['dining']:,.0f} | [Card] | X% | ₹[amount] |
| Travel | ₹{profile.monthly_spend['travel']:,.0f} | [Card] | X% | ₹[amount] |
| Online Shopping | ₹{profile.monthly_spend['online_shopping']:,.0f} | [Card] | X% | ₹[amount] |

**Total Estimated Monthly Rewards: ₹[sum]**
**Total Estimated Annual Rewards: ₹[sum x 12]**

## PORTFOLIO ANALYSIS

**Total Annual Fees:** ₹[sum of all fees]
**Total Annual Rewards:** ₹[sum of all rewards]
**Net Annual Benefit:** ₹[rewards - fees]
**Return on Fee Investment:** [X]%

## WARNINGS & CONSIDERATIONS

- [Important caveat 1]
- [Important caveat 2]
- [Important caveat 3]

---

{profile.generate_prompt_context()}

**User Query:** {query}

**Instructions:**
1. Recommend 2-3 cards that match the spending profile
2. Calculate exact ROI based on provided spending amounts
3. Create detailed category-wise strategy
4. Show breakeven analysis
5. Include comparison table
6. List important warnings
"""
        return prompt
    
    def _structure_output(self, ai_result: dict, query: str, profile: SpendingProfile) -> dict:
        """Parse AI output into structured format"""
        
        content = ai_result['content']
        
        structured = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'model_used': ai_result['model_used'],
                'query': query,
                'profile_name': profile.name,
                'profile_monthly_spend': profile.get_total_monthly_spend(),
                'profile_annual_spend': profile.get_annual_spend()
            },
            'raw_analysis': content,
            'recommendations': self._parse_recommendations(content),
            'category_strategy': self._parse_category_table(content),
            'portfolio_summary': self._parse_portfolio(content),
            'warnings': self._parse_warnings(content),
            'spending_profile': profile.to_dict()
        }
        
        return structured
    
    def _parse_recommendations(self, content: str) -> List[Dict]:
        """Parse card recommendations from AI output"""
        recommendations = []
        
        # Look for card names in bold or after "Card Name:"
        card_pattern = r'\*\*Card Name:\*\*\s*([^\n]+)'
        cards = re.findall(card_pattern, content, re.IGNORECASE)
        
        for card in cards:
            recommendations.append({
                'card_name': card.strip(),
                'extracted': True
            })
        
        return recommendations
    
    def _parse_category_table(self, content: str) -> Dict:
        """Extract category-wise spending strategy"""
        # This is a simplified parser - enhance based on actual AI output
        return {
            'table_found': '| Category |' in content,
            'categories': []
        }
    
    def _parse_portfolio(self, content: str) -> Dict:
        """Parse portfolio analysis section"""
        portfolio = {
            'total_annual_fees': 0,
            'total_annual_rewards': 0,
            'net_benefit': 0,
            'roi_percentage': 0
        }
        
        # Extract numbers from portfolio section
        fee_match = re.search(r'Total Annual Fees:\s*₹([\d,]+)', content)
        if fee_match:
            portfolio['total_annual_fees'] = int(fee_match.group(1).replace(',', ''))
        
        reward_match = re.search(r'Total Annual Rewards:\s*₹([\d,]+)', content)
        if reward_match:
            portfolio['total_annual_rewards'] = int(reward_match.group(1).replace(',', ''))
        
        return portfolio
    
    def _parse_warnings(self, content: str) -> List[str]:
        """Extract warnings and considerations"""
        warnings = []
        
        # Look for warnings section
        warnings_section = re.search(r'## WARNINGS.*?(?=##|$)', content, re.DOTALL | re.IGNORECASE)
        if warnings_section:
            lines = warnings_section.group(0).split('\n')
            for line in lines:
                if line.strip().startswith('-'):
                    warnings.append(line.strip()[1:].strip())
        
        return warnings
    
    def _save_outputs(self, structured_data: dict):
        """Save analysis in multiple formats"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        profile_name = structured_data['metadata']['profile_name']
        
        # Create output directories
        output_dir = Path("recommendations")
        json_dir = output_dir / "json"
        markdown_dir = output_dir / "markdown"
        
        json_dir.mkdir(parents=True, exist_ok=True)
        markdown_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON (structured data)
        json_file = json_dir / f"{timestamp}-{profile_name}-structured.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Structured JSON saved: {json_file}")
        
        # Save Markdown (human-readable)
        md_file = markdown_dir / f"{timestamp}-{profile_name}-analysis.md"
        markdown_content = self._generate_markdown(structured_data)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Markdown report saved: {md_file}")
        
        # Also save to main recommendations folder for backward compatibility
        legacy_file = output_dir / f"{timestamp}-card-analysis.md"
        with open(legacy_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Legacy format saved: {legacy_file}")
    
    def _generate_markdown(self, data: dict) -> str:
        """Generate markdown report from structured data"""
        
        md = f"""# Credit Card Analysis Report (Enhanced)

**Generated:** {datetime.fromisoformat(data['metadata']['timestamp']).strftime("%B %d, %Y at %I:%M %p IST")}
**AI Model:** `{data['metadata']['model_used']}`
**Profile:** {data['metadata']['profile_name']}
**Monthly Spend:** ₹{data['metadata']['profile_monthly_spend']:,.0f}
**Annual Spend:** ₹{data['metadata']['profile_annual_spend']:,.0f}

---

## Query

{data['metadata']['query']}

---

## Analysis

{data['raw_analysis']}

---

## Structured Summary

### Recommended Cards

"""
        
        for i, rec in enumerate(data['recommendations'], 1):
            md += f"{i}. **{rec['card_name']}**\n"
        
        if data['portfolio_summary']['total_annual_fees'] > 0:
            md += f"\n### Portfolio Summary\n\n"
            md += f"- **Total Annual Fees:** ₹{data['portfolio_summary']['total_annual_fees']:,}\n"
            md += f"- **Total Annual Rewards:** ₹{data['portfolio_summary']['total_annual_rewards']:,}\n"
            md += f"- **Net Annual Benefit:** ₹{data['portfolio_summary']['net_benefit']:,}\n"
        
        if data['warnings']:
            md += f"\n### Important Warnings\n\n"
            for warning in data['warnings']:
                md += f"- {warning}\n"
        
        md += f"""\n---

## Spending Profile Used

"""
        
        profile = data['spending_profile']
        for category, amount in profile['monthly_spend'].items():
            if amount > 0:
                md += f"- **{category.replace('_', ' ').title()}:** ₹{amount:,}/month\n"
        
        md += f"""\n---

*Generated by [Credit Card Optimizer](https://github.com/starkarthikr/credit-card-optimizer) - Enhanced Analysis*  
*Powered by [OpenRouter AI](https://openrouter.ai) - 100% FREE financial intelligence*
"""
        
        return md


def main():
    """Example usage of structured analyzer"""
    print("=" * 80)
    print("    📊 STRUCTURED CREDIT CARD ANALYZER")
    print("=" * 80)
    
    # Load available profiles
    profiles = SpendingProfile.list_profiles()
    
    if not profiles:
        print("\n⚠️ No profiles found. Creating sample profiles...")
        from user_profile import create_sample_profiles
        create_sample_profiles()
        profiles = SpendingProfile.list_profiles()
    
    print(f"\n📋 Found {len(profiles)} profile(s):\n")
    for i, profile_name in enumerate(profiles, 1):
        profile = SpendingProfile.load(profile_name)
        print(f"   {i}. {profile_name} (₹{profile.get_total_monthly_spend():,.0f}/month)")
    
    # Use first profile for demo
    profile = SpendingProfile.load(profiles[0])
    
    query = f"""Recommend the optimal credit card portfolio for this spending profile. 
Include 2-3 cards with detailed ROI calculations and category-wise usage strategy."""
    
    print(f"\n🎯 Using profile: {profile.name}")
    print(f"\n🔍 Query: {query}\n")
    
    analyzer = StructuredAnalyzer()
    result = analyzer.analyze_with_profile(query, profile)
    
    if result['success']:
        print("\n" + "=" * 80)
        print("✅ Analysis complete! Check recommendations/ folder for outputs:")
        print("   • JSON format in recommendations/json/")
        print("   • Markdown format in recommendations/markdown/")
        print("=" * 80)
    else:
        print(f"\n❌ Analysis failed: {result.get('error')}")


if __name__ == "__main__":
    main()
