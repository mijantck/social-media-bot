"""
Setup Verification Script
Run this to test if everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv

print("🔍 Checking your bot setup...\n")

# Load environment variables
load_dotenv()

# Track errors
errors = []
warnings = []

# Check Python version
print("1. Checking Python version...")
if sys.version_info < (3, 8):
    errors.append("Python 3.8+ required. You have: " + sys.version)
    print("   ❌ Python version too old")
else:
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}")

# Check environment variables
print("\n2. Checking environment variables...")

telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
if not telegram_token or telegram_token == 'your_telegram_bot_token_here':
    errors.append("TELEGRAM_BOT_TOKEN not set in .env file")
    print("   ❌ Telegram bot token missing")
else:
    print(f"   ✅ Telegram token found ({telegram_token[:10]}...)")

gemini_key = os.getenv('GEMINI_API_KEY')
if not gemini_key or gemini_key == 'your_gemini_api_key_here':
    warnings.append("GEMINI_API_KEY not set (AI features will be disabled)")
    print("   ⚠️  Gemini API key missing (AI features disabled)")
else:
    print(f"   ✅ Gemini API key found ({gemini_key[:10]}...)")

# Check dependencies
print("\n3. Checking required packages...")

required_packages = [
    ('telegram', 'python-telegram-bot'),
    ('yt_dlp', 'yt-dlp'),
    ('instaloader', 'instaloader'),
    ('google.generativeai', 'google-generativeai'),
    ('dotenv', 'python-dotenv'),
]

for module_name, package_name in required_packages:
    try:
        __import__(module_name)
        print(f"   ✅ {package_name}")
    except ImportError:
        errors.append(f"Package '{package_name}' not installed")
        print(f"   ❌ {package_name} - run: pip install {package_name}")

# Check file structure
print("\n4. Checking project files...")

required_files = [
    'bot.py',
    'downloaders.py',
    'caption_generator.py',
    'requirements.txt',
    '.env',
]

for filename in required_files:
    if os.path.exists(filename):
        print(f"   ✅ {filename}")
    else:
        if filename == '.env':
            errors.append(".env file missing - copy from .env.example")
        else:
            errors.append(f"{filename} missing")
        print(f"   ❌ {filename}")

# Summary
print("\n" + "="*50)
if errors:
    print("❌ SETUP INCOMPLETE\n")
    print("Errors found:")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")

    print("\nFix these issues then run: python bot.py")

elif warnings:
    print("⚠️  SETUP COMPLETE (with warnings)\n")
    print("Warnings:")
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")

    print("\nYou can run the bot, but some features may be limited.")
    print("Run: python bot.py")

else:
    print("✅ SETUP COMPLETE!\n")
    print("Everything looks good!")
    print("Run your bot with: python bot.py")

print("="*50)
