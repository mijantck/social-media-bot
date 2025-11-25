"""
Analytics Module
Track API usage, costs, and user activity
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class Analytics:
    """Track and analyze bot usage."""

    def __init__(self, db_path: str = "analytics.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # API Usage table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                username TEXT,
                api_type TEXT,
                feature TEXT,
                tokens_used INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                success BOOLEAN DEFAULT 1,
                error_message TEXT
            )
        ''')

        # User Activity table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                action TEXT,
                details TEXT
            )
        ''')

        # Download Stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                username TEXT,
                platform TEXT,
                content_type TEXT,
                success BOOLEAN DEFAULT 1,
                file_size INTEGER DEFAULT 0
            )
        ''')

        # Daily Stats summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                date DATE PRIMARY KEY,
                total_users INTEGER DEFAULT 0,
                total_requests INTEGER DEFAULT 0,
                total_downloads INTEGER DEFAULT 0,
                total_captions INTEGER DEFAULT 0,
                total_cost REAL DEFAULT 0.0
            )
        ''')

        conn.commit()
        conn.close()

    def log_api_usage(self, user_id: int, username: str, api_type: str,
                      feature: str, tokens: int = 0, cost: float = 0.0,
                      success: bool = True, error: str = None):
        """Log API usage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO api_usage
            (user_id, username, api_type, feature, tokens_used, cost, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, api_type, feature, tokens, cost, success, error))

        conn.commit()
        conn.close()

    def log_user_activity(self, user_id: int, username: str, first_name: str,
                          action: str, details: str = None):
        """Log user activity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user_activity
            (user_id, username, first_name, action, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, action, details))

        conn.commit()
        conn.close()

    def log_download(self, user_id: int, username: str, platform: str,
                     content_type: str, success: bool = True, file_size: int = 0):
        """Log download activity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO downloads
            (user_id, username, platform, content_type, success, file_size)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, platform, content_type, success, file_size))

        conn.commit()
        conn.close()

    def get_total_stats(self) -> Dict:
        """Get total statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total users
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM user_activity')
        total_users = cursor.fetchone()[0]

        # Total API calls
        cursor.execute('SELECT COUNT(*) FROM api_usage')
        total_api_calls = cursor.fetchone()[0]

        # Total cost
        cursor.execute('SELECT SUM(cost) FROM api_usage')
        total_cost = cursor.fetchone()[0] or 0.0

        # Total downloads
        cursor.execute('SELECT COUNT(*) FROM downloads WHERE success=1')
        total_downloads = cursor.fetchone()[0]

        # Total tokens
        cursor.execute('SELECT SUM(tokens_used) FROM api_usage')
        total_tokens = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_users': total_users,
            'total_api_calls': total_api_calls,
            'total_cost': round(total_cost, 4),
            'total_downloads': total_downloads,
            'total_tokens': total_tokens
        }

    def get_today_stats(self) -> Dict:
        """Get today's statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        today = datetime.now().date()

        # Today's users
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM user_activity
            WHERE DATE(timestamp) = ?
        ''', (today,))
        today_users = cursor.fetchone()[0]

        # Today's API calls
        cursor.execute('''
            SELECT COUNT(*) FROM api_usage
            WHERE DATE(timestamp) = ?
        ''', (today,))
        today_api_calls = cursor.fetchone()[0]

        # Today's cost
        cursor.execute('''
            SELECT SUM(cost) FROM api_usage
            WHERE DATE(timestamp) = ?
        ''', (today,))
        today_cost = cursor.fetchone()[0] or 0.0

        # Today's downloads
        cursor.execute('''
            SELECT COUNT(*) FROM downloads
            WHERE DATE(timestamp) = ? AND success=1
        ''', (today,))
        today_downloads = cursor.fetchone()[0]

        conn.close()

        return {
            'today_users': today_users,
            'today_api_calls': today_api_calls,
            'today_cost': round(today_cost, 4),
            'today_downloads': today_downloads
        }

    def get_top_users(self, limit: int = 10) -> List[Tuple]:
        """Get most active users."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                user_id,
                username,
                COUNT(*) as activity_count,
                MAX(timestamp) as last_active
            FROM user_activity
            GROUP BY user_id
            ORDER BY activity_count DESC
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_feature_usage(self) -> List[Tuple]:
        """Get feature usage statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                feature,
                COUNT(*) as usage_count,
                SUM(cost) as total_cost,
                SUM(tokens_used) as total_tokens
            FROM api_usage
            GROUP BY feature
            ORDER BY usage_count DESC
        ''')

        results = cursor.fetchall()
        conn.close()

        return results

    def get_platform_downloads(self) -> List[Tuple]:
        """Get download statistics by platform."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                platform,
                COUNT(*) as download_count,
                SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) as successful,
                SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) as failed
            FROM downloads
            GROUP BY platform
            ORDER BY download_count DESC
        ''')

        results = cursor.fetchall()
        conn.close()

        return results

    def get_hourly_activity(self, days: int = 7) -> List[Tuple]:
        """Get hourly activity for last N days."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                strftime('%H', timestamp) as hour,
                COUNT(*) as activity_count
            FROM user_activity
            WHERE timestamp >= datetime('now', '-' || ? || ' days')
            GROUP BY hour
            ORDER BY hour
        ''', (days,))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_cost_breakdown(self) -> Dict:
        """Get cost breakdown by feature."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                api_type,
                feature,
                COUNT(*) as calls,
                SUM(cost) as total_cost,
                AVG(cost) as avg_cost
            FROM api_usage
            WHERE cost > 0
            GROUP BY api_type, feature
            ORDER BY total_cost DESC
        ''')

        results = cursor.fetchall()
        conn.close()

        breakdown = {}
        for row in results:
            api_type, feature, calls, total_cost, avg_cost = row
            if api_type not in breakdown:
                breakdown[api_type] = []
            breakdown[api_type].append({
                'feature': feature,
                'calls': calls,
                'total_cost': round(total_cost, 4),
                'avg_cost': round(avg_cost, 6)
            })

        return breakdown

    def get_error_stats(self) -> List[Tuple]:
        """Get error statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                feature,
                COUNT(*) as error_count,
                error_message
            FROM api_usage
            WHERE success=0 AND error_message IS NOT NULL
            GROUP BY feature, error_message
            ORDER BY error_count DESC
            LIMIT 20
        ''')

        results = cursor.fetchall()
        conn.close()

        return results

    def get_recent_activity(self, limit: int = 50) -> List[Tuple]:
        """Get recent user activity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                timestamp,
                username,
                first_name,
                action,
                details
            FROM user_activity
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()
        conn.close()

        return results

    def estimate_monthly_cost(self) -> float:
        """Estimate monthly cost based on recent usage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get cost for last 7 days
        cursor.execute('''
            SELECT SUM(cost) FROM api_usage
            WHERE timestamp >= datetime('now', '-7 days')
        ''')
        week_cost = cursor.fetchone()[0] or 0.0

        conn.close()

        # Estimate monthly (assuming 30 days)
        monthly_estimate = (week_cost / 7) * 30
        return round(monthly_estimate, 2)

    def cleanup_old_data(self, days: int = 90):
        """Clean up data older than N days."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cutoff_date = datetime.now() - timedelta(days=days)

        cursor.execute('DELETE FROM api_usage WHERE timestamp < ?', (cutoff_date,))
        cursor.execute('DELETE FROM user_activity WHERE timestamp < ?', (cutoff_date,))
        cursor.execute('DELETE FROM downloads WHERE timestamp < ?', (cutoff_date,))

        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        return deleted


# Global analytics instance
analytics = Analytics()
