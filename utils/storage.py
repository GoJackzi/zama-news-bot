"""
Storage utilities for tracking posted items
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Storage:
    """Handles persistent storage of posted items"""
    
    def __init__(self, filename: str = 'posted_items.json'):
        self.filename = filename
        self.data = self._load()
    
    def _load(self) -> Dict[str, List[str]]:
        """Load posted items from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error reading {self.filename}, starting fresh")
                return self._get_empty_storage()
        return self._get_empty_storage()
    
    def _get_empty_storage(self) -> Dict[str, List[str]]:
        """Return empty storage structure"""
        return {
            'blog': [],
            'github': [],
            'twitter': [],
            'last_updated': None
        }
    
    def _save(self):
        """Save posted items to JSON file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving to {self.filename}: {e}")
    
    def is_posted(self, source: str, item_id: str) -> bool:
        """Check if an item has already been posted"""
        if source not in self.data:
            self.data[source] = []
        return item_id in self.data[source]
    
    def mark_posted(self, source: str, item_id: str):
        """Mark an item as posted"""
        if source not in self.data:
            self.data[source] = []
        
        if item_id not in self.data[source]:
            self.data[source].append(item_id)
            self.data['last_updated'] = datetime.now().isoformat()
            self._save()
            logger.info(f"Marked {source}:{item_id} as posted")
    
    def get_posted_count(self, source: str) -> int:
        """Get count of posted items for a source"""
        return len(self.data.get(source, []))
    
    def cleanup_old_items(self, source: str, keep_last: int = 100):
        """Keep only the last N items for a source to prevent unbounded growth"""
        if source in self.data and len(self.data[source]) > keep_last:
            self.data[source] = self.data[source][-keep_last:]
            self._save()
            logger.info(f"Cleaned up {source}, keeping last {keep_last} items")

