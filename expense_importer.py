#!/usr/bin/env python3
"""
Expense Importer
Import spending data from bank statements, expense trackers, and CSV files
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re

class ExpenseImporter:
    """Import and categorize expense data from various sources"""
    
    # Category mapping keywords
    CATEGORY_KEYWORDS = {
        'dining': ['restaurant', 'cafe', 'food', 'zomato', 'swiggy', 'dining', 'pizza', 'burger', 'starbucks', 'mcdonalds'],
        'travel': ['airline', 'flight', 'hotel', 'uber', 'ola', 'makemytrip', 'goibibo', 'booking', 'irctc', 'train'],
        'online_shopping': ['amazon', 'flipkart', 'myntra', 'ajio', 'meesho', 'shopping', 'ecommerce'],
        'groceries': ['supermarket', 'grocery', 'bigbasket', 'blinkit', 'instamart', 'dunzo', 'dmart', 'reliance fresh'],
        'fuel': ['petrol', 'diesel', 'fuel', 'hp', 'iocl', 'bharat petroleum', 'shell', 'gas station'],
        'utilities': ['electricity', 'water', 'gas', 'broadband', 'internet', 'mobile', 'recharge', 'postpaid'],
        'entertainment': ['netflix', 'prime', 'hotstar', 'spotify', 'movie', 'cinema', 'pvr', 'inox', 'gaming'],
        'healthcare': ['hospital', 'clinic', 'pharmacy', 'medical', 'apollo', 'doctor', 'lab test'],
        'education': ['school', 'college', 'university', 'course', 'books', 'tuition', 'udemy', 'coursera']
    }
    
    def __init__(self):
        self.transactions = []
        self.categorized_expenses = {}
    
    def import_csv(self, filepath: str, 
                   date_column: str = 'Date',
                   description_column: str = 'Description',
                   amount_column: str = 'Amount',
                   skip_header: bool = True) -> List[dict]:
        """Import transactions from CSV file"""
        
        transactions = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f) if skip_header else csv.reader(f)
            
            for row in reader:
                try:
                    transaction = {
                        'date': row[date_column] if isinstance(row, dict) else row[0],
                        'description': row[description_column] if isinstance(row, dict) else row[1],
                        'amount': self._parse_amount(row[amount_column] if isinstance(row, dict) else row[2]),
                        'category': 'other'
                    }
                    transactions.append(transaction)
                except Exception as e:
                    print(f"Warning: Skipping invalid row: {e}")
                    continue
        
        self.transactions.extend(transactions)
        return transactions
    
    def import_bank_statement(self, filepath: str, bank: str = 'generic') -> List[dict]:
        """Import from common bank statement formats"""
        
        # Bank-specific parsers
        if bank.lower() == 'hdfc':
            return self._parse_hdfc_statement(filepath)
        elif bank.lower() == 'sbi':
            return self._parse_sbi_statement(filepath)
        elif bank.lower() == 'icici':
            return self._parse_icici_statement(filepath)
        elif bank.lower() == 'axis':
            return self._parse_axis_statement(filepath)
        else:
            # Generic CSV format
            return self.import_csv(filepath)
    
    def _parse_hdfc_statement(self, filepath: str) -> List[dict]:
        """Parse HDFC Bank statement format"""
        # HDFC format: Date, Narration, Chq./Ref.No., Value Dt, Withdrawal Amt., Deposit Amt., Closing Balance
        return self.import_csv(
            filepath,
            date_column='Date',
            description_column='Narration',
            amount_column='Withdrawal Amt.'
        )
    
    def _parse_sbi_statement(self, filepath: str) -> List[dict]:
        """Parse SBI Bank statement format"""
        # SBI format varies, implement as needed
        return self.import_csv(filepath)
    
    def _parse_icici_statement(self, filepath: str) -> List[dict]:
        """Parse ICICI Bank statement format"""
        return self.import_csv(filepath)
    
    def _parse_axis_statement(self, filepath: str) -> List[dict]:
        """Parse Axis Bank statement format"""
        return self.import_csv(filepath)
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount from string, handle various formats"""
        # Remove currency symbols, commas
        amount_str = re.sub(r'[₹$,\s]', '', str(amount_str))
        
        try:
            return abs(float(amount_str))  # Use absolute value for expenses
        except ValueError:
            return 0.0
    
    def categorize_transactions(self) -> Dict[str, float]:
        """Automatically categorize all transactions"""
        
        categorized = {category: 0 for category in self.CATEGORY_KEYWORDS.keys()}
        categorized['other'] = 0
        
        for transaction in self.transactions:
            description = transaction['description'].lower()
            category = self._detect_category(description)
            
            transaction['category'] = category
            categorized[category] += transaction['amount']
        
        self.categorized_expenses = categorized
        return categorized
    
    def _detect_category(self, description: str) -> str:
        """Detect transaction category based on description"""
        
        description_lower = description.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        return 'other'
    
    def get_monthly_summary(self, month: Optional[int] = None, year: Optional[int] = None) -> Dict[str, float]:
        """Get spending summary for a specific month"""
        
        if month is None or year is None:
            now = datetime.now()
            month = now.month
            year = now.year
        
        monthly_expenses = {category: 0 for category in self.CATEGORY_KEYWORDS.keys()}
        monthly_expenses['other'] = 0
        
        for transaction in self.transactions:
            try:
                # Parse date
                trans_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
                
                if trans_date.month == month and trans_date.year == year:
                    category = transaction.get('category', 'other')
                    monthly_expenses[category] += transaction['amount']
            except:
                continue
        
        return monthly_expenses
    
    def export_to_profile(self, profile_name: str, num_months: int = 3) -> 'SpendingProfile':
        """Create spending profile from imported data"""
        
        from user_profile import SpendingProfile
        
        profile = SpendingProfile(profile_name)
        
        # Calculate average monthly spending
        total_expenses = {category: 0 for category in self.CATEGORY_KEYWORDS.keys()}
        total_expenses['other'] = 0
        
        for transaction in self.transactions:
            category = transaction.get('category', 'other')
            total_expenses[category] += transaction['amount']
        
        # Average over the number of months
        for category, total in total_expenses.items():
            avg_monthly = total / num_months if num_months > 0 else total
            if category in profile.monthly_spend:
                profile.monthly_spend[category] = round(avg_monthly, 2)
        
        return profile
    
    def export_summary(self, filepath: str = 'expense_summary.json'):
        """Export categorized summary to JSON"""
        
        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_transactions': len(self.transactions),
            'categorized_expenses': self.categorized_expenses,
            'total_amount': sum(self.categorized_expenses.values()),
            'transactions_sample': self.transactions[:10]  # First 10 for review
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return filepath


def create_sample_csv():
    """Create a sample expense CSV for testing"""
    
    sample_data = [
        ['Date', 'Description', 'Amount'],
        ['2026-01-15', 'Zomato Order #12345', '450'],
        ['2026-01-16', 'Amazon Shopping', '2500'],
        ['2026-01-17', 'Shell Petrol Pump', '3000'],
        ['2026-01-18', 'BigBasket Groceries', '1200'],
        ['2026-01-19', 'Starbucks Coffee', '350'],
        ['2026-01-20', 'MakeMyTrip Flight', '8500'],
        ['2026-01-21', 'Netflix Subscription', '649'],
        ['2026-01-22', 'Electricity Bill', '1500'],
        ['2026-01-23', 'Uber Ride', '280'],
        ['2026-01-24', 'Flipkart Electronics', '15000'],
    ]
    
    with open('sample_expenses.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    return 'sample_expenses.csv'


if __name__ == "__main__":
    print("=" * 80)
    print("    Credit Card Optimizer - Expense Importer")
    print("=" * 80)
    
    # Create sample CSV
    print("\nCreating sample expense file...")
    sample_file = create_sample_csv()
    print(f"✅ Created: {sample_file}")
    
    # Import and categorize
    print("\nImporting transactions...")
    importer = ExpenseImporter()
    transactions = importer.import_csv(sample_file)
    print(f"✅ Imported {len(transactions)} transactions")
    
    # Categorize
    print("\nCategorizing expenses...")
    categorized = importer.categorize_transactions()
    
    print("\nExpense Summary:")
    total = 0
    for category, amount in sorted(categorized.items(), key=lambda x: x[1], reverse=True):
        if amount > 0:
            print(f"  {category.replace('_', ' ').title()}: ₹{amount:,.0f}")
            total += amount
    print(f"\n  Total: ₹{total:,.0f}")
    
    # Export to profile
    print("\nCreating spending profile from imported data...")
    profile = importer.export_to_profile("Imported Profile", num_months=1)
    profile_path = profile.save()
    print(f"✅ Profile saved: {profile_path}")
    
    # Export summary
    summary_path = importer.export_summary()
    print(f"✅ Summary exported: {summary_path}")
