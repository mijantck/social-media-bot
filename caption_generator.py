"""
AI Caption Generator Module
Uses Google Gemini API to generate captions and hashtags
"""

import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
logger = logging.getLogger(__name__)


class CaptionGenerator:
    """Generate captions and hashtags using AI."""

    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')

        if api_key:
            genai.configure(api_key=api_key)
            # Using gemini-2.5-flash (latest stable, fast, free tier)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.enabled = True
        else:
            logger.warning("GEMINI_API_KEY not found. AI features disabled.")
            self.enabled = False

    async def generate_caption(self, topic: str, style: str = "engaging") -> str:
        """
        Generate a social media caption.

        Args:
            topic: Topic or description
            style: Caption style (engaging, professional, casual, funny)

        Returns:
            Generated caption
        """
        if not self.enabled:
            return "⚠️ AI features are disabled. Please add GEMINI_API_KEY to .env file."

        try:
            prompt = f"""
Create an {style} social media caption for: {topic}

Requirements:
- Make it catchy and attention-grabbing
- Keep it under 150 characters
- Include 1-2 relevant emojis
- Perfect for Instagram/Facebook/TikTok
- Target audience: 15-35 age group
- Don't include hashtags (they'll be generated separately)

Just return the caption, nothing else.
            """

            # Generate with timeout handling
            response = self.model.generate_content(
                prompt,
                request_options={'timeout': 30}  # 30 second timeout
            )
            caption = response.text.strip()

            return caption

        except Exception as e:
            logger.error(f"Caption generation error: {e}")
            error_msg = str(e)

            # User-friendly error messages
            if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                return "⚠️ AI generation timed out. Please try again with a shorter topic."
            elif 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                return "⚠️ API quota exceeded. Please wait a few minutes and try again."
            elif '429' in error_msg:
                return "⚠️ Too many requests. Please wait 1 minute and try again."

            return f"⚠️ Error generating caption: {error_msg}"

    async def generate_hashtags(self, topic: str, count: int = 15) -> str:
        """
        Generate trending hashtags.

        Args:
            topic: Topic or description
            count: Number of hashtags (default: 15)

        Returns:
            Space-separated hashtags
        """
        if not self.enabled:
            return "⚠️ AI features are disabled. Please add GEMINI_API_KEY to .env file."

        try:
            prompt = f"""
Generate {count} trending and relevant hashtags for: {topic}

Requirements:
- Mix of popular and niche hashtags
- Relevant to 15-35 age group
- Mix of broad and specific tags
- Include trending tags when relevant
- Perfect for Instagram/TikTok/Facebook

Format: Return ONLY the hashtags separated by spaces, like:
#hashtag1 #hashtag2 #hashtag3
            """

            # Generate with timeout handling
            response = self.model.generate_content(
                prompt,
                request_options={'timeout': 30}  # 30 second timeout
            )
            hashtags = response.text.strip()

            # Clean up the response
            hashtags = hashtags.replace('\n', ' ')

            return hashtags

        except Exception as e:
            logger.error(f"Hashtag generation error: {e}")
            error_msg = str(e)

            # User-friendly error messages
            if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                return "⚠️ AI generation timed out. Please try again."
            elif 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                return "⚠️ API quota exceeded. Please wait a few minutes and try again."
            elif '429' in error_msg:
                return "⚠️ Too many requests. Please wait 1 minute and try again."

            return f"⚠️ Error generating hashtags: {error_msg}"

    async def generate_caption_with_hashtags(self, topic: str, style: str = "engaging") -> dict:
        """
        Generate both caption and hashtags.

        Args:
            topic: Topic or description
            style: Caption style

        Returns:
            dict with 'caption' and 'hashtags'
        """
        caption = await self.generate_caption(topic, style)
        hashtags = await self.generate_hashtags(topic)

        return {
            'caption': caption,
            'hashtags': hashtags,
            'full_text': f"{caption}\n\n{hashtags}"
        }

    async def analyze_image_and_generate(self, image_path: str, style: str = "engaging") -> dict:
        """
        Analyze an image and generate caption + hashtags.

        Args:
            image_path: Path to the image file
            style: Caption style (engaging, professional, casual, funny)

        Returns:
            dict with 'caption', 'hashtags', and 'full_text'
        """
        if not self.enabled:
            return {
                'caption': "⚠️ AI features are disabled. Please add GEMINI_API_KEY to .env file.",
                'hashtags': "",
                'full_text': "⚠️ AI features are disabled."
            }

        try:
            # Load the image
            img = Image.open(image_path)

            # Prompt for analyzing image and generating content
            prompt = f"""
Analyze this image and create {style} social media content.

Tasks:
1. Generate a catchy caption (under 150 characters, include 1-2 emojis)
2. Generate 15 relevant hashtags

Requirements:
- Caption should be attention-grabbing and {style}
- Target audience: 15-35 age group
- Perfect for Instagram/Facebook/TikTok
- Hashtags: mix of popular and niche tags

Format your response EXACTLY like this:
CAPTION: [your caption here]
HASHTAGS: #tag1 #tag2 #tag3 ...
            """

            # Generate with image and timeout handling
            response = self.model.generate_content(
                [prompt, img],
                request_options={'timeout': 30}
            )
            result_text = response.text.strip()

            # Parse the response
            caption = ""
            hashtags = ""

            lines = result_text.split('\n')
            for line in lines:
                if line.startswith('CAPTION:'):
                    caption = line.replace('CAPTION:', '').strip()
                elif line.startswith('HASHTAGS:'):
                    hashtags = line.replace('HASHTAGS:', '').strip()

            # Fallback if parsing fails
            if not caption and not hashtags:
                # Try to split by any obvious delimiter
                parts = result_text.split('\n\n')
                if len(parts) >= 2:
                    caption = parts[0].strip()
                    hashtags = parts[1].strip()
                else:
                    caption = result_text.strip()
                    hashtags = ""

            return {
                'caption': caption or "✨ Image analyzed successfully!",
                'hashtags': hashtags,
                'full_text': f"{caption}\n\n{hashtags}" if hashtags else caption
            }

        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            error_msg = str(e)

            # User-friendly error messages
            if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                error_text = "⚠️ Image analysis timed out. Please try with a smaller image."
            elif 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                error_text = "⚠️ API quota exceeded. Please wait a few minutes and try again."
            elif '429' in error_msg:
                error_text = "⚠️ Too many requests. Please wait 1 minute and try again."
            else:
                error_text = f"⚠️ Error analyzing image: {error_msg}"

            return {
                'caption': error_text,
                'hashtags': "",
                'full_text': error_text
            }
