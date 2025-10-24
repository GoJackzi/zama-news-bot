"""
Configuration loader for the Zama Telegram News Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# Bot Configuration
CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', 0))
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))
MAX_TWEETS_PER_CHECK = int(os.getenv('MAX_TWEETS_PER_CHECK', 10))

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)
ZAMA_REPOS = [
    'zama-ai/fhevm',
    'zama-ai/tfhe-rs',
    'zama-ai/concrete-ml',
    'zama-ai/concrete'
]

# Zama Sources
ZAMA_BLOG_URL = 'https://www.zama.ai/blog'
ZAMA_BLOG_RSS = 'https://www.zama.ai/rss.xml'

# Zama Documentation & Status
ZAMA_CHANGELOG_URL = 'https://docs.zama.ai/change-log'
ZAMA_LITEPAPER_URL = 'https://docs.zama.ai/protocol/zama-protocol-litepaper'
ZAMA_STATUS_RSS = 'https://status.zama.ai/feed.rss'
ZAMA_STATUS_ATOM = 'https://status.zama.ai/feed.atom'

# GitHub monitoring options
MONITOR_GITHUB_RELEASES = True
MONITOR_GITHUB_MERGES = True  # Monitor merged PRs to main branch

# Storage
STORAGE_FILE = 'posted_items.json'

# Validation
def validate_config():
    """Validate required configuration"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required in .env file")
    if not TELEGRAM_CHANNEL_ID:
        raise ValueError("TELEGRAM_CHANNEL_ID is required in .env file")
    return True

