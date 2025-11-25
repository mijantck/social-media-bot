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
import pandas as pd
import plotly.express as px
from analytics import Analytics

# Load environment variables
load_dotenv()

# Initialize analytics
analytics = Analytics()

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
        # Kill all bot processes
        result = subprocess.run(['pkill', '-9', '-f', 'python.*bot.py'],
                              capture_output=True, text=True)
        time.sleep(2)  # Give it time to fully stop

        # Verify it's stopped
        is_running, _ = check_bot_status()
        if is_running:
            return False, "Bot is still running. Try again."

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
        page = st.radio("Go to", ["🏠 Home", "⚙️ Settings", "📊 Analytics", "📋 Tasks", "📝 Logs"])

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

    # Analytics Page
    elif page == "📊 Analytics":
        st.header("📊 Bot Analytics & Cost Tracking")

        # Get stats
        total_stats = analytics.get_total_stats()
        today_stats = analytics.get_today_stats()
        monthly_estimate = analytics.estimate_monthly_cost()

        # Overview Section
        st.subheader("📈 Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Users",
                f"{total_stats['total_users']}",
                f"+{today_stats['today_users']} today"
            )

        with col2:
            st.metric(
                "Total API Calls",
                f"{total_stats['total_api_calls']:,}",
                f"+{today_stats['today_api_calls']} today"
            )

        with col3:
            st.metric(
                "Total Cost",
                f"${total_stats['total_cost']:.4f}",
                f"+${today_stats['today_cost']:.4f} today"
            )

        with col4:
            st.metric(
                "Monthly Estimate",
                f"${monthly_estimate:.2f}",
                "Based on last 7 days"
            )

        st.divider()

        # Cost Breakdown
        st.subheader("💰 Cost Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Cost by Feature**")
            cost_breakdown = analytics.get_cost_breakdown()

            if cost_breakdown:
                cost_data = []
                for api_type, features in cost_breakdown.items():
                    for feature in features:
                        cost_data.append({
                            'Feature': f"{api_type} - {feature['feature']}",
                            'Calls': feature['calls'],
                            'Total Cost': feature['total_cost'],
                            'Avg Cost': feature['avg_cost']
                        })

                if cost_data:
                    df = pd.DataFrame(cost_data)
                    st.dataframe(df, use_container_width=True)

                    # Pie chart
                    fig = px.pie(df, values='Total Cost', names='Feature', title='Cost Distribution')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No cost data available yet. Start using the bot!")

        with col2:
            st.markdown("**Feature Usage**")
            feature_usage = analytics.get_feature_usage()

            if feature_usage:
                df_features = pd.DataFrame(feature_usage, columns=['Feature', 'Usage Count', 'Total Cost', 'Total Tokens'])
                st.dataframe(df_features, use_container_width=True)

                # Bar chart
                fig = px.bar(df_features, x='Feature', y='Usage Count', title='Feature Usage')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No usage data available yet.")

        st.divider()

        # User Statistics
        st.subheader("👥 User Activity")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Top Users**")
            top_users = analytics.get_top_users(limit=10)

            if top_users:
                df_users = pd.DataFrame(
                    top_users,
                    columns=['User ID', 'Username', 'Activity Count', 'Last Active']
                )
                st.dataframe(df_users, use_container_width=True)
            else:
                st.info("No user activity yet.")

        with col2:
            st.markdown("**Recent Activity**")
            recent = analytics.get_recent_activity(limit=20)

            if recent:
                df_recent = pd.DataFrame(
                    recent,
                    columns=['Timestamp', 'Username', 'Name', 'Action', 'Details']
                )

                # Format timestamp to show time only
                df_recent['Time'] = pd.to_datetime(df_recent['Timestamp']).dt.strftime('%H:%M:%S')
                df_recent = df_recent[['Time', 'Username', 'Name', 'Action', 'Details']]

                st.dataframe(df_recent, use_container_width=True, height=400)
            else:
                st.info("No recent activity.")

        st.divider()

        # Download Statistics
        st.subheader("📥 Download Statistics")

        platform_stats = analytics.get_platform_downloads()

        if platform_stats:
            df_downloads = pd.DataFrame(
                platform_stats,
                columns=['Platform', 'Total', 'Successful', 'Failed']
            )

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.dataframe(df_downloads, use_container_width=True)

            with col2:
                st.metric("Total Downloads", f"{df_downloads['Total'].sum()}")
                success_rate = df_downloads['Successful'].sum() / df_downloads['Total'].sum() * 100 if df_downloads['Total'].sum() > 0 else 0
                st.metric("Success Rate", f"{success_rate:.1f}%")

            with col3:
                # Get total file size from database
                conn = analytics.conn = __import__('sqlite3').connect('analytics.db')
                cursor = conn.cursor()
                cursor.execute('SELECT SUM(file_size) FROM downloads WHERE success = 1')
                total_bytes = cursor.fetchone()[0] or 0
                conn.close()

                total_mb = total_bytes / (1024 * 1024)
                st.metric("Total Downloaded", f"{total_mb:.1f} MB")
                st.metric("Avg File Size", f"{total_mb / max(df_downloads['Successful'].sum(), 1):.1f} MB")

            # Platform distribution
            fig = px.bar(df_downloads, x='Platform', y=['Successful', 'Failed'],
                         title='Downloads by Platform', barmode='stack')
            st.plotly_chart(fig, use_container_width=True)

            # Recent downloads with details
            st.markdown("**Recent Downloads (with file sizes)**")
            cursor = conn = __import__('sqlite3').connect('analytics.db').cursor()
            cursor.execute('''
                SELECT timestamp, username, platform, content_type,
                       CASE WHEN success = 1 THEN 'Success' ELSE 'Failed' END as status,
                       ROUND(file_size / 1024.0 / 1024.0, 2) as size_mb
                FROM downloads
                ORDER BY timestamp DESC
                LIMIT 10
            ''')
            recent_downloads = cursor.fetchall()
            cursor.connection.close()

            if recent_downloads:
                df_recent_dl = pd.DataFrame(
                    recent_downloads,
                    columns=['Time', 'User', 'Platform', 'Type', 'Status', 'Size (MB)']
                )
                df_recent_dl['Time'] = pd.to_datetime(df_recent_dl['Time']).dt.strftime('%H:%M:%S')
                st.dataframe(df_recent_dl, use_container_width=True)
        else:
            st.info("No download statistics available yet.")

        st.divider()

        # Token Usage
        st.subheader("🎟️ Token Usage")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Tokens", f"{total_stats['total_tokens']:,}")

        with col2:
            avg_tokens = total_stats['total_tokens'] / max(total_stats['total_api_calls'], 1)
            st.metric("Avg Tokens/Call", f"{avg_tokens:.0f}")

        with col3:
            token_cost = total_stats['total_cost'] / max(total_stats['total_tokens'], 1) * 1000 if total_stats['total_tokens'] > 0 else 0
            st.metric("Cost per 1K Tokens", f"${token_cost:.6f}")

        st.divider()

        # Error Tracking
        st.subheader("⚠️ Error Statistics")

        error_stats = analytics.get_error_stats()

        if error_stats:
            df_errors = pd.DataFrame(
                error_stats,
                columns=['Feature', 'Error Count', 'Error Message']
            )
            st.dataframe(df_errors, use_container_width=True)
        else:
            st.success("No errors recorded!")

        st.caption("💡 Analytics data is stored in SQLite database (analytics.db)")

    # Tasks Page
    elif page == "📋 Tasks":
        st.header("📋 Running Tasks & Processes")

        # Bot Processes Section
        st.subheader("🤖 Bot Processes")

        bot_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and 'python' in str(cmdline).lower() and 'bot.py' in str(cmdline):
                    uptime_seconds = time.time() - proc.info['create_time']
                    uptime_minutes = uptime_seconds / 60

                    bot_processes.append({
                        'PID': proc.info['pid'],
                        'Command': ' '.join(cmdline)[-50:],  # Last 50 chars
                        'CPU %': f"{proc.info['cpu_percent']:.1f}%",
                        'Memory %': f"{proc.info['memory_percent']:.1f}%",
                        'Uptime': f"{int(uptime_minutes)} min",
                        'Status': '🟢 Running'
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if bot_processes:
            df_bot = pd.DataFrame(bot_processes)
            st.dataframe(df_bot, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Bot Processes", len(bot_processes))
            with col2:
                avg_cpu = sum([float(p['CPU %'].rstrip('%')) for p in bot_processes]) / len(bot_processes)
                st.metric("Avg CPU Usage", f"{avg_cpu:.1f}%")
            with col3:
                avg_mem = sum([float(p['Memory %'].rstrip('%')) for p in bot_processes]) / len(bot_processes)
                st.metric("Avg Memory Usage", f"{avg_mem:.1f}%")
        else:
            st.warning("No bot processes running")

        st.divider()

        # Recent Downloads Section
        st.subheader("📥 Recent Download Tasks")

        conn = __import__('sqlite3').connect('analytics.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, username, platform, content_type,
                   CASE WHEN success = 1 THEN '✅ Success' ELSE '❌ Failed' END as status,
                   ROUND(file_size / 1024.0 / 1024.0, 2) as size_mb
            FROM downloads
            ORDER BY timestamp DESC
            LIMIT 15
        ''')
        recent_downloads = cursor.fetchall()

        if recent_downloads:
            df_downloads = pd.DataFrame(
                recent_downloads,
                columns=['Time', 'User', 'Platform', 'Type', 'Status', 'Size (MB)']
            )
            df_downloads['Time'] = pd.to_datetime(df_downloads['Time']).dt.strftime('%H:%M:%S')
            st.dataframe(df_downloads, use_container_width=True, height=300)

            # Download statistics
            success_count = len([d for d in recent_downloads if d[4] == '✅ Success'])
            total_size = sum([d[5] for d in recent_downloads if d[5]])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Downloads", len(recent_downloads))
            with col2:
                st.metric("Successful", success_count)
            with col3:
                st.metric("Total Data", f"{total_size:.1f} MB")
        else:
            st.info("No recent downloads")

        st.divider()

        # Recent API Calls Section
        st.subheader("🎟️ Recent API Tasks")

        cursor.execute('''
            SELECT timestamp, username, feature,
                   tokens_used, cost,
                   CASE WHEN success = 1 THEN '✅ Success' ELSE '❌ Failed' END as status
            FROM api_usage
            ORDER BY timestamp DESC
            LIMIT 15
        ''')
        recent_api = cursor.fetchall()
        conn.close()

        if recent_api:
            df_api = pd.DataFrame(
                recent_api,
                columns=['Time', 'User', 'Feature', 'Tokens', 'Cost', 'Status']
            )
            df_api['Time'] = pd.to_datetime(df_api['Time']).dt.strftime('%H:%M:%S')
            df_api['Cost'] = df_api['Cost'].apply(lambda x: f"${x:.6f}")
            st.dataframe(df_api, use_container_width=True, height=300)

            # API statistics
            success_count = len([a for a in recent_api if a[5] == '✅ Success'])
            total_tokens = sum([a[3] for a in recent_api if a[3]])
            total_cost = sum([a[4] for a in recent_api if a[4]])

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total API Calls", len(recent_api))
            with col2:
                st.metric("Successful", success_count)
            with col3:
                st.metric("Total Tokens", f"{total_tokens:,}")
            with col4:
                st.metric("Total Cost", f"${total_cost:.6f}")
        else:
            st.info("No recent API calls")

        st.divider()

        # System Processes Section
        st.subheader("💻 All Python Processes")

        all_python = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else proc.info['name']
                    all_python.append({
                        'PID': proc.info['pid'],
                        'Command': cmdline[-60:],  # Last 60 chars
                        'CPU %': f"{proc.info['cpu_percent']:.1f}%",
                        'Memory %': f"{proc.info['memory_percent']:.1f}%"
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if all_python:
            df_python = pd.DataFrame(all_python)
            with st.expander(f"View All Python Processes ({len(all_python)})"):
                st.dataframe(df_python, use_container_width=True, height=400)

        st.caption("💡 Refresh the page to update task information")

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
