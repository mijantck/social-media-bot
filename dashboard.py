"""
Social Media Bot - Control Dashboard
Web-based UI to control and monitor your Telegram bot
"""

import streamlit as st
import subprocess
import psutil
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Social Media Bot Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .status-online {
        color: #10b981;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .status-offline {
        color: #ef4444;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def check_bot_status():
    """Check if bot is running"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'python' in cmdline[0].lower() and 'bot.py' in ' '.join(cmdline):
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, None

def start_bot():
    """Start the bot"""
    try:
        # Get the correct Python executable from virtual environment
        python_path = './venv/bin/python'

        # Check if venv exists, otherwise use system python
        if not os.path.exists(python_path):
            import sys
            python_path = sys.executable

        # Start bot in background
        process = subprocess.Popen(
            [python_path, 'bot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        time.sleep(2)  # Wait for bot to start
        return True, f"Bot started successfully! (PID: {process.pid})"
    except Exception as e:
        return False, f"Error starting bot: {str(e)}"

def stop_bot():
    """Stop the bot"""
    try:
        subprocess.run(['pkill', '-f', 'python.*bot.py'], check=False)
        time.sleep(1)
        return True, "Bot stopped successfully!"
    except Exception as e:
        return False, f"Error stopping bot: {str(e)}"

def get_bot_info():
    """Get bot information"""
    token = os.getenv('TELEGRAM_BOT_TOKEN', 'Not set')
    gemini_key = os.getenv('GEMINI_API_KEY', 'Not set')

    # Mask sensitive info
    if token != 'Not set':
        token = token[:10] + '...' + token[-5:]
    if gemini_key != 'Not set':
        gemini_key = gemini_key[:10] + '...' + gemini_key[-5:]

    return {
        'token': token,
        'gemini_key': gemini_key,
        'bot_username': '@MySocialMediaTckBot'
    }

def get_system_stats():
    """Get system resource usage"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        'cpu': cpu_percent,
        'memory': memory.percent,
        'disk': disk.percent
    }

# Main Dashboard
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Social Media Bot Dashboard</h1>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/telegram-app.png", width=100)
        st.title("Navigation")
        page = st.radio("Go to", ["🏠 Home", "⚙️ Settings", "📊 Statistics", "📝 Logs"])

        st.divider()
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

        # Auto refresh
        if st.button("🔄 Refresh"):
            st.rerun()

    # Check bot status
    is_running, pid = check_bot_status()

    # Home Page
    if page == "🏠 Home":
        # Status Section
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.subheader("Bot Status")
            if is_running:
                st.markdown(f'<p class="status-online">🟢 ONLINE</p>', unsafe_allow_html=True)
                st.caption(f"Process ID: {pid}")
            else:
                st.markdown(f'<p class="status-offline">🔴 OFFLINE</p>', unsafe_allow_html=True)
                st.caption("Bot is not running")

        with col2:
            st.subheader("Quick Stats")
            bot_info = get_bot_info()
            st.metric("Bot Username", bot_info['bot_username'])

        with col3:
            st.subheader("Auto Refresh")
            auto_refresh = st.checkbox("Enable", value=False)
            if auto_refresh:
                time.sleep(5)
                st.rerun()

        st.divider()

        # Control Buttons
        st.subheader("🎮 Bot Controls")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("▶️ START BOT", type="primary", disabled=is_running):
                with st.spinner("Starting bot..."):
                    success, message = start_bot()
                    if success:
                        st.success(message)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)

        with col2:
            if st.button("⏹️ STOP BOT", type="secondary", disabled=not is_running):
                with st.spinner("Stopping bot..."):
                    success, message = stop_bot()
                    if success:
                        st.success(message)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)

        with col3:
            if st.button("🔄 RESTART BOT", disabled=not is_running):
                with st.spinner("Restarting bot..."):
                    stop_bot()
                    time.sleep(2)
                    success, message = start_bot()
                    if success:
                        st.success("Bot restarted successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)

        st.divider()

        # System Resources
        st.subheader("💻 System Resources")
        stats = get_system_stats()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("CPU Usage", f"{stats['cpu']}%")
            st.progress(stats['cpu'] / 100)

        with col2:
            st.metric("Memory Usage", f"{stats['memory']:.1f}%")
            st.progress(stats['memory'] / 100)

        with col3:
            st.metric("Disk Usage", f"{stats['disk']:.1f}%")
            st.progress(stats['disk'] / 100)

        st.divider()

        # Quick Info
        st.subheader("ℹ️ Bot Information")
        info_col1, info_col2 = st.columns(2)

        with info_col1:
            st.info("""
            **Features:**
            - Download from Instagram, YouTube, TikTok
            - AI Caption Generation
            - Hashtag Suggestions
            - Multi-platform support
            """)

        with info_col2:
            st.warning("""
            **Important:**
            - Keep your PC online for bot to work
            - Don't share your .env file
            - Monitor resource usage
            - Deploy to cloud for 24/7 operation
            """)

    # Settings Page
    elif page == "⚙️ Settings":
        st.header("⚙️ Settings")

        bot_info = get_bot_info()

        st.subheader("🔑 API Credentials")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Telegram Bot Token", value=bot_info['token'], disabled=True, type="password")
            st.caption("Stored in .env file")

        with col2:
            st.text_input("Gemini API Key", value=bot_info['gemini_key'], disabled=True, type="password")
            st.caption("Stored in .env file")

        st.divider()

        st.subheader("📁 File Management")

        if os.path.exists('downloads'):
            files = os.listdir('downloads')
            st.info(f"Downloaded files: {len(files)}")

            if files:
                if st.button("🗑️ Clean Downloads Folder"):
                    for file in files:
                        try:
                            os.remove(os.path.join('downloads', file))
                        except:
                            pass
                    st.success("Downloads folder cleaned!")
                    st.rerun()
        else:
            st.info("Downloads folder: Empty")

        st.divider()

        st.subheader("🚀 Deployment Options")
        st.info("""
        **Deploy to Cloud for 24/7 operation:**
        - Railway (Recommended) - $5/month
        - Render (Free tier available)
        - PythonAnywhere (Free tier available)

        Check `DEPLOYMENT.md` for detailed instructions.
        """)

    # Statistics Page
    elif page == "📊 Statistics":
        st.header("📊 Statistics")

        st.info("Statistics tracking coming soon! This will include:")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Users", "Coming Soon")
            st.metric("Total Downloads", "Coming Soon")
            st.metric("Total Captions Generated", "Coming Soon")

        with col2:
            st.metric("Uptime", "Coming Soon")
            st.metric("Messages Processed", "Coming Soon")
            st.metric("Errors", "Coming Soon")

        st.caption("💡 To enable statistics, consider adding a database (PostgreSQL/SQLite)")

    # Logs Page
    elif page == "📝 Logs":
        st.header("📝 Logs")

        st.info("Real-time logging coming soon!")

        if st.button("View Bot Output"):
            st.code("""
Bot logs will appear here when bot is running.
For now, run 'python bot.py' in terminal to see logs.
            """)

        st.caption("💡 Tip: Run `python bot.py` in terminal to see real-time logs")

if __name__ == '__main__':
    main()
