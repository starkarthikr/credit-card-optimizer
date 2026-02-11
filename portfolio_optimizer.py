#!/usr/bin/env python3
"""
Credit Card Portfolio Optimizer
Find optimal 2-3 card combinations to maximize rewards across spending categories
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from itertools import combinations
from user_profile import SpendingProfile


@dataclass
class CreditCard:
    """Credit card with reward rates and benefits"""
    name: str
    bank: str
    annual_fee: float
    
    # Reward rates by category (as percentage or points per Rs 100)
    reward_rates: Dict[str, float]
    
    # Special benefits
    lounge_access: bool = False
    travel_insurance: bool = False
    fuel_surcharge_waiver: bool = False
    
    # Eligibility
    min_income: float = 0
    min_credit_score: int = 0
    
    def calculate_rewards(self, spending: Dict[str, float]) -> float:
        """Calculate total annual rewards for given spending pattern"""
        total_rewards = 0
        
        for category, amount in spending.items():
            # Get reward rate for category (default to base rate if not specified)
            rate = self.reward_rates.get(category, self.reward_rates.get('base', 0))
            
            # Calculate rewards (assuming 1% = Rs 1 per Rs 100)
            rewards = (amount * 12 * rate) / 100
            total_rewards += rewards
        
        return total_rewards
    
    def calculate_net_value(self, spending: Dict[str, float]) -> float:
        """Calculate net value (rewards - annual fee)"""
        rewards = self.calculate_rewards(spending)
        return rewards - self.annual_fee
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'bank': self.bank,
            'annual_fee': self.annual_fee,
            'reward_rates': self.reward_rates,
            'lounge_access': self.lounge_access,
            'travel_insurance': self.travel_insurance
        }


class PortfolioOptimizer:
    """Optimize credit card portfolio for maximum rewards"""
    
    def __init__(self):
        self.cards = self._initialize_card_database()
    
    def _initialize_card_database(self) -> List[CreditCard]:
        """Initialize with popular Indian credit cards"""
        
        return [
            # Premium Travel Cards
            CreditCard(
                name="HDFC Bank Infinia",
                bank="HDFC Bank",
                annual_fee=12500,
                reward_rates={
                    'dining': 3.3,
                    'travel': 3.3,
                    'online_shopping': 3.3,
                    'groceries': 1.65,
                    'base': 1.65
                },
                lounge_access=True,
                travel_insurance=True,
                min_income=2400000
            ),
            CreditCard(
                name="Axis Bank Magnus",
                bank="Axis Bank",
                annual_fee=12500,
                reward_rates={
                    'dining': 2.5,
                    'travel': 2.5,
                    'online_shopping': 2.0,
                    'base': 1.2
                },
                lounge_access=True,
                travel_insurance=True,
                min_income=1500000
            ),
            
            # Mid-Tier Rewards Cards
            CreditCard(
                name="HDFC Bank Regalia",
                bank="HDFC Bank",
                annual_fee=2500,
                reward_rates={
                    'dining': 2.0,
                    'travel': 2.0,
                    'online_shopping': 1.5,
                    'base': 1.3
                },
                lounge_access=True,
                min_income=600000
            ),
            CreditCard(
                name="SBI Card Elite",
                bank="SBI Card",
                annual_fee=4999,
                reward_rates={
                    'dining': 3.0,
                    'travel': 2.0,
                    'online_shopping': 2.5,
                    'groceries': 2.0,
                    'base': 1.5
                },
                lounge_access=True,
                min_income=900000
            ),
            
            # Cashback Cards
            CreditCard(
                name="ICICI Amazon Pay",
                bank="ICICI Bank",
                annual_fee=0,
                reward_rates={
                    'online_shopping': 5.0,
                    'dining': 2.0,
                    'travel': 2.0,
                    'base': 1.0
                },
                min_income=360000
            ),
            CreditCard(
                name="Axis Bank Ace",
                bank="Axis Bank",
                annual_fee=0,
                reward_rates={
                    'utilities': 5.0,
                    'online_shopping': 2.0,
                    'base': 1.5
                },
                min_income=300000
            ),
            
            # Entry Level
            CreditCard(
                name="HDFC Bank Millennia",
                bank="HDFC Bank",
                annual_fee=1000,
                reward_rates={
                    'online_shopping': 5.0,
                    'dining': 2.5,
                    'base': 1.0
                },
                min_income=300000
            ),
        ]
    
    def filter_eligible_cards(self, profile: SpendingProfile) -> List[CreditCard]:
        """Filter cards based on user eligibility"""
        eligible = []
        
        income = profile.demographics.get('annual_income', 0)
        credit_score = profile.demographics.get('credit_score', 0)
        max_fee = profile.preferences.get('max_annual_fee', float('inf'))
        
        for card in self.cards:
            if (card.min_income <= income and 
                card.min_credit_score <= credit_score and
                card.annual_fee <= max_fee):
                eligible.append(card)
        
        return eligible
    
    def optimize_single_card(self, profile: SpendingProfile) -> Tuple[CreditCard, float]:
        """Find best single card for profile"""
        eligible = self.filter_eligible_cards(profile)
        
        best_card = None
        best_value = float('-inf')
        
        for card in eligible:
            net_value = card.calculate_net_value(profile.monthly_spend)
            if net_value > best_value:
                best_value = net_value
                best_card = card
        
        return best_card, best_value
    
    def optimize_portfolio(self, profile: SpendingProfile, max_cards: int = 3) -> Dict:
        """Find optimal card portfolio"""
        
        eligible = self.filter_eligible_cards(profile)
        
        print(f"\n💳 Analyzing {len(eligible)} eligible cards...")
        print(f"   Budget: Max annual fee ₹{profile.preferences.get('max_annual_fee'):,}")
        print(f"   Optimizing for: {max_cards} card(s)\n")
        
        best_portfolio = None
        best_total_value = float('-inf')
        
        # Try all combinations up to max_cards
        for num_cards in range(1, min(max_cards + 1, len(eligible) + 1)):
            for card_combo in combinations(eligible, num_cards):
                portfolio_value = self._calculate_portfolio_value(card_combo, profile)
                
                if portfolio_value['net_value'] > best_total_value:
                    best_total_value = portfolio_value['net_value']
                    best_portfolio = portfolio_value
                    best_portfolio['cards'] = list(card_combo)
        
        return best_portfolio
    
    def _calculate_portfolio_value(self, cards: Tuple[CreditCard, ...], profile: SpendingProfile) -> Dict:
        """Calculate value of a card portfolio with optimal category assignment"""
        
        spending = profile.monthly_spend
        total_fees = sum(card.annual_fee for card in cards)
        
        # For each spending category, assign to best card
        category_assignments = {}
        total_rewards = 0
        
        for category, monthly_amount in spending.items():
            if monthly_amount == 0:
                continue
            
            # Find card with highest reward rate for this category
            best_rate = 0
            best_card = None
            
            for card in cards:
                rate = card.reward_rates.get(category, card.reward_rates.get('base', 0))
                if rate > best_rate:
                    best_rate = rate
                    best_card = card
            
            if best_card:
                category_rewards = (monthly_amount * 12 * best_rate) / 100
                total_rewards += category_rewards
                
                category_assignments[category] = {
                    'card': best_card.name,
                    'monthly_spend': monthly_amount,
                    'reward_rate': best_rate,
                    'annual_rewards': category_rewards
                }
        
        return {
            'total_fees': total_fees,
            'total_rewards': total_rewards,
            'net_value': total_rewards - total_fees,
            'roi_percentage': ((total_rewards - total_fees) / total_fees * 100) if total_fees > 0 else 0,
            'category_assignments': category_assignments
        }
    
    def generate_recommendation_report(self, profile: SpendingProfile, portfolio: Dict) -> str:
        """Generate detailed portfolio recommendation report"""
        
        report = f"""# Optimal Credit Card Portfolio

## Recommended Cards

"""
        
        for i, card in enumerate(portfolio['cards'], 1):
            report += f"""### {i}. {card.name}

- **Bank:** {card.bank}
- **Annual Fee:** ₹{card.annual_fee:,}
- **Reward Rates:**
"""
            for cat, rate in sorted(card.reward_rates.items(), key=lambda x: x[1], reverse=True):
                report += f"  - {cat.replace('_', ' ').title()}: {rate}%\n"
            
            if card.lounge_access:
                report += "- **Lounge Access:** Yes\n"
            if card.travel_insurance:
                report += "- **Travel Insurance:** Yes\n"
            report += "\n"
        
        report += f"""## Category-Wise Card Usage Strategy

| Category | Monthly Spend | Use Card | Reward Rate | Annual Rewards |
|----------|---------------|----------|-------------|----------------|
"""
        
        for category, details in sorted(portfolio['category_assignments'].items(), 
                                       key=lambda x: x[1]['annual_rewards'], 
                                       reverse=True):
            report += f"""| {category.replace('_', ' ').title()} | ₹{details['monthly_spend']:,.0f} | {details['card']} | {details['reward_rate']}% | ₹{details['annual_rewards']:,.0f} |\n"""
        
        report += f"""\n## Portfolio Summary

- **Total Annual Fees:** ₹{portfolio['total_fees']:,.0f}
- **Total Annual Rewards:** ₹{portfolio['total_rewards']:,.0f}
- **Net Annual Benefit:** ₹{portfolio['net_value']:,.0f}
- **Return on Investment:** {portfolio['roi_percentage']:.1f}%

### Interpretation

"""
        
        if portfolio['net_value'] > 0:
            report += f"This portfolio provides a positive net benefit of ₹{portfolio['net_value']:,.0f} per year.\n"
        else:
            report += f"This portfolio results in a net loss of ₹{abs(portfolio['net_value']):,.0f} per year. Consider no-fee cards.\n"
        
        report += f"""\n---

*Generated by Credit Card Portfolio Optimizer*
"""
        
        return report


def main():
    """Example usage"""
    print("=" * 80)
    print("    🎯 CREDIT CARD PORTFOLIO OPTIMIZER")
    print("=" * 80)
    
    # Load or create sample profile
    try:
        profile = SpendingProfile.load("travel_enthusiast")
    except:
        from user_profile import create_sample_profiles
        create_sample_profiles()
        profile = SpendingProfile.load("travel_enthusiast")
    
    print(f"\n📁 Analyzing profile: {profile.name}")
    print(f"   Monthly spend: ₹{profile.get_total_monthly_spend():,.0f}")
    print(f"   Annual spend: ₹{profile.get_annual_spend():,.0f}")
    
    # Optimize portfolio
    optimizer = PortfolioOptimizer()
    portfolio = optimizer.optimize_portfolio(profile, max_cards=3)
    
    # Generate report
    report = optimizer.generate_recommendation_report(profile, portfolio)
    print("\n" + report)
    
    # Save report
    from pathlib import Path
    output_dir = Path("recommendations/portfolio")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = __import__('datetime').datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = output_dir / f"{timestamp}-portfolio-optimization.md"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved: {filepath}")
    print("=" * 80)


if __name__ == "__main__":
    main()
