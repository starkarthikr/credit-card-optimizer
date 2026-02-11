#!/usr/bin/env python3
"""
User Spending Profile System
Enables personalized credit card recommendations based on actual spending patterns
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class SpendingProfile:
    """User spending profile for personalized card recommendations"""
    
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
        # Monthly spending by category (in INR)
        self.monthly_spend = {
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
        
        # User preferences
        self.preferences = {
            'max_annual_fee': 10000,
            'preferred_banks': [],
            'excluded_banks': [],
            'reward_type': 'cashback',  # cashback, miles, points
            'card_network': 'any',  # visa, mastercard, amex, rupay, any
            'international_usage': False,
            'lounge_access_required': False,
            'golf_privileges': False,
            'concierge_service': False
        }
        
        # Current cards owned
        self.current_cards = []
        
        # Financial profile
        self.financial_profile = {
            'annual_income': 0,
            'age': 0,
            'occupation': '',
            'city': ''
        }
    
    def set_spending(self, category: str, amount: float):
        """Set monthly spending for a category"""
        if category in self.monthly_spend:
            self.monthly_spend[category] = amount
            self.updated_at = datetime.now().isoformat()
        else:
            raise ValueError(f"Invalid category: {category}")
    
    def get_total_monthly_spend(self) -> float:
        """Calculate total monthly spending"""
        return sum(self.monthly_spend.values())
    
    def get_total_annual_spend(self) -> float:
        """Calculate total annual spending"""
        return self.get_total_monthly_spend() * 12
    
    def get_spending_distribution(self) -> Dict[str, float]:
        """Get spending distribution as percentages"""
        total = self.get_total_monthly_spend()
        if total == 0:
            return {k: 0 for k in self.monthly_spend.keys()}
        
        return {
            category: (amount / total) * 100
            for category, amount in self.monthly_spend.items()
        }
    
    def get_top_categories(self, n: int = 3) -> List[tuple]:
        """Get top N spending categories"""
        sorted_categories = sorted(
            self.monthly_spend.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_categories[:n]
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary"""
        return {
            'profile_name': self.profile_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'monthly_spend': self.monthly_spend,
            'preferences': self.preferences,
            'current_cards': self.current_cards,
            'financial_profile': self.financial_profile
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SpendingProfile':
        """Create profile from dictionary"""
        profile = cls(data['profile_name'])
        profile.created_at = data.get('created_at', profile.created_at)
        profile.updated_at = data.get('updated_at', profile.updated_at)
        profile.monthly_spend = data.get('monthly_spend', profile.monthly_spend)
        profile.preferences = data.get('preferences', profile.preferences)
        profile.current_cards = data.get('current_cards', [])
        profile.financial_profile = data.get('financial_profile', profile.financial_profile)
        return profile
    
    def save(self, directory: str = 'profiles'):
        """Save profile to JSON file"""
        profiles_dir = Path(directory)
        profiles_dir.mkdir(exist_ok=True)
        
        filename = f"{self.profile_name.lower().replace(' ', '_')}.json"
        filepath = profiles_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    @classmethod
    def load(cls, profile_name: str, directory: str = 'profiles') -> 'SpendingProfile':
        """Load profile from JSON file"""
        filename = f"{profile_name.lower().replace(' ', '_')}.json"
        filepath = Path(directory) / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Profile not found: {profile_name}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    @staticmethod
    def list_profiles(directory: str = 'profiles') -> List[str]:
        """List all available profiles"""
        profiles_dir = Path(directory)
        if not profiles_dir.exists():
            return []
        
        return [f.stem for f in profiles_dir.glob('*.json')]
    
    def generate_analysis_prompt(self) -> str:
        """Generate personalized analysis prompt for AI"""
        total_monthly = self.get_total_monthly_spend()
        top_categories = self.get_top_categories(3)
        
        prompt = f"""Analyze and recommend the best credit card strategy for this spending profile:

**Monthly Spending Pattern (Total: ₹{total_monthly:,.0f}/month = ₹{total_monthly * 12:,.0f}/year)**
"""
        
        # Add detailed spending breakdown
        for category, amount in self.monthly_spend.items():
            if amount > 0:
                percentage = (amount / total_monthly * 100) if total_monthly > 0 else 0
                prompt += f"- {category.replace('_', ' ').title()}: ₹{amount:,.0f} ({percentage:.1f}%)\n"
        
        # Add preferences
        prompt += f"\n**Preferences:**\n"
        prompt += f"- Maximum Annual Fee: ₹{self.preferences['max_annual_fee']:,}\n"
        prompt += f"- Preferred Reward Type: {self.preferences['reward_type'].title()}\n"
        
        if self.preferences['preferred_banks']:
            prompt += f"- Preferred Banks: {', '.join(self.preferences['preferred_banks'])}\n"
        
        if self.preferences['lounge_access_required']:
            prompt += f"- Airport Lounge Access: Required\n"
        
        if self.preferences['international_usage']:
            prompt += f"- International Usage: Yes (low forex markup needed)\n"
        
        # Add current cards if any
        if self.current_cards:
            prompt += f"\n**Current Cards:** {', '.join(self.current_cards)}\n"
        
        # Add financial profile if available
        if self.financial_profile.get('annual_income', 0) > 0:
            prompt += f"\n**Financial Profile:**\n"
            prompt += f"- Annual Income: ₹{self.financial_profile['annual_income']:,}\n"
        
        prompt += """\n**Required Analysis:**
1. Primary card recommendation with specific reward rates for each spending category
2. Supplementary card (if beneficial) for categories not optimized by primary card
3. Detailed ROI calculation showing:
   - Total annual fees
   - Expected rewards by category
   - Net value after fees
   - Breakeven monthly spend
4. Spending strategy: which card to use for what
5. Alternative cards comparison (top 3 options)
6. Milestone benefits and how to maximize them
7. Warnings about terms, conditions, and caps

Provide specific calculations based on the exact spending amounts listed above.
"""
        
        return prompt


def create_sample_profile():
    """Create a sample spending profile"""
    profile = SpendingProfile("Sample User")
    
    # Set spending
    profile.set_spending('dining', 15000)
    profile.set_spending('online_shopping', 25000)
    profile.set_spending('groceries', 12000)
    profile.set_spending('fuel', 8000)
    profile.set_spending('travel', 20000)
    profile.set_spending('utilities', 5000)
    profile.set_spending('entertainment', 7000)
    
    # Set preferences
    profile.preferences['max_annual_fee'] = 5000
    profile.preferences['reward_type'] = 'cashback'
    profile.preferences['lounge_access_required'] = True
    profile.preferences['international_usage'] = False
    
    # Set financial profile
    profile.financial_profile['annual_income'] = 1200000
    profile.financial_profile['age'] = 32
    profile.financial_profile['occupation'] = 'Software Engineer'
    profile.financial_profile['city'] = 'Bangalore'
    
    return profile


if __name__ == "__main__":
    print("=" * 80)
    print("    Credit Card Optimizer - User Profile System")
    print("=" * 80)
    
    # Create sample profile
    print("\nCreating sample profile...")
    profile = create_sample_profile()
    
    # Display profile summary
    print(f"\nProfile: {profile.profile_name}")
    print(f"Total Monthly Spend: ₹{profile.get_total_monthly_spend():,.0f}")
    print(f"Total Annual Spend: ₹{profile.get_total_annual_spend():,.0f}")
    
    print("\nTop 3 Spending Categories:")
    for category, amount in profile.get_top_categories(3):
        print(f"  {category.replace('_', ' ').title()}: ₹{amount:,.0f}")
    
    # Save profile
    filepath = profile.save()
    print(f"\n✅ Profile saved: {filepath}")
    
    # Generate analysis prompt
    print("\n" + "=" * 80)
    print("Generated Analysis Prompt:")
    print("=" * 80)
    print(profile.generate_analysis_prompt())
