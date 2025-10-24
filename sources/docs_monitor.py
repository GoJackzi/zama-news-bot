"""
Zama documentation monitor for changelog and litepaper changes
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)


class DocsMonitor:
    """Monitor Zama documentation pages for changes"""
    
    def __init__(self, changelog_url: str, litepaper_url: str):
        """
        Initialize documentation monitor
        
        Args:
            changelog_url: URL of the changelog page
            litepaper_url: URL of the litepaper page
        """
        self.changelog_url = changelog_url
        self.litepaper_url = litepaper_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_changelog_updates(self) -> List[Dict[str, Any]]:
        """
        Check for changelog updates
        
        Returns:
            List of changelog entries
        """
        try:
            response = requests.get(self.changelog_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            entries = []
            
            # Look for changelog entries (adjust selectors based on actual HTML structure)
            # Common patterns: h2, h3 with dates, or article elements
            changelog_items = soup.find_all(['h2', 'h3', 'article'], limit=10)
            
            for item in changelog_items:
                # Try to extract version/date and content
                text = item.get_text(strip=True)
                
                # Skip if too short or just navigation elements
                if len(text) < 10 or 'Table of Contents' in text or 'Navigation' in text:
                    continue
                
                # Create unique ID from content hash
                content_hash = hashlib.md5(text.encode()).hexdigest()
                
                entry = {
                    'id': f"changelog:{content_hash}",
                    'title': text[:100] + ('...' if len(text) > 100 else ''),
                    'content': text[:500],
                    'url': self.changelog_url,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'date_obj': datetime.now(),
                    'type': 'changelog'
                }
                entries.append(entry)
            
            logger.info(f"Found {len(entries)} changelog entries")
            return entries[:5]  # Return top 5 most recent
            
        except Exception as e:
            logger.error(f"Error fetching changelog: {e}")
            return []
    
    def get_litepaper_updates(self) -> List[Dict[str, Any]]:
        """
        Check for litepaper changes by monitoring page hash
        
        Returns:
            List with litepaper update if changed
        """
        try:
            response = requests.get(self.litepaper_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content (skip navigation/footer)
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if not main_content:
                return []
            
            # Get text content and create hash
            content = main_content.get_text(strip=True)
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Extract title
            title_elem = soup.find('h1')
            title = title_elem.get_text(strip=True) if title_elem else "Zama Protocol Litepaper"
            
            entry = {
                'id': f"litepaper:{content_hash}",
                'title': title,
                'content': content[:500],
                'url': self.litepaper_url,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'date_obj': datetime.now(),
                'type': 'litepaper',
                'hash': content_hash
            }
            
            logger.info("Checked litepaper for updates")
            return [entry]
            
        except Exception as e:
            logger.error(f"Error fetching litepaper: {e}")
            return []

