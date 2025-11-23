# 🎮 Dashboard Guide

## Quick Start

### Launch Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## Features

### 🏠 Home Page

**Bot Status Monitor:**
- Real-time bot status (Online/Offline)
- Process ID display
- Auto-refresh option

**Bot Controls:**
- ▶️ START BOT - Launch your Telegram bot
- ⏹️ STOP BOT - Stop the running bot
- 🔄 RESTART BOT - Restart bot (stop + start)

**System Resources:**
- CPU usage monitoring
- Memory usage tracking
- Disk space monitoring

**Quick Information:**
- Bot features overview
- Important reminders
- Best practices

---

### ⚙️ Settings Page

**API Credentials:**
- View masked Telegram Bot Token
- View masked Gemini API Key
- (Actual values stored in `.env` file)

**File Management:**
- View downloaded files count
- Clean downloads folder
- Free up disk space

**Deployment Info:**
- Cloud deployment options
- Links to deployment guide

---

### 📊 Statistics Page

**Coming Soon:**
- Total users count
- Total downloads
- Captions generated
- Bot uptime
- Error tracking

*Note: Requires database integration*

---

### 📝 Logs Page

**Coming Soon:**
- Real-time bot logs
- Error logs
- Activity history

*Note: Currently view logs by running `python bot.py` in terminal*

---

## Dashboard Controls Explained

### How It Works

When you click **START BOT**:
```
Dashboard → Runs bot.py in background → Bot goes online
```

When you click **STOP BOT**:
```
Dashboard → Kills bot.py process → Bot goes offline
```

### Important Notes

1. **Dashboard vs Bot:**
   - Dashboard: Web UI for control (localhost:8501)
   - Bot: Telegram bot service (bot.py)
   - These are **separate processes**

2. **Keep Dashboard Running:**
   - To control bot, dashboard must be open
   - Close dashboard = lose control panel (bot keeps running)
   - Recommended: Keep dashboard tab open

3. **PC Requirements:**
   - PC must be ON for bot to work
   - Internet connection required
   - Dashboard uses minimal resources

---

## Workflow

### Normal Usage:

```
1. Open Terminal
2. Run: streamlit run dashboard.py
3. Dashboard opens in browser
4. Click "START BOT" button
5. Bot goes online on Telegram
6. Monitor status in dashboard
7. When done, click "STOP BOT"
```

### Development Workflow:

```
1. Code changes in bot.py
2. Click "RESTART BOT" in dashboard
3. Bot reloads with new code
4. Test on Telegram
5. Repeat
```

---

## Tips

### Auto Refresh
- Enable "Auto Refresh" checkbox
- Dashboard updates every 5 seconds
- See real-time status changes

### System Monitoring
- Watch CPU/Memory usage
- If high usage, investigate
- Consider upgrading PC or deploying to cloud

### Clean Downloads
- Downloads folder fills up over time
- Use "Clean Downloads Folder" button
- Frees up disk space

---

## Troubleshooting

### Dashboard won't start

**Error:** `streamlit: command not found`

**Solution:**
```bash
pip install streamlit psutil
# or
./venv/bin/pip install streamlit psutil
```

---

### Bot won't start from dashboard

**Possible causes:**
1. `.env` file missing or incorrect
2. Dependencies not installed
3. Port already in use

**Solution:**
```bash
# Test bot manually first
python bot.py

# Check .env file
cat .env

# Verify TOKEN is set
```

---

### "Connection Error" in browser

**Solution:**
```bash
# Kill any existing streamlit processes
pkill -f streamlit

# Restart dashboard
streamlit run dashboard.py
```

---

## Deploy Dashboard to Cloud

If you want to access dashboard remotely:

### Option 1: Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Deploy dashboard.py
4. Access from anywhere

### Option 2: VPS with Port Forwarding

```bash
# Run on VPS
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0

# Access via
http://your-vps-ip:8501
```

**Security Warning:** Add authentication if exposing dashboard publicly!

---

## Next Steps

1. **Add Database:** Track statistics (PostgreSQL/SQLite)
2. **Add Authentication:** Secure dashboard access
3. **Add Logs:** Real-time log viewer
4. **Add Analytics:** Usage charts and graphs
5. **Multi-bot Support:** Control multiple bots

---

## Screenshots

### Home Page
- Bot status indicator (Green/Red)
- Control buttons (Start/Stop/Restart)
- System resources (CPU/Memory/Disk)

### Settings Page
- API credentials (masked)
- File management
- Deployment options

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `R` | Refresh page |
| `M` | Open menu |
| `K` | Open command palette |

---

## Support

**Issues?**
- Check bot works: `python bot.py`
- Check dashboard dependencies: `pip list | grep streamlit`
- Review logs in terminal

**Feature Requests?**
- Open an issue
- Suggest improvements

---

Happy Bot Managing! 🚀
