"""
Bot Activity Tracker
Helper functions to track user activities and costs
"""

from analytics import analytics
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# Gemini API Pricing (as of 2025)
GEMINI_PRICING = {
    'gemini-2.5-flash': {
        'input_per_1k': 0.00001875,  # $0.01875 per 1M tokens
        'output_per_1k': 0.000075,    # $0.075 per 1M tokens
        'avg_tokens_caption': 150,     # Estimated tokens for caption
        'avg_tokens_image': 500,       # Estimated tokens for image analysis
    }
}

def estimate_cost(feature: str, tokens: int = 0) -> float:
    """Estimate cost based on feature and tokens."""
    pricing = GEMINI_PRICING['gemini-2.5-flash']

    if feature == 'caption':
        # Caption generation
        tokens = tokens or pricing['avg_tokens_caption']
        return (tokens / 1000) * pricing['output_per_1k']
    elif feature == 'hashtags':
        # Hashtag generation
        tokens = tokens or pricing['avg_tokens_caption']
        return (tokens / 1000) * pricing['output_per_1k']
    elif feature == 'image_analysis':
        # Image analysis
        tokens = tokens or pricing['avg_tokens_image']
        return (tokens / 1000) * (pricing['input_per_1k'] + pricing['output_per_1k'])
    else:
        return 0.0

def track_user_action(action: str):
    """Decorator to track user actions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            user = update.effective_user
            user_id = user.id
            username = user.username or "Unknown"
            first_name = user.first_name or "User"

            # Log the action
            analytics.log_user_activity(
                user_id=user_id,
                username=username,
                first_name=first_name,
                action=action,
                details=None
            )

            # Execute the original function
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

def track_download(platform: str, content_type: str, success: bool = True):
    """Track download activity."""
    def get_user_info(update):
        user = update.effective_user
        return user.id, user.username or "Unknown"

    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            try:
                result = await func(update, context, *args, **kwargs)

                # Track successful download
                user_id, username = get_user_info(update)
                analytics.log_download(
                    user_id=user_id,
                    username=username,
                    platform=platform,
                    content_type=content_type,
                    success=success
                )

                return result
            except Exception as e:
                # Track failed download
                user_id, username = get_user_info(update)
                analytics.log_download(
                    user_id=user_id,
                    username=username,
                    platform=platform,
                    content_type=content_type,
                    success=False
                )
                raise e
        return wrapper
    return decorator

def track_api_call(api_type: str, feature: str):
    """Track API usage and costs."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id', 0)
            username = kwargs.get('username', 'system')

            try:
                # Execute function
                result = await func(*args, **kwargs)

                # Estimate cost and tokens
                tokens = GEMINI_PRICING['gemini-2.5-flash'].get(f'avg_tokens_{feature}', 150)
                cost = estimate_cost(feature, tokens)

                # Log successful API call
                analytics.log_api_usage(
                    user_id=user_id,
                    username=username,
                    api_type=api_type,
                    feature=feature,
                    tokens=tokens,
                    cost=cost,
                    success=True,
                    error=None
                )

                return result
            except Exception as e:
                # Log failed API call
                analytics.log_api_usage(
                    user_id=user_id,
                    username=username,
                    api_type=api_type,
                    feature=feature,
                    tokens=0,
                    cost=0.0,
                    success=False,
                    error=str(e)
                )
                raise e
        return wrapper
    return decorator
