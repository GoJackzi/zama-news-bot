"""
Change detection and diff utilities
"""
import difflib
from typing import Dict, List, Tuple, Any


def detect_changelog_changes(current_content: str, previous_content: str) -> Dict[str, Any]:
    """
    Detect what changed in a changelog entry
    
    Returns:
        dict with added, removed, modified lines
    """
    if not previous_content:
        return {
            'is_new': True,
            'added': [],
            'removed': [],
            'modified': [],
            'has_changes': False
        }
    
    # Split into lines
    current_lines = [line.strip() for line in current_content.split('\n') if line.strip()]
    previous_lines = [line.strip() for line in previous_content.split('\n') if line.strip()]
    
    # Use difflib to find differences
    differ = difflib.Differ()
    diff = list(differ.compare(previous_lines, current_lines))
    
    added = []
    removed = []
    
    for line in diff:
        if line.startswith('+ '):
            # New line added
            added.append(line[2:])
        elif line.startswith('- '):
            # Line removed
            removed.append(line[2:])
    
    return {
        'is_new': False,
        'added': added[:10],  # Limit to first 10
        'removed': removed[:10],
        'has_changes': bool(added or removed)
    }


def format_changelog_changes(changes: Dict[str, Any]) -> str:
    """Format changelog changes for display"""
    if changes.get('is_new'):
        return ""
    
    if not changes.get('has_changes'):
        return "\n<i>No changes detected</i>"
    
    message = "\n\n<b>📝 What Changed:</b>\n"
    
    # Added content
    added = changes.get('added', [])
    if added:
        message += f"\n<b>✅ Added ({len(added)}):</b>\n"
        for line in added[:5]:  # Show first 5
            # Truncate long lines
            display_line = line[:150] + '...' if len(line) > 150 else line
            message += f"  + {display_line}\n"
        if len(added) > 5:
            message += f"  + ...and {len(added) - 5} more\n"
    
    # Removed content
    removed = changes.get('removed', [])
    if removed:
        message += f"\n<b>❌ Removed ({len(removed)}):</b>\n"
        for line in removed[:5]:  # Show first 5
            display_line = line[:150] + '...' if len(line) > 150 else line
            message += f"  - {display_line}\n"
        if len(removed) > 5:
            message += f"  - ...and {len(removed) - 5} more\n"
    
    return message


def detect_text_changes(current: str, previous: str) -> Dict[str, Any]:
    """
    Detect changes between two text blocks
    Returns percentage changed and key differences
    """
    if not previous:
        return {
            'is_new': True,
            'percent_changed': 0,
            'added_count': 0,
            'removed_count': 0
        }
    
    # Calculate similarity
    similarity = difflib.SequenceMatcher(None, previous, current).ratio()
    percent_changed = int((1 - similarity) * 100)
    
    # Count changes
    current_lines = current.split('\n')
    previous_lines = previous.split('\n')
    
    diff = list(difflib.Differ().compare(previous_lines, current_lines))
    
    added_count = sum(1 for line in diff if line.startswith('+ '))
    removed_count = sum(1 for line in diff if line.startswith('- '))
    
    return {
        'is_new': False,
        'percent_changed': percent_changed,
        'added_count': added_count,
        'removed_count': removed_count,
        'has_changes': percent_changed > 5  # More than 5% change
    }

