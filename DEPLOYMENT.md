# Deployment Guide

Run your bot 24/7 in the cloud!

## Option 1: Railway (Recommended - $5/month)

### Pros
- Easy setup
- Automatic deployments
- 24/7 uptime
- Good for beginners

### Steps

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your bot repository

3. **Add Environment Variables**
   - Go to project → Variables
   - Add:
     - `TELEGRAM_BOT_TOKEN`: your_token
     - `GEMINI_API_KEY`: your_key

4. **Create `Procfile`**
   ```bash
   worker: python bot.py
   ```

5. **Create `runtime.txt`**
   ```
   python-3.11.0
   ```

6. **Deploy**
   - Railway will auto-deploy
   - Check logs to ensure it's running

**Cost**: $5/month (includes $5 free credit monthly)

---

## Option 2: Render (Free Tier)

### Pros
- Free tier available
- Good performance
- Easy setup

### Steps

1. **Create Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **New Web Service**
   - Click "New +"
   - Select "Background Worker"
   - Connect repository

3. **Configure**
   - Name: social-media-bot
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

4. **Environment Variables**
   - Add `TELEGRAM_BOT_TOKEN`
   - Add `GEMINI_API_KEY`

5. **Deploy**
   - Click "Create Web Service"

**Cost**: Free (with limitations) or $7/month

---

## Option 3: PythonAnywhere (Free Tier)

### Pros
- Free tier available
- Simple for beginners
- No credit card required

### Cons
- Free tier has limitations
- Manual updates required

### Steps

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Files**
   - Go to "Files" tab
   - Upload all your bot files
   - Or use git clone in console

3. **Install Dependencies**
   - Open Bash console
   - Run:
     ```bash
     pip3 install --user -r requirements.txt
     ```

4. **Create .env File**
   - Create `.env` in Files tab
   - Add your tokens

5. **Run Bot**

   **For Free Tier** (manual start):
   - Open console
   - Run `python3 bot.py`
   - Bot stops when you close browser

   **For Paid Tier** ($5/month):
   - Go to "Tasks" tab
   - Create "Always-on task"
   - Command: `python3 /home/username/bot.py`
   - Bot runs 24/7

**Cost**: Free (limited) or $5/month

---

## Option 4: VPS (DigitalOcean, Linode, etc.)

### Pros
- Full control
- Best performance
- Can run multiple bots

### Cons
- Requires Linux knowledge
- More setup work

### Quick Setup (Ubuntu)

```bash
# 1. SSH into VPS
ssh root@your_server_ip

# 2. Install Python
apt update
apt install python3 python3-pip git -y

# 3. Clone your project
git clone https://github.com/yourusername/social-media-bot.git
cd social-media-bot

# 4. Install dependencies
pip3 install -r requirements.txt

# 5. Create .env file
nano .env
# Add your tokens, save (Ctrl+X, Y, Enter)

# 6. Test bot
python3 bot.py

# 7. Run with systemd (auto-restart)
sudo nano /etc/systemd/system/telegram-bot.service
```

Add this to the service file:
```ini
[Unit]
Description=Social Media Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/social-media-bot
ExecStart=/usr/bin/python3 /root/social-media-bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f
```

**Cost**: $5-10/month (DigitalOcean, Linode, Vultr)

---

## Comparison

| Platform        | Cost/Month | Setup  | Free Tier | Best For         |
|----------------|------------|--------|-----------|------------------|
| Railway        | $5         | Easy   | $5 credit | Beginners        |
| Render         | Free-$7    | Easy   | ✅        | Hobby projects   |
| PythonAnywhere | Free-$5    | Easy   | ✅        | Testing          |
| VPS            | $5-10      | Medium | ❌        | Advanced users   |

---

## Monitoring Your Bot

### Check if bot is running:

**Railway/Render:**
- Check dashboard logs

**PythonAnywhere:**
- Go to console and check process

**VPS:**
```bash
sudo systemctl status telegram-bot
```

### View Logs:

**Railway/Render:**
- Built-in logs in dashboard

**VPS:**
```bash
sudo journalctl -u telegram-bot -f
```

### Restart Bot:

**Railway/Render:**
- Click "Restart" in dashboard

**VPS:**
```bash
sudo systemctl restart telegram-bot
```

---

## Domain Setup (Optional)

If you want a custom domain for your bot's landing page:

1. Buy domain (Namecheap, GoDaddy: $10/year)
2. Create simple landing page
3. Point domain to your hosting
4. Add SSL certificate (Let's Encrypt - free)

---

## Scaling Tips

When your bot grows:

1. **Add Database**
   - PostgreSQL for user data
   - Redis for caching

2. **Use Queue System**
   - Celery for heavy tasks
   - Background workers for downloads

3. **Add Analytics**
   - Track usage stats
   - Monitor performance

4. **Load Balancing**
   - Multiple bot instances
   - Distribute load

---

## Security Checklist

- ✅ Keep `.env` file secure (never commit to git)
- ✅ Use strong tokens
- ✅ Enable 2FA on hosting account
- ✅ Regular backups
- ✅ Monitor logs for errors
- ✅ Update dependencies regularly

---

## Support

Having deployment issues?

1. Check bot logs for errors
2. Verify environment variables
3. Test locally first (`python bot.py`)
4. Check hosting platform status
5. Review documentation of your hosting provider

---

Happy deploying! 🚀
