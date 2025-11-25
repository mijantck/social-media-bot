"""
Test Analytics - Add Sample Data
"""

from analytics import analytics
import random
from datetime import datetime, timedelta

print("🧪 Adding sample analytics data...")

# Sample users
users = [
    (12345, "john_doe", "John"),
    (67890, "jane_smith", "Jane"),
    (11111, "bob_wilson", "Bob"),
    (22222, "alice_jones", "Alice"),
    (33333, "charlie_brown", "Charlie"),
]

# Sample actions
actions = ["start", "help", "download", "caption", "hashtags", "image_analysis"]
platforms = ["Instagram", "YouTube", "TikTok", "Facebook"]
features = ["caption", "hashtags", "image_analysis"]

print("\n📊 Adding user activities...")
for i in range(50):
    user = random.choice(users)
    action = random.choice(actions)
    analytics.log_user_activity(
        user_id=user[0],
        username=user[1],
        first_name=user[2],
        action=action,
        details=f"Test action {i+1}"
    )

print("✅ Added 50 user activities")

print("\n💰 Adding API usage data...")
for i in range(30):
    user = random.choice(users)
    feature = random.choice(features)

    tokens = random.randint(100, 500)
    cost = tokens * 0.0000075  # Approximate cost

    analytics.log_api_usage(
        user_id=user[0],
        username=user[1],
        api_type="Gemini AI",
        feature=feature,
        tokens=tokens,
        cost=cost,
        success=random.choice([True, True, True, False]),  # 75% success rate
        error="Test error" if random.random() < 0.25 else None
    )

print("✅ Added 30 API calls")

print("\n📥 Adding download statistics...")
for i in range(40):
    user = random.choice(users)
    platform = random.choice(platforms)

    analytics.log_download(
        user_id=user[0],
        username=user[1],
        platform=platform,
        content_type="video",
        success=random.choice([True, True, True, False]),  # 75% success rate
        file_size=random.randint(1000000, 50000000)  # 1MB - 50MB
    )

print("✅ Added 40 downloads")

# Get and display summary
print("\n" + "="*50)
print("📊 ANALYTICS SUMMARY")
print("="*50)

stats = analytics.get_total_stats()
print(f"\n📈 Total Statistics:")
print(f"   Total Users: {stats['total_users']}")
print(f"   Total API Calls: {stats['total_api_calls']}")
print(f"   Total Cost: ${stats['total_cost']:.4f}")
print(f"   Total Downloads: {stats['total_downloads']}")
print(f"   Total Tokens: {stats['total_tokens']:,}")

today = analytics.get_today_stats()
print(f"\n📅 Today's Statistics:")
print(f"   Active Users: {today['today_users']}")
print(f"   API Calls: {today['today_api_calls']}")
print(f"   Cost: ${today['today_cost']:.4f}")
print(f"   Downloads: {today['today_downloads']}")

monthly = analytics.estimate_monthly_cost()
print(f"\n💵 Monthly Estimate: ${monthly:.2f}")

print("\n✅ Sample data added successfully!")
print("\n🚀 Now run: streamlit run analytics_dashboard.py")
print("   Or visit: http://localhost:8501")
