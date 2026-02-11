#!/usr/bin/env python3
"""
Complete Credit Card Optimization Workflow
Demonstrates all enhanced features in action
"""

import sys
sys.path.insert(0, '..')

from user_profile import SpendingProfile, create_sample_profile
from expense_importer import ExpenseImporter, create_sample_csv
from structured_analyzer import StructuredAnalyzer
from portfolio_optimizer import PortfolioOptimizer
from milestone_tracker import MilestoneTracker
from card_data_fetcher import CardDataFetcher

print("="*100)
print(" " * 30 + "💳 COMPLETE CREDIT CARD OPTIMIZATION WORKFLOW 💳")
print("="*100)
print()
print("🎉 This example demonstrates ALL enhanced features:")
print("   1. User Spending Profiles")
print("   2. Expense Import & Categorization")
print("   3. Structured AI Analysis (JSON + Markdown)")
print("   4. Multi-Card Portfolio Optimization")
print("   5. Milestone Progress Tracking")
print("   6. Latest Card Data Fetching")
print()
print("="*100)
print()

# =============================================================================
# STEP 1: CREATE SAMPLE EXPENSE DATA
# =============================================================================
print("📊 STEP 1: Creating Sample Expense Data")
print("-" * 100)

sample_csv = create_sample_csv()
print(f"✅ Created sample CSV: {sample_csv}")
print()

# =============================================================================
# STEP 2: IMPORT & CATEGORIZE EXPENSES
# =============================================================================
print("📊 STEP 2: Importing & Categorizing Expenses")
print("-" * 100)

importer = ExpenseImporter()
transactions = importer.import_csv(sample_csv)
print(f"✅ Imported {len(transactions)} transactions")

categorized = importer.categorize_transactions()
print("\n📋 Expense Breakdown:")
for category, amount in sorted(categorized.items(), key=lambda x: x[1], reverse=True):
    if amount > 0:
        print(f"   {category.replace('_', ' ').title():20s}: ₹{amount:>8,.0f}")

print(f"\n   {'Total':20s}: ₹{sum(categorized.values()):>8,.0f}")
print()

# =============================================================================
# STEP 3: CREATE SPENDING PROFILE FROM DATA
# =============================================================================
print("📁 STEP 3: Creating Spending Profile")
print("-" * 100)

profile = importer.export_to_profile("Demo User", num_months=1)

# Enhance profile with preferences
profile.preferences['max_annual_fee'] = 15000
profile.preferences['reward_type'] = 'points'
profile.preferences['lounge_access_required'] = True
profile.preferences['international_usage'] = True

profile.financial_profile['annual_income'] = 1200000
profile.financial_profile['age'] = 32
profile.financial_profile['occupation'] = 'Software Engineer'
profile.financial_profile['city'] = 'Bangalore'

profile_path = profile.save()
print(f"✅ Profile saved: {profile_path}")
print(f"   Total Monthly Spend: ₹{profile.get_total_monthly_spend():,.0f}")
print(f"   Total Annual Spend: ₹{profile.get_total_annual_spend():,.0f}")
print("\n🎯 Top 3 Spending Categories:")
for category, amount in profile.get_top_categories(3):
    print(f"   {category.replace('_', ' ').title():20s}: ₹{amount:>8,.0f}")
print()

# =============================================================================
# STEP 4: GET AI RECOMMENDATIONS (STRUCTURED)
# =============================================================================
print("🤖 STEP 4: Getting AI-Powered Recommendations")
print("-" * 100)
print("🔄 Analyzing with AI... (this may take 30-60 seconds)")
print()

analyzer = StructuredAnalyzer()
result = analyzer.analyze_with_profile(profile)

if result.get('success', True):
    print("✅ AI analysis complete!")
    print(f"   Model used: {result.get('model_used', 'Unknown')}")
    
    # Save outputs
    json_path, md_path = analyzer.save_both()
    print(f"\n💾 Outputs saved:")
    print(f"   JSON: {json_path}")
    print(f"   Markdown: {md_path}")
    
    # Show structured data preview
    structured = result.get('structured_recommendations', {})
    if structured.get('primary_card'):
        print("\n🎯 Primary Recommendation:")
        primary = structured['primary_card']
        if primary.get('name'):
            print(f"   Card: {primary['name']}")
        if primary.get('annual_fee'):
            print(f"   Annual Fee: ₹{primary['annual_fee']:,.0f}")
        if primary.get('reward_rate'):
            print(f"   Reward Rate: {primary['reward_rate']}%")
    
    roi = result.get('roi_calculations', {})
    if roi:
        print("\n💰 ROI Summary:")
        if roi.get('total_annual_fees'):
            print(f"   Annual Fees: ₹{roi['total_annual_fees']:,.0f}")
        if roi.get('estimated_rewards'):
            print(f"   Est. Rewards: ₹{roi['estimated_rewards']:,.0f}")
        if roi.get('net_value'):
            print(f"   Net Value: ₹{roi['net_value']:,.0f}")
else:
    print(f"❌ AI analysis failed: {result.get('error')}")

print()

# =============================================================================
# STEP 5: OPTIMIZE MULTI-CARD PORTFOLIO
# =============================================================================
print("🎯 STEP 5: Finding Optimal Card Portfolio")
print("-" * 100)
print("🔍 Analyzing all card combinations...")
print()

optimizer = PortfolioOptimizer()
portfolios = optimizer.find_optimal_portfolio(
    profile,
    max_cards=3,
    max_total_fee=25000
)

print("✅ Portfolio optimization complete!")
print(f"   Found {len(portfolios)} optimal portfolios")
print("\n🏆 Top 3 Portfolio Recommendations:")
print()

for i, portfolio in enumerate(portfolios[:3], 1):
    print(f"#{i}. {' + '.join(portfolio['cards'])}")
    print(f"   Total Fees: ₹{portfolio['total_fee']:,.0f}")
    print(f"   Total Rewards: ₹{portfolio['total_rewards']:,.0f}")
    print(f"   Net Value: ₹{portfolio['net_value']:,.0f}")
    print(f"   ROI: {portfolio['roi_percentage']:.1f}%")
    print()

# Save full report
report = optimizer.generate_report(profile, max_cards=3)
from pathlib import Path
from datetime import datetime
output_dir = Path('../recommendations')
output_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
portfolio_path = output_dir / f"{timestamp}-portfolio-optimization.md"
with open(portfolio_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"💾 Full portfolio report saved: {portfolio_path}")
print()

# =============================================================================
# STEP 6: TRACK MILESTONE PROGRESS
# =============================================================================
print("🏆 STEP 6: Tracking Milestone Progress")
print("-" * 100)

tracker = MilestoneTracker()

# Simulate spending on different cards
print("💳 Simulating card spending...")
tracker.update_spend('HDFC Infinia', 250000)  # ₹2.5L spent
tracker.update_spend('Axis Magnus', 75000)    # ₹75K spent
tracker.update_spend('SBI Cashback', 150000)  # ₹1.5L spent

print("✅ Spending updated")
print("\n🎯 Milestone Status:")
print()

# Show progress for each card
for card_name in ['HDFC Infinia', 'Axis Magnus', 'SBI Cashback']:
    progress_data = tracker.get_card_progress(card_name)
    if progress_data:
        print(f"\n{card_name}:")
        for milestone in progress_data:
            status = "✅" if milestone['achieved'] else "🔵"
            print(f"   {status} {milestone['name']:40s} {milestone['progress']:>5.1f}%")

# Save milestone report
milestone_path = tracker.save_report()
print(f"\n💾 Milestone report saved: {milestone_path}")
print()

# =============================================================================
# STEP 7: FETCH LATEST CARD DATA
# =============================================================================
print("🔄 STEP 7: Fetching Latest Card Data")
print("-" * 100)

fetcher = CardDataFetcher()

print("🔍 Fetching from r/CreditCardsIndia...")
posts = fetcher.fetch_reddit_discussions(limit=5)

if posts:
    print(f"✅ Found {len(posts)} recent discussions")
    print("\n💬 Top Discussions:")
    for i, post in enumerate(posts[:3], 1):
        print(f"   {i}. {post['title'][:80]}...")
        print(f"      Score: {post['score']} | URL: {post['url']}")
else:
    print("⚠️ Could not fetch Reddit data (API limit or connection issue)")

# Generate data summary
summary = fetcher.generate_data_summary()
summary_path = output_dir / f"{timestamp}-card-data-summary.md"
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"\n💾 Data summary saved: {summary_path}")
print()

# =============================================================================
# SUMMARY
# =============================================================================
print("="*100)
print(" " * 35 + "🎉 WORKFLOW COMPLETE! 🎉")
print("="*100)
print()
print("📊 Summary of Generated Files:")
print(f"   1. Spending Profile: {profile_path}")
print(f"   2. AI Analysis (JSON): {json_path}")
print(f"   3. AI Analysis (Markdown): {md_path}")
print(f"   4. Portfolio Optimization: {portfolio_path}")
print(f"   5. Milestone Tracker: {milestone_path}")
print(f"   6. Card Data Summary: {summary_path}")
print()
print("✨ Next Steps:")
print("   1. Review the AI recommendations in the Markdown file")
print("   2. Check the JSON file for programmatic access")
print("   3. Analyze the portfolio optimization for best card combos")
print("   4. Track your milestone progress monthly")
print("   5. Import your actual bank statements using expense_importer.py")
print()
print("🚀 Pro Tip: Run this workflow monthly to optimize your credit card strategy!")
print()
print("="*100)
