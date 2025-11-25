"""
Social Media Manager Bot - Content Downloader
Supports: Instagram, YouTube, TikTok, Facebook
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

# Import our custom modules
from downloaders import ContentDownloader
from caption_generator import CaptionGenerator
from analytics import analytics

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize services
downloader = ContentDownloader()
caption_gen = CaptionGenerator()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start command is issued."""
    user = update.effective_user

    # Track user activity
    analytics.log_user_activity(
        user_id=user.id,
        username=user.username or "unknown",
        first_name=user.first_name or "User",
        action="start",
        details="User started the bot"
    )

    welcome_message = f"""
👋 Welcome {user.first_name}!

🤖 **Social Media Manager Bot**

I can help you with:
📥 Download content from Instagram, YouTube, TikTok
📸 Analyze images and generate captions
✍️ Generate captions with AI
🔖 Suggest trending hashtags

**How to use:**
1️⃣ Send me any Instagram/YouTube/TikTok link
2️⃣ Send me a photo for AI analysis
3️⃣ Get AI-generated captions & hashtags

**Commands:**
/start - Show this message
/help - Get detailed help
/caption - Generate caption for text
/hashtags - Get hashtag suggestions

Made with ❤️ for content creators
    """
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    user = update.effective_user

    # Track user activity
    analytics.log_user_activity(
        user_id=user.id,
        username=user.username or "unknown",
        first_name=user.first_name or "User",
        action="help",
        details="User requested help"
    )

    help_text = """
📖 **How to Use This Bot:**

**📸 Analyze Your Photos:**
Simply send me any photo and I'll:
• Analyze the image content
• Generate a catchy caption
• Suggest 15 relevant hashtags

**Download Content:**
Just send me a link from:
• Instagram (posts, reels, stories)
• YouTube (videos, shorts)
• TikTok (videos)
• Facebook (videos)

**Generate Captions:**
Use: /caption <your topic>
Example: /caption sunset beach photo

**Get Hashtags:**
Use: /hashtags <your topic>
Example: /hashtags fitness motivation

**Supported Links:**
✅ instagram.com/p/xxxxx
✅ instagram.com/reel/xxxxx
✅ youtube.com/watch?v=xxxxx
✅ youtu.be/xxxxx
✅ tiktok.com/@user/video/xxxxx
✅ facebook.com/watch?v=xxxxx

**Tips:**
• Send photos directly for AI analysis
• Send links one at a time
• Video downloads may take 30-60 seconds
• Maximum video size: 50MB (Telegram limit)

Need more help? Contact @YourUsername
    """
    await update.message.reply_text(help_text)


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle URLs sent by users."""
    url = update.message.text.strip()
    user = update.effective_user

    # Track user activity
    analytics.log_user_activity(
        user_id=user.id,
        username=user.username or "unknown",
        first_name=user.first_name or "User",
        action="download",
        details=f"Download requested: {url}"
    )

    # Check if it's a supported URL
    if not any(domain in url for domain in ['instagram.com', 'youtube.com', 'youtu.be', 'tiktok.com', 'facebook.com']):
        await update.message.reply_text(
            "❌ I can only download from Instagram, YouTube, TikTok, and Facebook.\n\n"
            "Send /help to see examples."
        )
        return

    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Processing your link...\nThis may take 30-60 seconds.")

    import time
    start_time = time.time()

    try:
        # Download the content
        result = await downloader.download(url)

        if result['success']:
            download_time = time.time() - start_time
            file_size = os.path.getsize(result['file_path']) if os.path.exists(result['file_path']) else 0
            file_size_mb = file_size / (1024 * 1024)

            # Delete processing message
            await processing_msg.delete()

            # Send the downloaded content (video/image only with basic caption)
            if result['type'] == 'video':
                await update.message.reply_video(
                    video=open(result['file_path'], 'rb'),
                    caption=f"✅ Downloaded from {result['platform']}\n\n{result.get('caption', '')}",
                    supports_streaming=True
                )
            elif result['type'] == 'image':
                await update.message.reply_photo(
                    photo=open(result['file_path'], 'rb'),
                    caption=f"✅ Downloaded from {result['platform']}\n\n{result.get('caption', '')}"
                )

            # Send statistics in separate message
            stats_text = f"""📊 **Download Statistics:**
📱 Platform: {result['platform']}
📦 File Size: {file_size_mb:.2f} MB
⏱️ Time Taken: {download_time:.1f} seconds
🎬 Type: {result['type'].upper()}"""

            await update.message.reply_text(stats_text)

            # Track successful download
            analytics.log_download(
                user_id=user.id,
                username=user.username or "unknown",
                platform=result['platform'],
                content_type=result['type'],
                success=True,
                file_size=file_size
            )

            # Clean up downloaded file
            if os.path.exists(result['file_path']):
                os.remove(result['file_path'])

            # Ask if user wants AI caption
            keyboard = [
                [InlineKeyboardButton("✨ Generate AI Caption", callback_data=f"caption_{url}")],
                [InlineKeyboardButton("🔖 Get Hashtags", callback_data=f"hashtags_{url}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Would you like AI-generated content?",
                reply_markup=reply_markup
            )

        else:
            # Track failed download
            platform = "Unknown"
            if 'instagram.com' in url:
                platform = "Instagram"
            elif 'youtube.com' in url or 'youtu.be' in url:
                platform = "YouTube"
            elif 'tiktok.com' in url:
                platform = "TikTok"
            elif 'facebook.com' in url:
                platform = "Facebook"

            analytics.log_download(
                user_id=user.id,
                username=user.username or "unknown",
                platform=platform,
                content_type="video",
                success=False
            )
            await processing_msg.edit_text(f"❌ Error: {result['error']}")

    except Exception as e:
        logger.error(f"Error downloading: {e}")
        # Track failed download
        analytics.log_download(
            user_id=user.id,
            username=user.username or "unknown",
            platform="Unknown",
            content_type="video",
            success=False
        )
        await processing_msg.edit_text(f"❌ An error occurred: {str(e)}")


async def caption_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate AI caption."""
    user = update.effective_user

    # Track user activity
    analytics.log_user_activity(
        user_id=user.id,
        username=user.username or "unknown",
        first_name=user.first_name or "User",
        action="caption",
        details="Caption generation requested"
    )

    if not context.args:
        await update.message.reply_text(
            "Please provide a topic!\n\n"
            "Example: /caption sunset beach photo"
        )
        return

    topic = ' '.join(context.args)
    processing_msg = await update.message.reply_text("✍️ Generating caption...")

    import time
    start_time = time.time()

    try:
        caption = await caption_gen.generate_caption(topic)
        generation_time = time.time() - start_time

        # Track API usage (estimated)
        estimated_tokens = 150  # Average tokens for caption
        estimated_cost = estimated_tokens * 0.000075 / 1000  # Output token cost

        # Send caption first
        response_text = f"""✨ **Generated Caption:**

{caption}"""

        await processing_msg.edit_text(response_text)

        # Send statistics in separate message
        stats_text = f"""📊 **Statistics:**
⏱️ Time: {generation_time:.2f}s
🎟️ Tokens: ~{estimated_tokens}
💰 Cost: ${estimated_cost:.6f}"""

        await update.message.reply_text(stats_text)

        analytics.log_api_usage(
            user_id=user.id,
            username=user.username or "unknown",
            api_type="Gemini AI",
            feature="caption",
            tokens=estimated_tokens,
            cost=estimated_cost,
            success=True
        )
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")
        # Track failed API call
        analytics.log_api_usage(
            user_id=user.id,
            username=user.username or "unknown",
            api_type="Gemini AI",
            feature="caption",
            tokens=0,
            cost=0.0,
            success=False,
            error=str(e)
        )


async def hashtags_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate hashtag suggestions."""
    user = update.effective_user

    # Track user activity
    analytics.log_user_activity(
        user_id=user.id,
        username=user.username or "unknown",
        first_name=user.first_name or "User",
        action="hashtags",
        details="Hashtag generation requested"
    )

    if not context.args:
        await update.message.reply_text(
            "Please provide a topic!\n\n"
            "Example: /hashtags fitness motivation"
        )
        return

    topic = ' '.join(context.args)
    processing_msg = await update.message.reply_text("🔖 Generating hashtags...")

    try:
        hashtags = await caption_gen.generate_hashtags(topic)
        await processing_msg.edit_text(f"🔖 **Suggested Hashtags:**\n\n{hashtags}")

        # Track API usage (estimated)
        estimated_tokens = 150  # Average tokens for hashtags
        estimated_cost = estimated_tokens * 0.000075 / 1000  # Output token cost

        analytics.log_api_usage(
            user_id=user.id,
            username=user.username or "unknown",
            api_type="Gemini AI",
            feature="hashtags",
            tokens=estimated_tokens,
            cost=estimated_cost,
            success=True
        )
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")
        # Track failed API call
        analytics.log_api_usage(
            user_id=user.id,
            username=user.username or "unknown",
            api_type="Gemini AI",
            feature="hashtags",
            tokens=0,
            cost=0.0,
            success=False,
            error=str(e)
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith('caption_'):
        url = data.replace('caption_', '')
        await query.message.reply_text("✍️ Generating AI caption...")
        try:
            caption = await caption_gen.generate_caption(f"social media post from {url}")
            await query.message.reply_text(f"✨ **AI Caption:**\n\n{caption}")
        except Exception as e:
            await query.message.reply_text(f"❌ Error: {str(e)}")

    elif data.startswith('hashtags_'):
        url = data.replace('hashtags_', '')
        await query.message.reply_text("🔖 Generating hashtags...")
        try:
            hashtags = await caption_gen.generate_hashtags(f"content from {url}")
            await query.message.reply_text(f"🔖 **Hashtags:**\n\n{hashtags}")
        except Exception as e:
            await query.message.reply_text(f"❌ Error: {str(e)}")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photos sent by users and generate caption + hashtags."""
    user = update.effective_user

    # Track user activity
    analytics.log_user_activity(
        user_id=user.id,
        username=user.username or "unknown",
        first_name=user.first_name or "User",
        action="image_analysis",
        details="Image analysis requested"
    )

    # Send processing message
    processing_msg = await update.message.reply_text("📸 Analyzing your image...\nGenerating caption and hashtags...")

    import time
    start_time = time.time()

    try:
        # Get the photo (largest size)
        photo = update.message.photo[-1]

        # Download the photo
        photo_file = await photo.get_file()
        photo_path = f"downloads/photo_{user.id}_{photo.file_id}.jpg"
        await photo_file.download_to_drive(photo_path)

        # Get file size
        file_size = os.path.getsize(photo_path) / 1024  # KB

        # Analyze image and generate caption + hashtags
        result = await caption_gen.analyze_image_and_generate(photo_path)

        analysis_time = time.time() - start_time

        # Delete processing message
        await processing_msg.delete()

        # Track API usage (estimated - image analysis uses more tokens)
        estimated_tokens = 500  # Average tokens for image analysis
        estimated_cost = estimated_tokens * 0.000075 / 1000  # Output token cost

        # Send result - Caption and hashtags first
        response_text = f"""✨ **AI Image Analysis:**

{result['caption']}

{result['hashtags']}"""

        await update.message.reply_text(response_text)

        # Send statistics in separate message
        stats_text = f"""📊 **Statistics:**
📷 Image Size: {file_size:.1f} KB
⏱️ Analysis Time: {analysis_time:.2f}s
🎟️ Tokens Used: ~{estimated_tokens}
💰 API Cost: ${estimated_cost:.6f}"""

        await update.message.reply_text(stats_text)

        analytics.log_api_usage(
            user_id=user.id,
            username=user.username or "unknown",
            api_type="Gemini AI",
            feature="image_analysis",
            tokens=estimated_tokens,
            cost=estimated_cost,
            success=True
        )

        # Clean up downloaded photo
        if os.path.exists(photo_path):
            os.remove(photo_path)

    except Exception as e:
        logger.error(f"Photo handling error: {e}")
        await processing_msg.edit_text(f"❌ Error analyzing image: {str(e)}")
        # Track failed API call
        analytics.log_api_usage(
            user_id=user.id,
            username=user.username or "unknown",
            api_type="Gemini AI",
            feature="image_analysis",
            tokens=0,
            cost=0.0,
            success=False,
            error=str(e)
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")


async def post_init(application: Application):
    """Set up bot commands menu."""
    commands = [
        BotCommand("start", "🏠 Start the bot"),
        BotCommand("help", "❓ Get help and instructions"),
        BotCommand("caption", "✍️ Generate AI caption"),
        BotCommand("hashtags", "🔖 Generate hashtags"),
    ]
    await application.bot.set_my_commands(commands)
    print("✅ Bot commands menu set up successfully!")


def main():
    """Start the bot."""
    # Get bot token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file!")
        print("Please create a .env file with your bot token.")
        return

    # Create application
    application = Application.builder().token(token).build()

    # Set up bot commands menu
    application.post_init = post_init

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("caption", caption_command))
    application.add_handler(CommandHandler("hashtags", hashtags_command))

    # Add URL handler (detects messages with URLs)
    application.add_handler(MessageHandler(filters.TEXT & filters.Entity("url"), handle_url))

    # Add photo handler (detects photos)
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Add button callback handler
    application.add_handler(CallbackQueryHandler(button_callback))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    print("🤖 Bot is starting...")
    print("Press Ctrl+C to stop")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
