#!/usr/bin/env python3
"""
Credit Card Milestone Tracker
Track spending toward milestone benefits and bonus rewards
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

class Milestone:
    """Milestone benefit definition"""
    
    def __init__(self, name: str, spend_required: float, reward: str, deadline: str = None):
        self.name = name
        self.spend_required = spend_required
        self.reward = reward
        self.deadline = deadline
        self.current_spend = 0
    
    def remaining_spend(self) -> float:
        return max(0, self.spend_required - self.current_spend)
    
    def progress_percentage(self) -> float:
        return min(100, (self.current_spend / self.spend_required) * 100)
    
    def is_achieved(self) -> bool:
        return self.current_spend >= self.spend_required
    
    def days_remaining(self) -> int:
        if not self.deadline:
            return None
        try:
            deadline_date = datetime.strptime(self.deadline, '%Y-%m-%d')
            return (deadline_date - datetime.now()).days
        except:
            return None

class MilestoneTracker:
    """Track milestones across multiple credit cards"""
    
    def __init__(self):
        self.cards = {}
        self._load_indian_card_milestones()
    
    def _load_indian_card_milestones(self):
        """Load common milestone benefits for Indian credit cards"""
        
        # HDFC Infinia
        self.cards['HDFC Infinia'] = [
            Milestone('Quarterly 12,500 bonus points', 400000, '₹12,500 bonus reward points', self._get_quarter_end()),
            Milestone('Annual 15,000 bonus points', 800000, '₹15,000 bonus reward points', self._get_year_end()),
            Milestone('Renewal fee waiver', 800000, 'Fee waived (₹12,500)', self._get_year_end())
        ]
        
        # Axis Magnus
        self.cards['Axis Magnus'] = [
            Milestone('Monthly 10,000 edge reward', 100000, '10,000 Edge Reward points', self._get_month_end()),
            Milestone('Annual 25,000 bonus', 1500000, '25,000 bonus points', self._get_year_end())
        ]
        
        # HDFC Diners Black
        self.cards['HDFC Diners Club Black'] = [
            Milestone('Fee reversal', 500000, 'Annual fee reversed (₹10,000)', self._get_year_end()),
            Milestone('10X reward points', 80000, '10X points on smartbuy (monthly)', self._get_month_end())
        ]
        
        # SBI Cashback
        self.cards['SBI Cashback'] = [
            Milestone('Annual fee waiver', 200000, 'Fee waived (₹999)', self._get_year_end())
        ]
        
        # Axis Vistara Infinite
        self.cards['Axis Vistara Infinite'] = [
            Milestone('Silver tier status', 150000, 'Vistara Silver membership', self._get_year_end()),
            Milestone('Gold tier status', 500000, 'Vistara Gold membership', self._get_year_end()),
            Milestone('Fee waiver', 400000, 'Annual fee waived (₹10,000)', self._get_year_end())
        ]
    
    def _get_month_end(self) -> str:
        """Get last day of current month"""
        today = datetime.now()
        next_month = today.replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        return last_day.strftime('%Y-%m-%d')
    
    def _get_quarter_end(self) -> str:
        """Get last day of current quarter"""
        today = datetime.now()
        quarter = (today.month - 1) // 3
        quarter_end_month = (quarter + 1) * 3
        quarter_end = datetime(today.year, quarter_end_month, 1) + timedelta(days=32)
        quarter_end = quarter_end.replace(day=1) - timedelta(days=1)
        return quarter_end.strftime('%Y-%m-%d')
    
    def _get_year_end(self) -> str:
        """Get last day of current year"""
        return f"{datetime.now().year}-12-31"
    
    def update_spend(self, card_name: str, amount: float):
        """Update spend for a card"""
        if card_name in self.cards:
            for milestone in self.cards[card_name]:
                milestone.current_spend += amount
    
    def get_card_progress(self, card_name: str) -> List[dict]:
        """Get milestone progress for a card"""
        if card_name not in self.cards:
            return []
        
        progress = []
        for milestone in self.cards[card_name]:
            progress.append({
                'name': milestone.name,
                'target': milestone.spend_required,
                'current': milestone.current_spend,
                'remaining': milestone.remaining_spend(),
                'progress': milestone.progress_percentage(),
                'achieved': milestone.is_achieved(),
                'reward': milestone.reward,
                'deadline': milestone.deadline,
                'days_remaining': milestone.days_remaining()
            })
        return progress
    
    def generate_report(self) -> str:
        """Generate milestone tracking report"""
        
        report = f"""# Credit Card Milestone Tracker

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p IST")}
**Tracking:** {len(self.cards)} cards

---

"""
        
        for card_name, milestones in self.cards.items():
            report += f"## {card_name}\n\n"
            
            progress_data = self.get_card_progress(card_name)
            
            for data in progress_data:
                status = "✅ ACHIEVED" if data['achieved'] else "🎯 IN PROGRESS"
                
                report += f"### {status}: {data['name']}\n\n"
                report += f"- **Target Spend:** ₹{data['target']:,.0f}\n"
                report += f"- **Current Spend:** ₹{data['current']:,.0f}\n"
                report += f"- **Remaining:** ₹{data['remaining']:,.0f}\n"
                report += f"- **Progress:** {data['progress']:.1f}%\n"
                report += f"- **Reward:** {data['reward']}\n"
                
                if data['days_remaining'] is not None:
                    report += f"- **Days Remaining:** {data['days_remaining']} days\n"
                
                # Progress bar
                progress_bar_length = 20
                filled = int(progress_bar_length * data['progress'] / 100)
                bar = "█" * filled + "░" * (progress_bar_length - filled)
                report += f"- **Progress Bar:** [{bar}] {data['progress']:.1f}%\n"
                
                report += "\n"
            
            report += "---\n\n"
        
        report += """## Tips for Reaching Milestones

1. **Plan large purchases** around milestone deadlines
2. **Prepay bills** like insurance, rent if allowed
3. **Buy gift cards** for future spending
4. **Split transactions** among cards strategically
5. **Use bill payment platforms** that accept credit cards
6. **Consider family add-on cards** for combined spending

---

*Generated by [Credit Card Optimizer](https://github.com/starkarthikr/credit-card-optimizer)*
"""
        
        return report
    
    def save_report(self, filepath: str = None) -> str:
        """Save milestone report"""
        if not filepath:
            output_dir = Path('recommendations')
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = output_dir / f"{timestamp}-milestone-tracker.md"
        
        report = self.generate_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(filepath)


if __name__ == "__main__":
    print("=" * 80)
    print("    Credit Card Milestone Tracker")
    print("=" * 80)
    
    tracker = MilestoneTracker()
    
    # Simulate some spending
    print("\nSimulating spending...")
    tracker.update_spend('HDFC Infinia', 250000)
    tracker.update_spend('Axis Magnus', 75000)
    tracker.update_spend('SBI Cashback', 150000)
    
    # Generate report
    filepath = tracker.save_report()
    print(f"\n✅ Milestone report saved: {filepath}")
    
    # Show preview
    report = tracker.generate_report()
    print("\nReport Preview:")
    print(report[:1500])
