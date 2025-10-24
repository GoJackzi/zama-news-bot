"""
Twitter scraper for @zama_fhe using nitter.net or direct scraping
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


class TwitterScraper:
    """Scrape tweets from @zama_fhe"""
    
    def __init__(self, handle: str):
        """
        Initialize Twitter scraper
        
        Args:
            handle: Twitter handle without @ (e.g., 'zama_fhe')
        """
        self.handle = handle
        # List of nitter instances to try (they sometimes go down)
        self.nitter_instances = [
            'https://nitter.net',
            'https://nitter.privacydev.net',
            'https://nitter.poast.org',
            'https://nitter.1d4.us'
        ]
    
    def get_latest_tweets(self, max_tweets: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch latest tweets from the user
        
        Args:
            max_tweets: Maximum number of tweets to return
            
        Returns:
            List of tweet dictionaries
        """
        # Try each nitter instance until one works
        for instance in self.nitter_instances:
            try:
                tweets = self._fetch_from_nitter(instance, max_tweets)
                if tweets:
                    return tweets
            except Exception as e:
                logger.warning(f"Failed to fetch from {instance}: {e}")
                continue
        
        logger.error("All nitter instances failed, trying direct scraping")
        # Fallback to direct Twitter scraping (less reliable)
        return self._fetch_from_twitter_direct(max_tweets)
    
    def _fetch_from_nitter(self, instance: str, max_tweets: int) -> List[Dict[str, Any]]:
        """
        Fetch tweets from a nitter instance
        
        Args:
            instance: Nitter instance URL
            max_tweets: Maximum number of tweets to return
            
        Returns:
            List of tweet dictionaries
        """
        url = f"{instance}/{self.handle}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        tweets = []
        
        # Find tweet containers (nitter structure)
        tweet_elements = soup.find_all('div', class_='timeline-item')
        
        for tweet_elem in tweet_elements[:max_tweets]:
            try:
                # Skip retweets and replies if desired
                if tweet_elem.find('div', class_='retweet-header'):
                    continue
                
                # Extract tweet content
                content_elem = tweet_elem.find('div', class_='tweet-content')
                if not content_elem:
                    continue
                
                text = content_elem.get_text(strip=True)
                
                # Extract tweet link
                link_elem = tweet_elem.find('a', class_='tweet-link')
                tweet_url = ''
                tweet_id = ''
                if link_elem and 'href' in link_elem.attrs:
                    tweet_path = link_elem['href']
                    tweet_url = f"https://twitter.com{tweet_path.replace(instance, '')}"
                    # Extract tweet ID from path
                    parts = tweet_path.split('/')
                    if len(parts) > 0:
                        tweet_id = parts[-1].split('#')[0]
                
                # Extract date
                date_elem = tweet_elem.find('span', class_='tweet-date')
                date_str = ''
                if date_elem:
                    date_link = date_elem.find('a')
                    if date_link and 'title' in date_link.attrs:
                        date_str = date_link['title']
                
                if text and tweet_id:
                    tweet = {
                        'id': tweet_id,
                        'text': text,
                        'url': tweet_url if tweet_url else f"https://twitter.com/{self.handle}/status/{tweet_id}",
                        'date': self._format_date(date_str),
                        'date_obj': self._parse_date(date_str),
                        'author': f"@{self.handle}"
                    }
                    tweets.append(tweet)
                    
            except Exception as e:
                logger.warning(f"Error parsing tweet element: {e}")
                continue
        
        logger.info(f"Fetched {len(tweets)} tweets from {instance}")
        return tweets
    
    def _fetch_from_twitter_direct(self, max_tweets: int) -> List[Dict[str, Any]]:
        """
        Fallback: Try to scrape directly from Twitter (less reliable, may not work)
        
        Args:
            max_tweets: Maximum number of tweets to return
            
        Returns:
            List of tweet dictionaries
        """
        try:
            # This is a very basic fallback and likely won't work due to Twitter's restrictions
            # But keeping it as a last resort
            url = f"https://twitter.com/{self.handle}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            # Twitter will likely return JavaScript-rendered content
            # This is a placeholder that likely won't work without a proper browser
            logger.warning("Direct Twitter scraping is unreliable and likely to fail")
            return []
            
        except Exception as e:
            logger.error(f"Direct Twitter scraping failed: {e}")
            return []
    
    def _format_date(self, date_str: str) -> str:
        """Format date string to readable format"""
        if not date_str:
            return ''
        try:
            # Nitter format: "MMM D, YYYY · H:MM AM/PM UTC"
            dt = datetime.strptime(date_str, '%b %d, %Y · %I:%M %p %Z')
            return dt.strftime('%Y-%m-%d %H:%M UTC')
        except:
            # Return as-is if parsing fails
            return date_str
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime object"""
        if not date_str:
            return datetime.now()
        try:
            return datetime.strptime(date_str, '%b %d, %Y · %I:%M %p %Z')
        except:
            return datetime.now()

