#!/usr/bin/env python3
"""
Multi-Card Portfolio Optimizer
Finds optimal credit card combinations to maximize rewards
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from itertools import combinations
from user_profile import SpendingProfile

class CardData:
    """Credit card data structure"""
    
    def __init__(self, name: str, bank: str, annual_fee: float):
        self.name = name
        self.bank = bank
        self.annual_fee = annual_fee
        
        # Category-wise reward rates (in percentage or points per ₹100)
        self.category_rewards = {
            'dining': 0,
            'travel': 0,
            'online_shopping': 0,
            'groceries': 0,
            'fuel': 0,
            'utilities': 0,
            'entertainment': 0,
            'healthcare': 0,
            'education': 0,
            'other': 0
        }
        
        # Benefits
        self.lounge_access = 0  # visits per quarter
        self.travel_insurance = False
        self.reward_type = 'cashback'  # cashback, points, miles
        self.point_value = 0.25  # value per point in INR
        
    def calculate_rewards(self, spending_profile: SpendingProfile) -> float:
        """Calculate annual rewards for given spending profile"""
        total_rewards = 0
        
        for category, monthly_spend in spending_profile.monthly_spend.items():
            if category in self.category_rewards:
                reward_rate = self.category_rewards[category]
                
                if self.reward_type == 'cashback':
                    # Direct cashback percentage
                    category_reward = (monthly_spend * 12 * reward_rate) / 100
                else:
                    # Points/miles
                    points = (monthly_spend * 12 * reward_rate) / 100
                    category_reward = points * self.point_value
                
                total_rewards += category_reward
        
        return total_rewards
    
    def calculate_net_value(self, spending_profile: SpendingProfile) -> float:
        """Calculate net value (rewards - fees)"""
        rewards = self.calculate_rewards(spending_profile)
        return rewards - self.annual_fee


class PortfolioOptimizer:
    """Optimize credit card portfolio for maximum rewards"""
    
    def __init__(self):
        self.cards_database = self._load_indian_cards()
    
    def _load_indian_cards(self) -> List[CardData]:
        """Load popular Indian credit cards database"""
        
        cards = []
        
        # HDFC Cards
        infinia = CardData("HDFC Infinia", "HDFC", 12500)
        infinia.category_rewards = {'dining': 5, 'travel': 5, 'online_shopping': 3.3, 'groceries': 3.3, 'fuel': 3.3, 'utilities': 1, 'other': 3.3}
        infinia.reward_type = 'points'
        infinia.point_value = 1.0
        infinia.lounge_access = 12
        cards.append(infinia)
        
        diners_black = CardData("HDFC Diners Club Black", "HDFC", 10000)
        diners_black.category_rewards = {'dining': 3.3, 'travel': 3.3, 'online_shopping': 3.3, 'groceries': 1.3, 'fuel': 1.3, 'utilities': 1, 'other': 1.3}
        diners_black.lounge_access = 12
        cards.append(diners_black)
        
        # Axis Cards
        magnus = CardData("Axis Magnus", "Axis", 12500)
        magnus.category_rewards = {'dining': 2.4, 'travel': 2.4, 'online_shopping': 1.2, 'groceries': 1.2, 'fuel': 1.2, 'utilities': 1.2, 'other': 1.2}
        magnus.lounge_access = 8
        cards.append(magnus)
        
        vistara = CardData("Axis Vistara Infinite", "Axis", 10000)
        vistara.category_rewards = {'dining': 1.5, 'travel': 3, 'online_shopping': 1.5, 'groceries': 1.5, 'fuel': 1.5, 'utilities': 1, 'other': 1.5}
        cards.append(vistara)
        
        # SBI Cards
        sbi_cashback = CardData("SBI Cashback", "SBI", 999)
        sbi_cashback.category_rewards = {'online_shopping': 5, 'other': 1}
        sbi_cashback.reward_type = 'cashback'
        cards.append(sbi_cashback)
        
        # ICICI Cards
        amazon_pay = CardData("ICICI Amazon Pay", "ICICI", 0)
        amazon_pay.category_rewards = {'online_shopping': 5, 'other': 1}
        amazon_pay.reward_type = 'cashback'
        cards.append(amazon_pay)
        
        # AMEX Cards
        amex_plat = CardData("AMEX Platinum Travel", "AMEX", 5000)
        amex_plat.category_rewards = {'dining': 1.5, 'travel': 2, 'online_shopping': 1, 'other': 1}
        amex_plat.reward_type = 'points'
        amex_plat.point_value = 0.5
        cards.append(amex_plat)
        
        # IndusInd Cards
        legend = CardData("IndusInd Legend", "IndusInd", 10000)
        legend.category_rewards = {'dining': 3, 'travel': 3, 'online_shopping': 3, 'groceries': 2, 'fuel': 2, 'utilities': 1, 'other': 2}
        cards.append(legend)
        
        return cards
    
    def find_optimal_portfolio(self, spending_profile: SpendingProfile, 
                              max_cards: int = 3,
                              max_total_fee: float = 25000) -> List[Tuple]:
        """Find optimal card combinations"""
        
        portfolios = []
        
        # Generate all possible combinations
        for n_cards in range(1, max_cards + 1):
            for card_combo in combinations(self.cards_database, n_cards):
                total_fee = sum(card.annual_fee for card in card_combo)
                
                # Skip if exceeds fee budget
                if total_fee > max_total_fee:
                    continue
                
                # Calculate optimal spending for this portfolio
                total_rewards = self._calculate_portfolio_rewards(card_combo, spending_profile)
                net_value = total_rewards - total_fee
                
                portfolios.append({
                    'cards': [card.name for card in card_combo],
                    'total_fee': total_fee,
                    'total_rewards': total_rewards,
                    'net_value': net_value,
                    'roi_percentage': (net_value / total_fee * 100) if total_fee > 0 else float('inf'),
                    'spending_strategy': self._generate_strategy(card_combo, spending_profile)
                })
        
        # Sort by net value
        portfolios.sort(key=lambda x: x['net_value'], reverse=True)
        
        return portfolios[:10]  # Top 10 portfolios
    
    def _calculate_portfolio_rewards(self, cards: Tuple[CardData], profile: SpendingProfile) -> float:
        """Calculate optimal rewards using best card for each category"""
        
        total_rewards = 0
        
        for category, monthly_spend in profile.monthly_spend.items():
            if monthly_spend == 0:
                continue
            
            # Find best card for this category
            best_reward_rate = 0
            best_card = None
            
            for card in cards:
                if card.category_rewards.get(category, 0) > best_reward_rate:
                    best_reward_rate = card.category_rewards[category]
                    best_card = card
            
            # Calculate reward
            if best_card:
                annual_spend = monthly_spend * 12
                
                if best_card.reward_type == 'cashback':
                    category_reward = (annual_spend * best_reward_rate) / 100
                else:
                    points = (annual_spend * best_reward_rate) / 100
                    category_reward = points * best_card.point_value
                
                total_rewards += category_reward
        
        return total_rewards
    
    def _generate_strategy(self, cards: Tuple[CardData], profile: SpendingProfile) -> Dict[str, str]:
        """Generate spending strategy for portfolio"""
        
        strategy = {}
        
        for category, monthly_spend in profile.monthly_spend.items():
            if monthly_spend == 0:
                continue
            
            best_reward_rate = 0
            best_card_name = None
            
            for card in cards:
                if card.category_rewards.get(category, 0) > best_reward_rate:
                    best_reward_rate = card.category_rewards[category]
                    best_card_name = card.name
            
            if best_card_name:
                strategy[category] = best_card_name
        
        return strategy
    
    def generate_report(self, spending_profile: SpendingProfile, max_cards: int = 3) -> str:
        """Generate portfolio optimization report"""
        
        print("\n🔍 Finding optimal credit card portfolios...")
        portfolios = self.find_optimal_portfolio(spending_profile, max_cards)
        
        report = f"""# Multi-Card Portfolio Optimization Report

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p IST")}
**Profile:** {spending_profile.profile_name}
**Monthly Spend:** ₹{spending_profile.get_total_monthly_spend():,.0f}
**Annual Spend:** ₹{spending_profile.get_total_annual_spend():,.0f}

---

## Top 10 Optimal Portfolios

"""
        
        for i, portfolio in enumerate(portfolios, 1):
            report += f"""### #{i}. {' + '.join(portfolio['cards'])}

- **Total Annual Fees:** ₹{portfolio['total_fee']:,.0f}
- **Total Annual Rewards:** ₹{portfolio['total_rewards']:,.0f}
- **Net Value:** ₹{portfolio['net_value']:,.0f}
- **ROI:** {portfolio['roi_percentage']:.1f}%

**Spending Strategy:**
"""
            
            for category, card_name in portfolio['spending_strategy'].items():
                spend = spending_profile.monthly_spend.get(category, 0)
                if spend > 0:
                    report += f"- {category.replace('_', ' ').title()} (₹{spend:,.0f}/month): **{card_name}**\n"
            
            report += "\n---\n\n"
        
        report += """## Recommendations

1. **Start with the top portfolio** if you can afford the annual fees
2. **Use the spending strategy** to maximize rewards on each transaction
3. **Review quarterly** as card benefits and your spending patterns change
4. **Consider fee waivers** - many cards waive fees if you meet spending thresholds

---

*Generated by [Credit Card Optimizer](https://github.com/starkarthikr/credit-card-optimizer)*
"""
        
        return report


if __name__ == "__main__":
    print("=" * 80)
    print("    Multi-Card Portfolio Optimizer")
    print("=" * 80)
    
    from user_profile import create_sample_profile
    profile = create_sample_profile()
    
    optimizer = PortfolioOptimizer()
    report = optimizer.generate_report(profile, max_cards=3)
    
    # Save report
    output_dir = Path('recommendations')
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = output_dir / f"{timestamp}-portfolio-optimization.md"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Portfolio optimization report saved: {filepath}")
    print("\nTop 3 Portfolios Preview:")
    print(report[:2000])
