"""
Analytics Dashboard - Admin Panel
View API usage, costs, and user statistics
"""

import streamlit as st
import pandas as pd
from analytics import Analytics
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Bot Analytics - Admin Panel",
    page_icon="📊",
    layout="wide"
)

# Initialize analytics
analytics = Analytics()

# Custom CSS
st.markdown("""
<style>
    .big-metric {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
    }
    .cost-metric {
        font-size: 2rem;
        font-weight: bold;
        color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Bot Analytics Dashboard")
st.markdown("**Admin Panel** - Track API usage, costs, and user activity")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    st.link_button("🏠 Back to Bot Dashboard", "http://localhost:8501", use_container_width=True)

    st.divider()

    st.header("Filters")
    refresh = st.button("🔄 Refresh Data")

    st.divider()

    st.caption("Last updated: " + datetime.now().strftime("%H:%M:%S"))

# Get stats
total_stats = analytics.get_total_stats()
today_stats = analytics.get_today_stats()
monthly_estimate = analytics.estimate_monthly_cost()

# Overview Section
st.header("📈 Overview")

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
st.header("💰 Cost Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cost by Feature")
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
    st.subheader("Feature Usage")
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
st.header("👥 User Activity")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Users")
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
    st.subheader("Recent Activity")
    recent = analytics.get_recent_activity(limit=20)

    if recent:
        df_recent = pd.DataFrame(
            recent,
            columns=['Timestamp', 'Username', 'Name', 'Action', 'Details']
        )
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No recent activity.")

st.divider()

# Download Statistics
st.header("📥 Download Statistics")

platform_stats = analytics.get_platform_downloads()

if platform_stats:
    df_downloads = pd.DataFrame(
        platform_stats,
        columns=['Platform', 'Total', 'Successful', 'Failed']
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.dataframe(df_downloads, use_container_width=True)

    with col2:
        st.metric("Total Downloads", f"{df_downloads['Total'].sum()}")
        st.metric("Success Rate", f"{(df_downloads['Successful'].sum() / df_downloads['Total'].sum() * 100):.1f}%")

    # Platform distribution
    fig = px.bar(df_downloads, x='Platform', y=['Successful', 'Failed'],
                 title='Downloads by Platform', barmode='stack')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No download statistics available yet.")

st.divider()

# Error Tracking
st.header("⚠️ Error Statistics")

error_stats = analytics.get_error_stats()

if error_stats:
    df_errors = pd.DataFrame(
        error_stats,
        columns=['Feature', 'Error Count', 'Error Message']
    )
    st.dataframe(df_errors, use_container_width=True)
else:
    st.success("No errors recorded!")

st.divider()

# Hourly Activity
st.header("🕐 Activity Patterns")

hourly = analytics.get_hourly_activity(days=7)

if hourly:
    df_hourly = pd.DataFrame(hourly, columns=['Hour', 'Activity Count'])

    fig = px.line(df_hourly, x='Hour', y='Activity Count',
                  title='Hourly Activity (Last 7 Days)', markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Not enough data for activity patterns.")

st.divider()

# Token Usage
st.header("🎟️ Token Usage")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tokens", f"{total_stats['total_tokens']:,}")

with col2:
    avg_tokens = total_stats['total_tokens'] / max(total_stats['total_api_calls'], 1)
    st.metric("Avg Tokens/Call", f"{avg_tokens:.0f}")

with col3:
    token_cost = total_stats['total_cost'] / max(total_stats['total_tokens'], 1) * 1000
    st.metric("Cost per 1K Tokens", f"${token_cost:.6f}")

st.divider()

# Data Management
st.header("🗑️ Data Management")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Cleanup Old Data")
    days = st.number_input("Delete data older than (days):", min_value=30, value=90)
    if st.button("🗑️ Clean Up"):
        deleted = analytics.cleanup_old_data(days)
        st.success(f"Deleted {deleted} old records!")
        st.rerun()

with col2:
    st.subheader("Export Data")
    if st.button("📊 Export CSV"):
        st.info("Export feature coming soon!")

with col3:
    st.subheader("Database Info")
    st.info(f"Database: analytics.db")
    try:
        import os
        size = os.path.getsize("analytics.db") / 1024  # KB
        st.metric("DB Size", f"{size:.2f} KB")
    except:
        st.caption("Database not created yet")

# Footer
st.divider()
st.caption("💡 Tip: This dashboard updates in real-time. Enable auto-refresh in sidebar.")
st.caption("⚡ Powered by Streamlit | Data tracked by Analytics module")
