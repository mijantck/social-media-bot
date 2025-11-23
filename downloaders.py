"""
Content Downloader Module
Handles downloading from Instagram, YouTube, TikTok, Facebook
"""

import os
import yt_dlp
import instaloader
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ContentDownloader:
    """Download content from various social media platforms."""

    def __init__(self):
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)

        # Initialize instaloader
        self.insta_loader = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
        )

    async def download(self, url: str) -> dict:
        """
        Download content from URL.

        Args:
            url: URL to download from

        Returns:
            dict with success, type, file_path, platform, error, caption
        """
        try:
            # Detect platform
            if 'instagram.com' in url:
                return await self._download_instagram(url)
            elif 'youtube.com' in url or 'youtu.be' in url:
                return await self._download_youtube(url)
            elif 'tiktok.com' in url:
                return await self._download_tiktok(url)
            elif 'facebook.com' in url or 'fb.watch' in url:
                return await self._download_facebook(url)
            else:
                return {
                    'success': False,
                    'error': 'Unsupported platform'
                }

        except Exception as e:
            logger.error(f"Download error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def _download_instagram(self, url: str) -> dict:
        """Download from Instagram using yt-dlp (more reliable)."""
        try:
            output_template = str(self.download_dir / 'instagram_%(id)s.%(ext)s')

            # yt-dlp options with better Instagram support and timeout handling
            ydl_opts = {
                'outtmpl': output_template,
                'format': 'best[filesize<50M]/best',
                'quiet': True,
                'no_warnings': True,
                # Timeout settings
                'socket_timeout': 30,  # 30 seconds socket timeout
                'retries': 3,  # Retry 3 times
                'fragment_retries': 3,
                # Add headers to avoid blocking
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                }
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                # Determine type (video or image)
                file_ext = filename.split('.')[-1].lower()
                media_type = 'video' if file_ext in ['mp4', 'webm', 'mkv'] else 'image'

                return {
                    'success': True,
                    'type': media_type,
                    'file_path': filename,
                    'platform': 'Instagram',
                    'caption': info.get('description', '') or info.get('title', '')
                }

        except Exception as e:
            logger.error(f"Instagram download error: {e}")
            error_msg = str(e)

            # User-friendly error messages
            if 'timed out' in error_msg.lower() or 'timeout' in error_msg.lower():
                error_msg = 'Download timed out. The video/image might be too large or network is slow. Please try again.'
            elif '401' in error_msg or '403' in error_msg:
                error_msg = 'Access denied. The post might be private or restricted.'
            elif '404' in error_msg:
                error_msg = 'Post not found. Check if the link is correct.'

            return {
                'success': False,
                'error': f'Instagram error: {error_msg}'
            }

    async def _download_youtube(self, url: str) -> dict:
        """Download from YouTube."""
        try:
            output_template = str(self.download_dir / 'youtube_%(id)s.%(ext)s')

            ydl_opts = {
                'outtmpl': output_template,
                'format': 'best[filesize<50M]/best',  # Limit to 50MB for Telegram
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
                'fragment_retries': 3,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                return {
                    'success': True,
                    'type': 'video',
                    'file_path': filename,
                    'platform': 'YouTube',
                    'caption': info.get('title', '')
                }

        except Exception as e:
            logger.error(f"YouTube download error: {e}")
            return {
                'success': False,
                'error': f'YouTube error: {str(e)}'
            }

    async def _download_tiktok(self, url: str) -> dict:
        """Download from TikTok."""
        try:
            output_template = str(self.download_dir / 'tiktok_%(id)s.%(ext)s')

            ydl_opts = {
                'outtmpl': output_template,
                'format': 'best[filesize<50M]/best',
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
                'fragment_retries': 3,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                return {
                    'success': True,
                    'type': 'video',
                    'file_path': filename,
                    'platform': 'TikTok',
                    'caption': info.get('description', '')
                }

        except Exception as e:
            logger.error(f"TikTok download error: {e}")
            return {
                'success': False,
                'error': f'TikTok error: {str(e)}'
            }

    async def _download_facebook(self, url: str) -> dict:
        """Download from Facebook."""
        try:
            output_template = str(self.download_dir / 'facebook_%(id)s.%(ext)s')

            ydl_opts = {
                'outtmpl': output_template,
                'format': 'best[filesize<50M]/best',
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
                'fragment_retries': 3,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                return {
                    'success': True,
                    'type': 'video',
                    'file_path': filename,
                    'platform': 'Facebook',
                    'caption': info.get('title', '')
                }

        except Exception as e:
            logger.error(f"Facebook download error: {e}")
            return {
                'success': False,
                'error': f'Facebook error: {str(e)}'
            }
