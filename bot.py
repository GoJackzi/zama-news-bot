"""
Main Zama Telegram News Bot
"""
import asyncio
import logging
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import config
from utils.storage import Storage
from utils.formatter import (
    format_blog_post, 
    format_github_release, 
    format_pr,
    format_changelog,
    format_litepaper,
    format_status,
    format_startup_message,
    format_error_message
)
from sources.zama_blog import ZamaBlogMonitor
from sources.github_monitor import GitHubMonitor
from sources.docs_monitor import DocsMonitor
from sources.status_monitor import StatusMonitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ZamaNewsBot:
    """Main bot class"""
    
    def __init__(self):
        """Initialize the bot"""
        # Validate configuration
        config.validate_config()
        
        # Initialize Telegram bot
        self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        self.channel_id = config.TELEGRAM_CHANNEL_ID
        
        # Initialize storage
        self.storage = Storage(config.STORAGE_FILE)
        
        # Initialize source monitors
        self.blog_monitor = ZamaBlogMonitor(
            rss_url=config.ZAMA_BLOG_RSS,
            blog_url=config.ZAMA_BLOG_URL
        )
        self.github_monitor = GitHubMonitor(
            repos=config.ZAMA_REPOS,
            github_token=config.GITHUB_TOKEN,
            monitor_merges=config.MONITOR_GITHUB_MERGES
        )
        self.docs_monitor = DocsMonitor(
            changelog_url=config.ZAMA_CHANGELOG_URL,
            litepaper_url=config.ZAMA_LITEPAPER_URL
        )
        self.status_monitor = StatusMonitor(
            rss_url=config.ZAMA_STATUS_RSS,
            atom_url=config.ZAMA_STATUS_ATOM
        )
        
        # Initialize scheduler
        self.scheduler = AsyncIOScheduler()
        
        logger.info("Zama News Bot initialized")
    
    def _is_too_old(self, date_obj, days: int = 30) -> bool:
        """
        Check if an item is too old (for filtering on first run)
        
        Args:
            date_obj: datetime object of the item
            days: Number of days threshold (default 30)
            
        Returns:
            True if item is older than threshold
        """
        if not date_obj:
            return False
        
        from datetime import timedelta
        threshold = datetime.now() - timedelta(days=days)
        
        # Only filter old items if storage is mostly empty (first run)
        total_items = (
            self.storage.get_posted_count('blog') +
            self.storage.get_posted_count('github') +
            self.storage.get_posted_count('github_pr')
        )
        
        # If we have less than 5 tracked items, we're on first run
        if total_items < 5:
            return date_obj < threshold
        
        return False
    
    async def send_message(self, message: str) -> bool:
        """
        Send a message to the Telegram channel
        
        Args:
            message: Message text (HTML formatted)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=True  # Disable link previews to keep messages compact
            )
            logger.info("Message sent successfully")
            return True
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def check_blog_updates(self):
        """Check for new blog posts"""
        logger.info("Checking blog updates...")
        try:
            posts = self.blog_monitor.get_latest_posts(max_posts=5)
            new_posts = 0
            
            # Reverse to post oldest first, newest last
            for post in reversed(posts):
                post_id = post['id']
                if not self.storage.is_posted('blog', post_id):
                    # Skip old items on first run (older than 30 days)
                    if self._is_too_old(post.get('date_obj')):
                        self.storage.mark_posted('blog', post_id)  # Mark as posted but don't send
                        continue
                    
                    message = format_blog_post(post)
                    if await self.send_message(message):
                        self.storage.mark_posted('blog', post_id)
                        new_posts += 1
                        # Small delay between messages
                        await asyncio.sleep(2)
            
            logger.info(f"Found {new_posts} new blog posts")
            
        except Exception as e:
            logger.error(f"Error checking blog updates: {e}")
    
    async def check_github_updates(self):
        """Check for new GitHub releases"""
        logger.info("Checking GitHub updates...")
        try:
            releases = self.github_monitor.get_latest_releases()
            new_releases = 0
            
            # Reverse to post oldest first, newest last
            for release in reversed(releases):
                release_id = release['id']
                if not self.storage.is_posted('github', release_id):
                    # Skip old items on first run (older than 30 days)
                    if self._is_too_old(release.get('date_obj')):
                        self.storage.mark_posted('github', release_id)  # Mark as posted but don't send
                        continue
                    
                    message = format_github_release(release)
                    if await self.send_message(message):
                        self.storage.mark_posted('github', release_id)
                        new_releases += 1
                        # Small delay between messages
                        await asyncio.sleep(2)
            
            logger.info(f"Found {new_releases} new releases")
            
        except Exception as e:
            logger.error(f"Error checking GitHub updates: {e}")
    
    async def check_pr_updates(self):
        """Check for new merged PRs"""
        logger.info("Checking GitHub PR updates...")
        try:
            prs = self.github_monitor.get_merged_prs(per_repo=3)
            new_prs = 0
            
            # Reverse to post oldest first, newest last
            for pr in reversed(prs):
                pr_id = pr['id']
                if not self.storage.is_posted('github_pr', pr_id):
                    # Skip old items on first run (older than 7 days for PRs)
                    if self._is_too_old(pr.get('date_obj'), days=7):
                        self.storage.mark_posted('github_pr', pr_id)  # Mark as posted but don't send
                        continue
                    
                    message = format_pr(pr)
                    if await self.send_message(message):
                        self.storage.mark_posted('github_pr', pr_id)
                        new_prs += 1
                        # Small delay between messages
                        await asyncio.sleep(2)
            
            logger.info(f"Found {new_prs} new merged PRs")
            
        except Exception as e:
            logger.error(f"Error checking PR updates: {e}")
    
    async def check_docs_updates(self):
        """Check for documentation updates"""
        logger.info("Checking documentation updates...")
        try:
            # Check changelog
            changelog_entries = self.docs_monitor.get_changelog_updates()
            new_changelog = 0
            
            # Reverse to post oldest first, newest last
            for entry in reversed(changelog_entries):
                entry_id = entry['id']
                if not self.storage.is_posted('changelog', entry_id):
                    message = format_changelog(entry)
                    if await self.send_message(message):
                        self.storage.mark_posted('changelog', entry_id)
                        new_changelog += 1
                        await asyncio.sleep(2)
            
            # Check litepaper (with change detection)
            litepaper_entries = self.docs_monitor.get_litepaper_updates()
            new_litepaper = 0
            
            for entry in litepaper_entries:
                entry_id = entry['id']
                if not self.storage.is_posted('litepaper', entry_id):
                    # Get previous version for comparison
                    previous_hash = self.storage.get_last_litepaper_hash()
                    current_hash = entry.get('hash', '')
                    
                    # Add change info to entry
                    if previous_hash and previous_hash != current_hash:
                        entry['has_changes'] = True
                        entry['previous_hash'] = previous_hash
                    
                    message = format_litepaper(entry)
                    if await self.send_message(message):
                        self.storage.mark_posted('litepaper', entry_id)
                        self.storage.save_litepaper_hash(current_hash)
                        new_litepaper += 1
                        await asyncio.sleep(2)
            
            logger.info(f"Found {new_changelog} changelog + {new_litepaper} litepaper updates")
            
        except Exception as e:
            logger.error(f"Error checking docs updates: {e}")
    
    async def check_status_updates(self):
        """Check for system status updates"""
        logger.info("Checking system status updates...")
        try:
            updates = self.status_monitor.get_status_updates(max_items=5)
            new_status = 0
            
            # Reverse to post oldest first, newest last
            for update in reversed(updates):
                update_id = update['id']
                if not self.storage.is_posted('status', update_id):
                    message = format_status(update)
                    if await self.send_message(message):
                        self.storage.mark_posted('status', update_id)
                        new_status += 1
                        await asyncio.sleep(2)
            
            logger.info(f"Found {new_status} new status updates")
            
        except Exception as e:
            logger.error(f"Error checking status updates: {e}")
    
    async def check_all_updates(self):
        """Check all sources for updates"""
        logger.info("=" * 50)
        logger.info(f"Starting update check at {datetime.now()}")
        
        # Check all sources
        await self.check_blog_updates()
        await self.check_github_updates()
        if config.MONITOR_GITHUB_MERGES:
            await self.check_pr_updates()
        await self.check_docs_updates()
        await self.check_status_updates()
        
        # Cleanup old items periodically
        self.storage.cleanup_old_items('blog', keep_last=100)
        self.storage.cleanup_old_items('github', keep_last=100)
        self.storage.cleanup_old_items('github_pr', keep_last=200)
        self.storage.cleanup_old_items('changelog', keep_last=100)
        self.storage.cleanup_old_items('litepaper', keep_last=50)
        self.storage.cleanup_old_items('status', keep_last=100)
        
        logger.info("Update check completed")
        logger.info("=" * 50)
    
    async def start(self):
        """Start the bot"""
        logger.info("Starting Zama News Bot...")
        
        # Send startup message to channel
        try:
            startup_msg = format_startup_message()
            await self.send_message(startup_msg)
        except Exception as e:
            logger.error(f"Failed to send startup message: {e}")
        
        # Do an initial check
        await self.check_all_updates()
        
        # Schedule periodic checks
        if config.CHECK_INTERVAL_HOURS > 0:
            # Use hours if specified
            self.scheduler.add_job(
                self.check_all_updates,
                trigger=IntervalTrigger(hours=config.CHECK_INTERVAL_HOURS),
                id='update_check',
                name='Check for Zama updates',
                replace_existing=True
            )
            check_interval_text = f"{config.CHECK_INTERVAL_HOURS} hours"
        else:
            # Use minutes for more frequent checks
            self.scheduler.add_job(
                self.check_all_updates,
                trigger=IntervalTrigger(minutes=config.CHECK_INTERVAL_MINUTES),
                id='update_check',
                name='Check for Zama updates',
                replace_existing=True
            )
            check_interval_text = f"{config.CHECK_INTERVAL_MINUTES} minutes"
        
        # Start scheduler
        self.scheduler.start()
        logger.info(f"Scheduler started. Checking every {check_interval_text}")
        
        # Keep the bot running
        try:
            while True:
                await asyncio.sleep(60)  # Sleep for 60 seconds
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.scheduler.shutdown()


async def main():
    """Main entry point"""
    bot = ZamaNewsBot()
    await bot.start()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

