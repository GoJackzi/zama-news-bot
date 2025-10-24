"""
Zama blog monitor using RSS feed or web scraping
"""
import feedparser
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ZamaBlogMonitor:
    """Monitor Zama blog for new posts"""
    
    def __init__(self, rss_url: str, blog_url: str):
        """
        Initialize blog monitor
        
        Args:
            rss_url: URL of the RSS feed
            blog_url: URL of the blog homepage (fallback)
        """
        self.rss_url = rss_url
        self.blog_url = blog_url
    
    def get_latest_posts(self, max_posts: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch latest blog posts
        
        Args:
            max_posts: Maximum number of posts to return
            
        Returns:
            List of post dictionaries
        """
        # Try RSS feed first
        posts = self._fetch_from_rss(max_posts)
        
        # If RSS fails, try scraping
        if not posts:
            logger.info("RSS feed failed, trying web scraping")
            posts = self._fetch_from_web(max_posts)
        
        return posts
    
    def _fetch_from_rss(self, max_posts: int) -> List[Dict[str, Any]]:
        """Fetch posts from RSS feed"""
        try:
            feed = feedparser.parse(self.rss_url)
            
            if feed.bozo:  # Feed parsing error
                logger.warning(f"RSS feed parsing error: {feed.bozo_exception}")
                return []
            
            posts = []
            
            for entry in feed.entries[:max_posts]:
                post = {
                    'id': entry.get('id', entry.get('link', '')),
                    'title': entry.get('title', 'Untitled'),
                    'url': entry.get('link', ''),
                    'summary': self._clean_summary(entry.get('summary', entry.get('description', ''))),
                    'date': self._format_date(entry.get('published', entry.get('updated', ''))),
                    'date_obj': self._parse_date(entry.get('published_parsed', entry.get('updated_parsed', None)))
                }
                posts.append(post)
            
            logger.info(f"Fetched {len(posts)} posts from RSS feed")
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed: {e}")
            return []
    
    def _fetch_from_web(self, max_posts: int) -> List[Dict[str, Any]]:
        """Scrape posts from blog website (fallback method)"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.blog_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            posts = []
            
            # This is a generic scraper - might need adjustment based on actual site structure
            # Look for common blog post patterns
            articles = soup.find_all(['article', 'div'], class_=['post', 'blog-post', 'article'], limit=max_posts)
            
            for article in articles:
                title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                link_elem = article.find('a', href=True)
                
                if title_elem and link_elem:
                    url = link_elem['href']
                    if not url.startswith('http'):
                        url = f"https://www.zama.ai{url}"
                    
                    post = {
                        'id': url,
                        'title': title_elem.get_text(strip=True),
                        'url': url,
                        'summary': '',
                        'date': '',
                        'date_obj': datetime.now()
                    }
                    posts.append(post)
            
            logger.info(f"Scraped {len(posts)} posts from website")
            return posts
            
        except Exception as e:
            logger.error(f"Error scraping blog website: {e}")
            return []
    
    def _clean_summary(self, summary: str) -> str:
        """Clean HTML tags and truncate summary"""
        # Remove HTML tags
        soup = BeautifulSoup(summary, 'html.parser')
        text = soup.get_text(strip=True)
        
        # Limit length
        if len(text) > 300:
            text = text[:300]
        
        return text
    
    def _format_date(self, date_str: str) -> str:
        """Format date string to readable format"""
        if not date_str:
            return ''
        try:
            # Try parsing common date formats
            for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            return date_str
        except:
            return date_str
    
    def _parse_date(self, date_tuple) -> datetime:
        """Parse date tuple to datetime object"""
        if date_tuple:
            try:
                return datetime(*date_tuple[:6])
            except:
                pass
        return datetime.now()

