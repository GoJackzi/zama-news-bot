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
        Check for changelog updates with better parsing
        
        Returns:
            List of changelog entries
        """
        try:
            response = requests.get(self.changelog_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            entries = []
            
            # Look for changelog sections - typically h2 headings with date/version
            sections = soup.find_all(['h2', 'h3', 'section', 'article'])
            
            for section in sections:
                # Extract heading text
                heading = section.get_text(strip=True)
                
                # Skip navigation, TOC, etc.
                skip_keywords = ['Table of Contents', 'Navigation', 'Search', 'Menu', 'Sidebar']
                if any(keyword in heading for keyword in skip_keywords) or len(heading) < 5:
                    continue
                
                # Try to find associated content
                content_parts = []
                
                # Get next siblings until next heading
                next_elem = section.find_next_sibling()
                while next_elem and next_elem.name not in ['h1', 'h2', 'h3']:
                    if next_elem.name == 'p':
                        text = next_elem.get_text(strip=True)
                        if text:
                            content_parts.append(text)
                    elif next_elem.name in ['ul', 'ol']:
                        # Handle lists with bullet points
                        items = next_elem.find_all('li')
                        for item in items[:5]:  # Max 5 list items
                            text = item.get_text(strip=True)
                            if text:
                                content_parts.append(f"• {text}")
                    elif next_elem.name == 'div':
                        text = next_elem.get_text(strip=True)
                        if text and len(text) > 20:  # Only substantial divs
                            content_parts.append(text)
                    next_elem = next_elem.find_next_sibling()
                    if len(content_parts) >= 6:  # Limit total elements
                        break
                
                full_content = '\n'.join(content_parts)
                
                # Extract date if present in heading
                import re
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', heading)
                date_str = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
                
                # Create better title
                title = heading
                # If heading is just a date, try to get more context
                if re.match(r'^\d{4}-\d{2}-\d{2}$', heading.strip()):
                    if content_parts:
                        first_line = content_parts[0].split('\n')[0]
                        title = f"{heading}: {first_line[:60]}"
                
                # Create unique ID from title + date
                content_hash = hashlib.md5(f"{title}{date_str}".encode()).hexdigest()
                
                entry = {
                    'id': f"changelog:{content_hash}",
                    'title': title[:150],
                    'content': full_content[:600] if full_content else heading,
                    'url': self.changelog_url,
                    'date': date_str,
                    'date_obj': self._parse_changelog_date(date_str),
                    'type': 'changelog'
                }
                entries.append(entry)
            
            logger.info(f"Found {len(entries)} changelog entries")
            return entries[:5]  # Return top 5 most recent
            
        except Exception as e:
            logger.error(f"Error fetching changelog: {e}")
            return []
    
    def _parse_changelog_date(self, date_str: str) -> datetime:
        """Parse changelog date string"""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return datetime.now()
    
    def get_litepaper_updates(self, previous_content: str = None) -> List[Dict[str, Any]]:
        """
        Check for litepaper changes with detailed diff detection
        
        Args:
            previous_content: Previously stored litepaper content for comparison
            
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
            
            # Extract sections for detailed comparison
            sections = {}
            for heading in main_content.find_all(['h1', 'h2', 'h3']):
                heading_text = heading.get_text(strip=True)
                # Get content until next heading
                content_parts = []
                next_elem = heading.find_next_sibling()
                while next_elem and next_elem.name not in ['h1', 'h2', 'h3']:
                    if next_elem.name in ['p', 'ul', 'ol', 'div']:
                        text = next_elem.get_text(strip=True)
                        if text:
                            content_parts.append(text)
                    next_elem = next_elem.find_next_sibling()
                sections[heading_text] = ' '.join(content_parts)
            
            # Get full text and create hash
            content = main_content.get_text(strip=True)
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Extract title
            title_elem = soup.find('h1')
            title = title_elem.get_text(strip=True) if title_elem else "Zama Protocol Litepaper"
            
            # Detect changes if previous content provided
            changes = self._detect_litepaper_changes(sections, previous_content)
            
            entry = {
                'id': f"litepaper:{content_hash}",
                'title': title,
                'content': content[:500],
                'url': self.litepaper_url,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'date_obj': datetime.now(),
                'type': 'litepaper',
                'hash': content_hash,
                'sections': sections,
                'changes': changes
            }
            
            logger.info("Checked litepaper for updates")
            return [entry]
            
        except Exception as e:
            logger.error(f"Error fetching litepaper: {e}")
            return []
    
    def _detect_litepaper_changes(self, current_sections: dict, previous_content: str) -> dict:
        """Detect what changed in the litepaper"""
        changes = {
            'added_sections': [],
            'removed_sections': [],
            'modified_sections': [],
            'has_changes': False
        }
        
        if not previous_content:
            return changes
        
        try:
            import json
            previous_sections = json.loads(previous_content)
            
            # Find added sections
            for section in current_sections:
                if section not in previous_sections:
                    changes['added_sections'].append(section)
            
            # Find removed sections
            for section in previous_sections:
                if section not in current_sections:
                    changes['removed_sections'].append(section)
            
            # Find modified sections
            for section in current_sections:
                if section in previous_sections:
                    if current_sections[section] != previous_sections[section]:
                        changes['modified_sections'].append(section)
            
            changes['has_changes'] = bool(
                changes['added_sections'] or 
                changes['removed_sections'] or 
                changes['modified_sections']
            )
            
        except:
            # If comparison fails, just mark as changed
            changes['has_changes'] = True
        
        return changes

