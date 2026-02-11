#!/usr/bin/env python3
"""
Structured Card Analyzer
Generates AI analysis with structured JSON output and comparison tables
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from main import generate_content
from user_profile import SpendingProfile

class StructuredAnalyzer:
    """Generate structured credit card analysis with JSON output"""
    
    def __init__(self):
        self.analysis_data = {}
        self.recommendations = []
    
    def analyze_with_profile(self, profile: SpendingProfile, model: str = "meta-llama/llama-3.2-3b-instruct:free") -> dict:
        """Run analysis with user spending profile"""
        
        # Generate enhanced prompt from profile
        prompt = profile.generate_analysis_prompt()
        
        # Get AI analysis
        print(f"\n🔍 Analyzing for profile: {profile.profile_name}")
        print(f"   Total monthly spend: ₹{profile.get_total_monthly_spend():,.0f}")
        
        result = generate_content(prompt, model, retry_fallback=True)
        
        if result['success']:
            # Structure the output
            structured_data = {
                'timestamp': datetime.now().isoformat(),
                'profile_name': profile.profile_name,
                'model_used': result['model_used'],
                'spending_profile': profile.to_dict(),
                'raw_analysis': result['content'],
                'structured_recommendations': self._parse_recommendations(result['content']),
                'roi_calculations': self._extract_roi_data(result['content']),
                'comparison_table': self._generate_comparison_table(result['content'])
            }
            
            self.analysis_data = structured_data
            return structured_data
        else:
            return {'success': False, 'error': result['error']}
    
    def analyze_cards(self, cards: List[str], spending_amount: float, model: str = "meta-llama/llama-3.2-3b-instruct:free") -> dict:
        """Compare specific credit cards"""
        
        prompt = f"""Compare these Indian credit cards for someone with ₹{spending_amount:,.0f} monthly spending:

Cards to compare:
{chr(10).join([f'{i+1}. {card}' for i, card in enumerate(cards)])}

For each card, provide:

### Card Name
- **Annual Fee**: ₹X
- **Reward Rate**: X% or X points/₹100
- **Best Categories**: [List]
- **Annual Value**: ₹X (for ₹{spending_amount:,.0f}/month spend)
- **Key Benefits**: [List top 5]
- **Breakeven Spend**: ₹X/month
- **Pros**: [List 3]
- **Cons**: [List 3]

## Direct Comparison Table

Create a markdown table comparing all cards across:
- Annual Fee
- Reward Rate  
- Lounge Access
- Travel Insurance
- Best Use Case
- Estimated Annual Value

## Final Recommendation

Rank the cards from best to worst for this spending level and explain why.
"""
        
        result = generate_content(prompt, model, retry_fallback=True)
        
        if result['success']:
            structured_data = {
                'timestamp': datetime.now().isoformat(),
                'cards_compared': cards,
                'monthly_spending': spending_amount,
                'model_used': result['model_used'],
                'raw_analysis': result['content'],
                'structured_data': self._parse_comparison(result['content'], cards),
                'comparison_table': self._extract_table(result['content'])
            }
            
            self.analysis_data = structured_data
            return structured_data
        else:
            return {'success': False, 'error': result['error']}
    
    def _parse_recommendations(self, analysis_text: str) -> dict:
        """Extract structured recommendations from AI text"""
        
        recommendations = {
            'primary_card': {},
            'supplementary_cards': [],
            'strategy': ''
        }
        
        # Extract primary card mention
        primary_match = re.search(r'(?:Primary Card|Recommended|Best Card):\s*\*\*([^*]+)\*\*', analysis_text, re.IGNORECASE)
        if primary_match:
            recommendations['primary_card']['name'] = primary_match.group(1).strip()
        
        # Extract annual fees
        fee_matches = re.findall(r'Annual Fee[:\s]*₹([\d,]+)', analysis_text)
        if fee_matches:
            recommendations['primary_card']['annual_fee'] = float(fee_matches[0].replace(',', ''))
        
        # Extract reward rates
        reward_matches = re.findall(r'(?:Reward Rate|Cashback)[:\s]*([\d.]+)%', analysis_text)
        if reward_matches:
            recommendations['primary_card']['reward_rate'] = float(reward_matches[0])
        
        return recommendations
    
    def _extract_roi_data(self, analysis_text: str) -> dict:
        """Extract ROI calculations"""
        
        roi = {
            'total_annual_fees': 0,
            'estimated_rewards': 0,
            'net_value': 0,
            'breakeven_spend': 0
        }
        
        # Extract various financial figures
        fee_matches = re.findall(r'(?:Annual Fee|Total Fee)[:\s]*₹([\d,]+)', analysis_text)
        if fee_matches:
            roi['total_annual_fees'] = sum([float(f.replace(',', '')) for f in fee_matches[:2]])
        
        reward_matches = re.findall(r'(?:Annual Reward|Total Reward|Rewards)[:\s]*₹([\d,]+)', analysis_text)
        if reward_matches:
            roi['estimated_rewards'] = float(reward_matches[0].replace(',', ''))
        
        net_matches = re.findall(r'(?:Net Value|Net Benefit)[:\s]*₹([\d,]+)', analysis_text)
        if net_matches:
            roi['net_value'] = float(net_matches[0].replace(',', ''))
        
        return roi
    
    def _generate_comparison_table(self, analysis_text: str) -> str:
        """Generate formatted comparison table"""
        
        # Extract existing table if present
        table_match = re.search(r'\|[^|]+\|[^|]+\|.*?\n\|[-\s|]+\n((?:\|[^\n]+\n)+)', analysis_text)
        
        if table_match:
            return table_match.group(0)
        else:
            return "No comparison table found in analysis"
    
    def _parse_comparison(self, analysis_text: str, cards: List[str]) -> dict:
        """Parse card comparison data"""
        
        comparison = {}
        
        for card in cards:
            comparison[card] = {
                'annual_fee': None,
                'reward_rate': None,
                'best_for': [],
                'pros': [],
                'cons': []
            }
        
        return comparison
    
    def _extract_table(self, text: str) -> str:
        """Extract markdown table from text"""
        table_match = re.search(r'(\|.+\|\n\|[-\s:|]+\|\n(?:\|.+\|\n)+)', text, re.MULTILINE)
        return table_match.group(0) if table_match else "No table found"
    
    def save_json(self, filepath: str = None) -> str:
        """Save structured analysis as JSON"""
        
        if not filepath:
            output_dir = Path('recommendations/structured')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = output_dir / f"{timestamp}-analysis.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_markdown(self, filepath: str = None) -> str:
        """Save analysis as enhanced markdown"""
        
        if not self.analysis_data:
            return None
        
        if not filepath:
            output_dir = Path('recommendations')
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = output_dir / f"{timestamp}-structured-analysis.md"
        
        # Build enhanced markdown
        profile_name = self.analysis_data.get('profile_name', 'Custom')
        spending_profile = self.analysis_data.get('spending_profile', {})
        
        markdown = f"""# Credit Card Analysis Report (Structured)

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p IST")}
**Profile:** {profile_name}
**AI Model:** `{self.analysis_data.get('model_used', 'Unknown')}`
**Analysis Type:** Personalized Optimization

---

## Spending Profile Summary

"""
        
        if spending_profile.get('monthly_spend'):
            total_monthly = sum(spending_profile['monthly_spend'].values())
            markdown += f"**Total Monthly Spend:** ₹{total_monthly:,.0f}\n\n"
            markdown += "**Category Breakdown:**\n\n"
            
            for category, amount in sorted(spending_profile['monthly_spend'].items(), key=lambda x: x[1], reverse=True):
                if amount > 0:
                    percentage = (amount / total_monthly * 100) if total_monthly > 0 else 0
                    markdown += f"- {category.replace('_', ' ').title()}: ₹{amount:,.0f} ({percentage:.1f}%)\n"
        
        markdown += "\n---\n\n## AI Analysis\n\n"
        markdown += self.analysis_data.get('raw_analysis', '')
        
        markdown += "\n\n---\n\n## Structured Data\n\n"
        markdown += "```json\n"
        markdown += json.dumps(self.analysis_data.get('structured_recommendations', {}), indent=2)
        markdown += "\n```\n"
        
        markdown += "\n---\n\n"
        markdown += "*Generated by [Credit Card Optimizer](https://github.com/starkarthikr/credit-card-optimizer)*\n"
        markdown += "*Powered by [OpenRouter AI](https://openrouter.ai)*\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        return str(filepath)
    
    def save_both(self) -> tuple:
        """Save both JSON and Markdown formats"""
        json_path = self.save_json()
        md_path = self.save_markdown()
        return (json_path, md_path)


if __name__ == "__main__":
    print("=" * 80)
    print("    Structured Credit Card Analyzer")
    print("=" * 80)
    
    # Create sample profile
    from user_profile import create_sample_profile
    profile = create_sample_profile()
    
    # Run structured analysis
    analyzer = StructuredAnalyzer()
    print("\nRunning structured analysis...")
    
    result = analyzer.analyze_with_profile(profile)
    
    if result.get('success', True):
        print("\n✅ Analysis complete!")
        
        # Save outputs
        json_path, md_path = analyzer.save_both()
        print(f"\n📄 JSON saved: {json_path}")
        print(f"📄 Markdown saved: {md_path}")
        
        print("\n📊 Structured Data Preview:")
        print(json.dumps(result.get('structured_recommendations', {}), indent=2)[:500])
    else:
        print(f"\n❌ Analysis failed: {result.get('error')}")
