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
    
    def __init__(self, name: str = "default"):
        self.name = name
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
            'insurance': 0,
            'education': 0,
            'other': 0
        }
        
        # User preferences
        self.preferences = {
            'max_annual_fee': 10000,
            'preferred_banks': [],
            'avoid_banks': [],
            'reward_preference': 'cashback',  # 'cashback', 'miles', 'points'
            'lifestyle_benefits': [],  # 'lounge', 'golf', 'concierge', 'dining'
            'min_credit_limit': 100000,
            'existing_cards': []
        }
        
        # User demographics
        self.demographics = {
            'annual_income': 0,
            'city': '',
            'employment_type': 'salaried',  # 'salaried', 'self-employed', 'business'
            'credit_score': 0
        }
    
    def update_spending(self, category: str, amount: float):
        """Update spending for a specific category"""
        if category in self.monthly_spend:
            self.monthly_spend[category] = amount
            self.updated_at = datetime.now().isoformat()
    
    def get_total_monthly_spend(self) -> float:
        """Calculate total monthly spending"""
        return sum(self.monthly_spend.values())
    
    def get_annual_spend(self) -> float:
        """Calculate annual spending"""
        return self.get_total_monthly_spend() * 12
    
    def get_category_percentages(self) -> Dict[str, float]:
        """Get spending breakdown by percentage"""
        total = self.get_total_monthly_spend()
        if total == 0:
            return {cat: 0 for cat in self.monthly_spend}
        return {cat: (amt / total) * 100 for cat, amt in self.monthly_spend.items()}
    
    def get_top_categories(self, n: int = 3) -> List[tuple]:
        """Get top N spending categories"""
        sorted_cats = sorted(self.monthly_spend.items(), key=lambda x: x[1], reverse=True)
        return sorted_cats[:n]
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary"""
        return {
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'monthly_spend': self.monthly_spend,
            'preferences': self.preferences,
            'demographics': self.demographics,
            'summary': {
                'total_monthly_spend': self.get_total_monthly_spend(),
                'annual_spend': self.get_annual_spend(),
                'category_percentages': self.get_category_percentages(),
                'top_categories': self.get_top_categories()
            }
        }
    
    def to_json(self) -> str:
        """Convert profile to JSON string"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    def save(self, directory: str = "profiles"):
        """Save profile to file"""
        profile_dir = Path(directory)
        profile_dir.mkdir(exist_ok=True)
        
        filepath = profile_dir / f"{self.name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
        
        print(f"✅ Profile saved: {filepath}")
        return str(filepath)
    
    @classmethod
    def load(cls, name: str, directory: str = "profiles"):
        """Load profile from file"""
        filepath = Path(directory) / f"{name}.json"
        
        if not filepath.exists():
            raise FileNotFoundError(f"Profile not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        profile = cls(name=data['name'])
        profile.created_at = data['created_at']
        profile.updated_at = data['updated_at']
        profile.monthly_spend = data['monthly_spend']
        profile.preferences = data['preferences']
        profile.demographics = data['demographics']
        
        print(f"✅ Profile loaded: {name}")
        return profile
    
    @classmethod
    def list_profiles(cls, directory: str = "profiles") -> List[str]:
        """List all saved profiles"""
        profile_dir = Path(directory)
        if not profile_dir.exists():
            return []
        return [f.stem for f in profile_dir.glob("*.json")]
    
    def generate_prompt_context(self) -> str:
        """Generate context for AI prompt"""
        top_cats = self.get_top_categories(3)
        
        context = f"""\n\n## User Spending Profile\n\n**Monthly Spending Pattern:**\n"""
        
        for category, amount in self.monthly_spend.items():
            if amount > 0:
                pct = (amount / self.get_total_monthly_spend()) * 100
                context += f"- {category.replace('_', ' ').title()}: ₹{amount:,.0f} ({pct:.1f}%)\n"
        
        context += f"\n**Total Monthly Spend:** ₹{self.get_total_monthly_spend():,.0f}\n"
        context += f"**Annual Spend:** ₹{self.get_annual_spend():,.0f}\n\n"
        
        context += f"**User Preferences:**\n"
        context += f"- Maximum Annual Fee: ₹{self.preferences['max_annual_fee']:,}\n"
        context += f"- Reward Preference: {self.preferences['reward_preference'].title()}\n"
        
        if self.preferences['preferred_banks']:
            context += f"- Preferred Banks: {', '.join(self.preferences['preferred_banks'])}\n"
        
        if self.preferences['lifestyle_benefits']:
            context += f"- Desired Benefits: {', '.join(self.preferences['lifestyle_benefits'])}\n"
        
        if self.demographics['annual_income'] > 0:
            context += f"\n**Demographics:**\n"
            context += f"- Annual Income: ₹{self.demographics['annual_income']:,}\n"
        
        return context


def create_sample_profiles():
    """Create sample profiles for demonstration"""
    
    # Profile 1: Travel Enthusiast
    travel_profile = SpendingProfile("travel_enthusiast")
    travel_profile.monthly_spend = {
        'dining': 15000,
        'travel': 40000,
        'online_shopping': 20000,
        'groceries': 10000,
        'fuel': 5000,
        'utilities': 5000,
        'entertainment': 10000,
        'insurance': 5000,
        'education': 0,
        'other': 5000
    }
    travel_profile.preferences = {
        'max_annual_fee': 15000,
        'preferred_banks': ['HDFC', 'Axis'],
        'avoid_banks': [],
        'reward_preference': 'miles',
        'lifestyle_benefits': ['lounge', 'travel_insurance'],
        'min_credit_limit': 200000,
        'existing_cards': []
    }
    travel_profile.demographics = {
        'annual_income': 1500000,
        'city': 'Bengaluru',
        'employment_type': 'salaried',
        'credit_score': 780
    }
    travel_profile.save()
    
    # Profile 2: Online Shopping Enthusiast
    shopping_profile = SpendingProfile("online_shopper")
    shopping_profile.monthly_spend = {
        'dining': 10000,
        'travel': 5000,
        'online_shopping': 50000,
        'groceries': 15000,
        'fuel': 8000,
        'utilities': 5000,
        'entertainment': 7000,
        'insurance': 0,
        'education': 0,
        'other': 5000
    }
    shopping_profile.preferences = {
        'max_annual_fee': 5000,
        'preferred_banks': ['ICICI', 'SBI'],
        'avoid_banks': [],
        'reward_preference': 'cashback',
        'lifestyle_benefits': ['shopping_discounts'],
        'min_credit_limit': 100000,
        'existing_cards': []
    }
    shopping_profile.demographics = {
        'annual_income': 1000000,
        'city': 'Mumbai',
        'employment_type': 'salaried',
        'credit_score': 750
    }
    shopping_profile.save()
    
    # Profile 3: Budget Conscious
    budget_profile = SpendingProfile("budget_conscious")
    budget_profile.monthly_spend = {
        'dining': 5000,
        'travel': 3000,
        'online_shopping': 8000,
        'groceries': 12000,
        'fuel': 6000,
        'utilities': 4000,
        'entertainment': 3000,
        'insurance': 2000,
        'education': 5000,
        'other': 2000
    }
    budget_profile.preferences = {
        'max_annual_fee': 0,
        'preferred_banks': [],
        'avoid_banks': [],
        'reward_preference': 'cashback',
        'lifestyle_benefits': [],
        'min_credit_limit': 50000,
        'existing_cards': []
    }
    budget_profile.demographics = {
        'annual_income': 600000,
        'city': 'Pune',
        'employment_type': 'salaried',
        'credit_score': 720
    }
    budget_profile.save()
    
    print("\n✅ Created 3 sample profiles:")
    print("   1. travel_enthusiast (₹1.15L/month, premium cards)")
    print("   2. online_shopper (₹1.05L/month, cashback focus)")
    print("   3. budget_conscious (₹50K/month, no annual fee)")


if __name__ == "__main__":
    print("=" * 80)
    print("    💳 CREDIT CARD OPTIMIZER - USER PROFILE SYSTEM")
    print("=" * 80)
    
    # Create sample profiles
    print("\n📁 Creating sample profiles...\n")
    create_sample_profiles()
    
    # List profiles
    print("\n📋 Available Profiles:")
    profiles = SpendingProfile.list_profiles()
    for profile_name in profiles:
        profile = SpendingProfile.load(profile_name)
        total_spend = profile.get_total_monthly_spend()
        top_cat = profile.get_top_categories(1)[0]
        print(f"   • {profile_name}: ₹{total_spend:,.0f}/month (Top: {top_cat[0]} - ₹{top_cat[1]:,.0f})")
    
    print("\n" + "=" * 80)
    print("\n✅ Profile system ready! Use these profiles with run_analysis.py\n")
    print("=" * 80)
