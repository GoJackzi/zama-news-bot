"""
Zama status page monitor using RSS/Atom feeds
"""
import feedparser
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StatusMonitor:
    """Monitor Zama status page for incidents and updates"""
    
    def __init__(self, rss_url: str, atom_url: str):
        """
        Initialize status monitor
        
        Args:
            rss_url: URL of the RSS feed
            atom_url: URL of the Atom feed (fallback)
        """
        self.rss_url = rss_url
        self.atom_url = atom_url
    
    def get_status_updates(self, max_items: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch status updates from feed
        
        Args:
            max_items: Maximum number of items to return
            
        Returns:
            List of status update dictionaries
        """
        # Try RSS feed first
        updates = self._fetch_from_feed(self.rss_url, max_items)
        
        # If RSS fails, try Atom
        if not updates:
            logger.info("RSS feed failed, trying Atom feed")
            updates = self._fetch_from_feed(self.atom_url, max_items)
        
        return updates
    
    def _fetch_from_feed(self, feed_url: str, max_items: int) -> List[Dict[str, Any]]:
        """Fetch updates from feed URL"""
        try:
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:  # Feed parsing error
                logger.warning(f"Feed parsing error: {feed.bozo_exception}")
                return []
            
            updates = []
            
            for entry in feed.entries[:max_items]:
                # Determine status type from title/content
                title = entry.get('title', 'Status Update')
                status_type = self._determine_status_type(title)
                
                update = {
                    'id': entry.get('id', entry.get('link', '')),
                    'title': title,
                    'content': self._clean_content(entry.get('summary', entry.get('description', ''))),
                    'url': entry.get('link', feed_url),
                    'date': self._format_date(entry.get('published', entry.get('updated', ''))),
                    'date_obj': self._parse_date(entry.get('published_parsed', entry.get('updated_parsed', None))),
                    'status_type': status_type,
                    'type': 'status'
                }
                updates.append(update)
            
            logger.info(f"Fetched {len(updates)} status updates from feed")
            return updates
            
        except Exception as e:
            logger.error(f"Error fetching status feed: {e}")
            return []
    
    def _determine_status_type(self, title: str) -> str:
        """Determine status type from title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['incident', 'outage', 'down', 'error']):
            return 'incident'
        elif any(word in title_lower for word in ['resolved', 'fixed', 'restored']):
            return 'resolved'
        elif any(word in title_lower for word in ['maintenance', 'scheduled', 'upgrade']):
            return 'maintenance'
        elif any(word in title_lower for word in ['degraded', 'performance', 'slow']):
            return 'degraded'
        else:
            return 'update'
    
    def _clean_content(self, content: str) -> str:
        """Clean HTML and limit content length"""
        from bs4 import BeautifulSoup
        
        # Remove HTML tags
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text(strip=True)
        
        # Limit length
        if len(text) > 400:
            text = text[:400]
        
        return text
    
    def _format_date(self, date_str: str) -> str:
        """Format date string to readable format"""
        if not date_str:
            return ''
        try:
            for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d %H:%M UTC')
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

