# Railway Deployment Guide

## Quick Deploy to Railway

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit for Railway deployment"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Railway

#### For Bot Service:
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will detect Python automatically
5. Add Environment Variables:
   - `TELEGRAM_BOT_TOKEN` = your_bot_token
   - `GEMINI_API_KEY` = your_gemini_key
6. Deploy!

#### For Dashboard (Optional - Separate Service):
1. In same project, click "+ New Service"
2. Select same GitHub repo
3. Change start command to: `streamlit run dashboard.py --server.port=$PORT --server.headless=true`
4. Add same environment variables
5. Deploy!

### Step 3: Set Environment Variables

In Railway dashboard → Variables tab:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

### Important Notes:

1. **Database**: SQLite file will persist in Railway's volume storage
2. **Downloads folder**: Will be created automatically
3. **Free Tier**: $5 credit/month (usually enough for small bots)
4. **Always-on**: Bot will run 24/7 until credit exhausted

### Monitoring:
- Check logs in Railway dashboard
- View metrics in "Observability" tab
- Monitor credit usage in "Usage" tab

### Cost Optimization:
- Bot uses minimal resources (~50MB RAM)
- Estimated cost: $3-5/month
- Dashboard optional (can run locally)

### Troubleshooting:

**Bot not responding:**
- Check logs for errors
- Verify environment variables set correctly
- Check if service is running

**Out of memory:**
- Downloads folder cleanup may be needed
- Consider adding cron job for cleanup

**Database issues:**
- Railway auto-creates persistent volume
- Database resets if service redeployed without volume

### Support:
Contact: @YourUsername
