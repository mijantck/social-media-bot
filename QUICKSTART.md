# Quick Start Guide

Get your bot running in 5 minutes!

## 1. Install Dependencies

```bash
cd social-media-bot
pip install -r requirements.txt
```

## 2. Create Telegram Bot

1. Open Telegram → Search `@BotFather`
2. Send: `/newbot`
3. Name: `My Social Media Bot`
4. Username: `my_socialmedia_bot` (must end with 'bot')
5. **Copy the token** (example: `1234567890:ABCdefGHI...`)

## 3. Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. **Copy the key**

## 4. Setup Environment

```bash
cp .env.example .env
```

Edit `.env` and paste your keys:
```
TELEGRAM_BOT_TOKEN=paste_your_telegram_token_here
GEMINI_API_KEY=paste_your_gemini_key_here
```

## 5. Run Bot

```bash
python bot.py
```

Should see:
```
🤖 Bot is starting...
Press Ctrl+C to stop
```

## 6. Test It!

1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Try sending an Instagram link!

Example: `https://www.instagram.com/p/xxxxx/`

## Common First Commands

```
/start          - See welcome message
/help           - Get help
/caption travel - Generate caption
/hashtags food  - Get hashtags
```

## Troubleshooting

**Bot doesn't respond?**
- Make sure bot is running (`python bot.py`)
- Check if you sent `/start` first
- Verify token in `.env` is correct

**Can't install dependencies?**
```bash
# Try with pip3
pip3 install -r requirements.txt

# Or create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Python version error?**
```bash
# Check Python version (need 3.8+)
python --version

# If too old, install Python 3.8+
# Visit: https://www.python.org/downloads/
```

Need more help? Read `README.md` for detailed documentation!
