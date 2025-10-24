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
        Check for changelog updates with proper structure parsing
        
        Returns:
            List of changelog entries
        """
        try:
            response = requests.get(self.changelog_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            entries = []
            
            # Find main content area
            main = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if not main:
                return []
            
            # Look for h2 headings (main sections in changelog)
            headings = main.find_all('h2')
            
            for heading in headings:
                heading_text = heading.get_text(strip=True)
                
                # Skip navigation, TOC, etc.
                skip_keywords = ['Table of Contents', 'Navigation', 'Search', 'Menu', 'Sidebar', 'Change']
                if any(keyword in heading_text for keyword in skip_keywords) or len(heading_text) < 3:
                    continue
                
                # Collect content until next h2
                content_parts = []
                current = heading.find_next_sibling()
                
                while current and current.name != 'h2':
                    # Handle paragraphs
                    if current.name == 'p':
                        text = current.get_text(strip=True)
                        if text and len(text) > 10:  # Skip very short paragraphs
                            content_parts.append(('p', text))
                    
                    # Handle lists
                    elif current.name in ['ul', 'ol']:
                        list_items = []
                        for li in current.find_all('li', recursive=False):
                            li_text = li.get_text(strip=True)
                            if li_text:
                                list_items.append(li_text)
                        if list_items:
                            content_parts.append(('list', list_items[:8]))  # Max 8 items
                    
                    # Handle h3 subheadings
                    elif current.name == 'h3':
                        subheading = current.get_text(strip=True)
                        if subheading:
                            content_parts.append(('h3', subheading))
                    
                    current = current.find_next_sibling()
                    
                    # Limit content
                    if len(content_parts) >= 8:
                        break
                
                if not content_parts:
                    continue
                
                # Format content with proper structure
                formatted_content = self._format_changelog_content(content_parts)
                
                # Extract date
                import re
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', heading_text)
                date_str = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
                
                # Create entry
                content_hash = hashlib.md5(f"{heading_text}{date_str}".encode()).hexdigest()
                
                entry = {
                    'id': f"changelog:{content_hash}",
                    'title': heading_text[:150],
                    'content': formatted_content,
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
    
    def _format_changelog_content(self, content_parts: List) -> str:
        """Format changelog content with proper structure"""
        formatted = []
        
        for content_type, content in content_parts:
            if content_type == 'p':
                # Regular paragraph
                formatted.append(content[:250])  # Limit length
            elif content_type == 'h3':
                # Subheading
                formatted.append(f"<b>{content}</b>")
            elif content_type == 'list':
                # List items
                for item in content:
                    formatted.append(f"• {item[:200]}")
        
        return '\n'.join(formatted[:600])  # Join with single newlines
    
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

