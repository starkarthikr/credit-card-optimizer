#!/usr/bin/env python3
"""
Expense Tracker Import System
Import transactions from bank statements, Money Manager, Walnut, CRED exports
"""

import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from user_profile import SpendingProfile


class ExpenseImporter:
    """Import and categorize expenses from various sources"""
    
    CATEGORY_KEYWORDS = {
        'dining': ['restaurant', 'zomato', 'swiggy', 'food', 'cafe', 'dining', 'pizza', 'burger', 'dominos', 'mcdonald'],
        'travel': ['uber', 'ola', 'flight', 'airline', 'hotel', 'booking', 'goibibo', 'makemytrip', 'train', 'irctc'],
        'online_shopping': ['amazon', 'flipkart', 'myntra', 'ajio', 'meesho', 'online', 'ecommerce'],
        'groceries': ['bigbasket', 'blinkit', 'zepto', 'dunzo', 'grocery', 'supermarket', 'dmart', 'reliance fresh'],
        'fuel': ['petrol', 'diesel', 'fuel', 'hp', 'bharat petroleum', 'indian oil', 'shell'],
        'utilities': ['electricity', 'water', 'gas', 'broadband', 'jio', 'airtel', 'vodafone', 'bsnl', 'postpaid'],
        'entertainment': ['netflix', 'amazon prime', 'hotstar', 'spotify', 'youtube', 'cinema', 'movie', 'bookmyshow'],
        'insurance': ['insurance', 'policy', 'lic', 'hdfc life', 'icici prudential'],
        'education': ['school', 'college', 'course', 'tuition', 'udemy', 'coursera', 'education', 'books']
    }
    
    def __init__(self):
        self.transactions = []
    
    def import_csv(self, filepath: str, format_type: str = 'auto') -> List[Dict]:
        """Import transactions from CSV file"""
        
        print(f"\n📄 Importing transactions from: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            print(f"   Found {len(df)} transactions")
            
            # Detect format and parse accordingly
            if format_type == 'auto':
                format_type = self._detect_format(df)
                print(f"   Detected format: {format_type}")
            
            if format_type == 'bank_statement':
                self.transactions = self._parse_bank_statement(df)
            elif format_type == 'money_manager':
                self.transactions = self._parse_money_manager(df)
            elif format_type == 'generic':
                self.transactions = self._parse_generic(df)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            
            print(f"✅ Imported {len(self.transactions)} transactions\n")
            return self.transactions
            
        except Exception as e:
            print(f"❌ Error importing file: {e}")
            return []
    
    def _detect_format(self, df: pd.DataFrame) -> str:
        """Auto-detect CSV format"""
        columns = [c.lower() for c in df.columns]
        
        if 'transaction date' in columns or 'txn date' in columns:
            return 'bank_statement'
        elif 'account' in columns and 'amount' in columns:
            return 'money_manager'
        else:
            return 'generic'
    
    def _parse_bank_statement(self, df: pd.DataFrame) -> List[Dict]:
        """Parse bank statement format"""
        transactions = []
        
        # Common bank statement columns
        date_col = None
        desc_col = None
        amount_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'date' in col_lower:
                date_col = col
            elif 'description' in col_lower or 'narration' in col_lower or 'particulars' in col_lower:
                desc_col = col
            elif 'amount' in col_lower or 'debit' in col_lower or 'withdrawal' in col_lower:
                amount_col = col
        
        if not all([date_col, desc_col, amount_col]):
            raise ValueError("Could not identify required columns")
        
        for _, row in df.iterrows():
            amount = self._parse_amount(row[amount_col])
            if amount > 0:  # Only debit transactions
                transactions.append({
                    'date': row[date_col],
                    'description': str(row[desc_col]),
                    'amount': amount,
                    'category': self._categorize_transaction(str(row[desc_col]))
                })
        
        return transactions
    
    def _parse_money_manager(self, df: pd.DataFrame) -> List[Dict]:
        """Parse Money Manager export format"""
        transactions = []
        
        for _, row in df.iterrows():
            if row.get('Type', '').lower() == 'expense':
                transactions.append({
                    'date': row.get('Date', ''),
                    'description': row.get('Description', ''),
                    'amount': self._parse_amount(row.get('Amount', 0)),
                    'category': row.get('Category', 'other').lower().replace(' ', '_')
                })
        
        return transactions
    
    def _parse_generic(self, df: pd.DataFrame) -> List[Dict]:
        """Parse generic CSV with date, description, amount"""
        transactions = []
        
        for _, row in df.iterrows():
            amount = self._parse_amount(row.iloc[2] if len(row) > 2 else 0)
            if amount > 0:
                transactions.append({
                    'date': row.iloc[0],
                    'description': str(row.iloc[1] if len(row) > 1 else ''),
                    'amount': amount,
                    'category': self._categorize_transaction(str(row.iloc[1]) if len(row) > 1 else '')
                })
        
        return transactions
    
    def _parse_amount(self, amount) -> float:
        """Parse amount from string or number"""
        if isinstance(amount, (int, float)):
            return abs(float(amount))
        
        # Remove currency symbols and commas
        amount_str = str(amount).replace('₹', '').replace(',', '').replace('Rs', '').strip()
        
        try:
            return abs(float(amount_str))
        except:
            return 0.0
    
    def _categorize_transaction(self, description: str) -> str:
        """Categorize transaction based on description"""
        description_lower = description.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        return 'other'
    
    def calculate_monthly_spending(self, months: int = 1) -> Dict[str, float]:
        """Calculate average monthly spending by category"""
        
        if not self.transactions:
            return {}
        
        category_totals = {}
        
        for txn in self.transactions:
            category = txn['category']
            amount = txn['amount']
            
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += amount
        
        # Calculate average per month
        monthly_avg = {cat: total / months for cat, total in category_totals.items()}
        
        return monthly_avg
    
    def create_profile_from_transactions(self, profile_name: str, months: int = 3) -> SpendingProfile:
        """Create user profile from imported transactions"""
        
        print(f"\n📋 Creating profile '{profile_name}' from {len(self.transactions)} transactions...")
        
        monthly_spending = self.calculate_monthly_spending(months)
        
        profile = SpendingProfile(profile_name)
        
        # Map calculated spending to profile categories
        for category, amount in monthly_spending.items():
            if category in profile.monthly_spend:
                profile.monthly_spend[category] = round(amount, 2)
        
        total_spend = profile.get_total_monthly_spend()
        print(f"   Total monthly spend: ₹{total_spend:,.0f}")
        
        # Show top categories
        top_cats = profile.get_top_categories(3)
        print(f"\n   Top spending categories:")
        for cat, amt in top_cats:
            pct = (amt / total_spend) * 100 if total_spend > 0 else 0
            print(f"      • {cat.replace('_', ' ').title()}: ₹{amt:,.0f} ({pct:.1f}%)")
        
        # Save profile
        profile.save()
        
        return profile
    
    def generate_report(self) -> str:
        """Generate spending analysis report"""
        
        if not self.transactions:
            return "No transactions to analyze."
        
        monthly_spending = self.calculate_monthly_spending()
        total_spend = sum(monthly_spending.values())
        
        report = f"""# Expense Analysis Report

**Total Transactions:** {len(self.transactions)}
**Average Monthly Spend:** ₹{total_spend:,.0f}

## Category Breakdown

| Category | Monthly Spend | Percentage |
|----------|---------------|------------|
"""
        
        sorted_cats = sorted(monthly_spending.items(), key=lambda x: x[1], reverse=True)
        
        for category, amount in sorted_cats:
            pct = (amount / total_spend) * 100 if total_spend > 0 else 0
            report += f"| {category.replace('_', ' ').title()} | ₹{amount:,.0f} | {pct:.1f}% |\n"
        
        report += f"""\n**Total:** ₹{total_spend:,.0f} | 100%

---

*Generated by Credit Card Optimizer - Expense Importer*
"""
        
        return report


def main():
    """Example usage"""
    print("=" * 80)
    print("    📊 EXPENSE IMPORTER - TRANSACTION ANALYSIS")
    print("=" * 80)
    
    print("\n📝 Supported Formats:")
    print("   1. Bank Statement CSV (Date, Description, Amount)")
    print("   2. Money Manager Export")
    print("   3. Generic CSV (Date, Description, Amount)")
    
    print("\n💾 Sample Data Creation...")
    
    # Create sample transactions CSV
    sample_dir = Path("sample_data")
    sample_dir.mkdir(exist_ok=True)
    
    sample_file = sample_dir / "transactions_sample.csv"
    
    sample_data = [
        ['Date', 'Description', 'Amount'],
        ['2026-01-15', 'Zomato Food Order', '850'],
        ['2026-01-16', 'Amazon Shopping', '2500'],
        ['2026-01-17', 'Uber Ride', '350'],
        ['2026-01-18', 'BigBasket Grocery', '3200'],
        ['2026-01-19', 'Shell Petrol Pump', '2800'],
        ['2026-01-20', 'Netflix Subscription', '650'],
        ['2026-01-21', 'Flipkart Electronics', '15000'],
        ['2026-01-22', 'Swiggy Dinner', '920'],
        ['2026-01-23', 'Ola Auto', '180'],
        ['2026-01-24', 'Myntra Clothing', '4500'],
    ]
    
    with open(sample_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    print(f"✅ Created sample file: {sample_file}")
    
    # Import and analyze
    importer = ExpenseImporter()
    importer.import_csv(str(sample_file))
    
    # Generate report
    print("\n" + importer.generate_report())
    
    # Create profile
    profile = importer.create_profile_from_transactions("imported_profile", months=1)
    
    print("\n" + "=" * 80)
    print("✅ Import complete! Use this profile with structured_analyzer.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
