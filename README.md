# Social Media Manager Bot

A powerful Telegram bot that helps content creators download content from social media platforms and generate AI-powered captions and hashtags.

## Features

- **Content Downloader**: Download videos and images from:
  - Instagram (posts, reels, stories)
  - YouTube (videos, shorts)
  - TikTok (videos)
  - Facebook (videos)

- **AI Caption Generator**: Generate engaging captions using Google Gemini AI
- **Hashtag Suggestions**: Get trending and relevant hashtags
- **Multi-platform Support**: Works on Telegram (WhatsApp and Messenger coming soon)

## Target Audience

Perfect for content creators, influencers, and social media managers aged 15-35.

## Prerequisites

- Python 3.8 or higher
- Telegram account
- Google Gemini API key (free tier available)

## Installation

### Step 1: Clone or Download

```bash
cd social-media-bot
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name (e.g., "My Social Media Manager")
   - Choose a username (must end with 'bot', e.g., "my_socialmedia_bot")
4. Copy the **bot token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 4: Get Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the API key

### Step 5: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` file and add your keys:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 6: Run the Bot

```bash
python bot.py
```

You should see:
```
🤖 Bot is starting...
Press Ctrl+C to stop
```

## Usage

### Download Content

1. Open your bot on Telegram
2. Send `/start` to begin
3. Send any supported link:
   - `https://www.instagram.com/p/xxxxx/`
   - `https://www.youtube.com/watch?v=xxxxx`
   - `https://www.tiktok.com/@user/video/xxxxx`
   - `https://www.facebook.com/watch?v=xxxxx`

### Generate Captions

```
/caption sunset beach photography
```

### Get Hashtags

```
/hashtags fitness motivation workout
```

## Commands

- `/start` - Welcome message and features
- `/help` - Detailed help and examples
- `/caption <topic>` - Generate AI caption
- `/hashtags <topic>` - Generate hashtag suggestions

## Supported Platforms

| Platform  | Videos | Images | Stories | Status |
|-----------|--------|--------|---------|--------|
| Instagram | ✅     | ✅     | ✅      | Working |
| YouTube   | ✅     | ❌     | ❌      | Working |
| TikTok    | ✅     | ❌     | ❌      | Working |
| Facebook  | ✅     | ❌     | ❌      | Working |

## Troubleshooting

### Bot not responding

1. Check if bot is running (`python bot.py`)
2. Verify `TELEGRAM_BOT_TOKEN` in `.env` is correct
3. Make sure you started bot with `/start` command

### Download fails

1. Check internet connection
2. Some private accounts may not work
3. Very large files (>50MB) cannot be sent via Telegram

### AI features not working

1. Verify `GEMINI_API_KEY` in `.env` is correct
2. Check Gemini API quota at https://makersuite.google.com
3. Free tier has 15 requests per minute limit

### Instagram login required

For private accounts:
1. The bot uses anonymous access
2. Private content cannot be downloaded
3. Public posts work without login

## Project Structure

```
social-media-bot/
├── bot.py                  # Main bot application
├── downloaders.py          # Content download logic
├── caption_generator.py    # AI caption/hashtag generation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your credentials (not in git)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Cost Breakdown

- **Telegram Bot**: Free
- **Google Gemini API**: Free tier (15 requests/min)
- **Hosting** (when deploying):
  - PythonAnywhere: Free tier available
  - Railway: $5/month
  - Render: Free tier available

**Total**: $0-5/month

## Deployment (Optional)

### Deploy to Railway

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Add environment variables in Railway dashboard
4. Your bot will run 24/7

### Deploy to PythonAnywhere (Free)

1. Create account at https://www.pythonanywhere.com
2. Upload files via Files tab
3. Create bash console and run `pip install -r requirements.txt`
4. Run bot with "Always-on tasks" (paid) or scheduled tasks

## Roadmap

### Phase 1 (Current)
- ✅ Telegram bot
- ✅ Instagram downloader
- ✅ YouTube downloader
- ✅ TikTok downloader
- ✅ AI caption generator
- ✅ Hashtag suggestions

### Phase 2 (Coming Soon)
- ⏳ WhatsApp integration
- ⏳ Facebook Messenger integration
- ⏳ Post scheduler
- ⏳ Database for user preferences
- ⏳ Analytics dashboard

### Phase 3 (Future)
- ⏳ Multi-platform posting
- ⏳ Content calendar
- ⏳ Team collaboration
- ⏳ Advanced analytics

## Support

- Report bugs: Create an issue
- Feature requests: Create an issue
- Questions: Contact via Telegram

## License

MIT License - feel free to use for personal or commercial projects.

## Disclaimer

This bot is for educational purposes. Always respect copyright and terms of service of social media platforms. Only download content you have permission to use.

---

Made with ❤️ for content creators
