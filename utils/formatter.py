"""
Message formatting utilities for Telegram
"""
from datetime import datetime
from typing import Dict, Any
import html


def escape_markdown(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return html.escape(text)


def format_blog_post(post: Dict[str, Any]) -> str:
    """Format a blog post for Telegram (HTML format)"""
    title = escape_html(post.get('title', 'Untitled'))
    url = post.get('url', '')
    summary = escape_html(post.get('summary', '')[:300])  # Limit summary length
    date = post.get('date', '')
    
    message = f"📝 <b>New Blog Post</b>\n\n"
    message += f"<b>{title}</b>\n\n"
    
    if summary:
        message += f"{summary}...\n\n"
    
    if date:
        message += f"📅 {date}\n"
    
    message += f"🔗 <a href='{url}'>Read more</a>"
    
    return message


def format_github_release(release: Dict[str, Any]) -> str:
    """Format a GitHub release for Telegram (HTML format)"""
    repo = escape_html(release.get('repo', 'Unknown'))
    version = escape_html(release.get('version', 'Unknown'))
    url = release.get('url', '')
    body = escape_html(release.get('body', '')[:400])  # Limit body length
    date = release.get('date', '')
    
    message = f"🚀 <b>New Release: {repo}</b>\n\n"
    message += f"<b>Version {version}</b>\n\n"
    
    if body:
        message += f"{body}...\n\n"
    
    if date:
        message += f"📅 {date}\n"
    
    message += f"🔗 <a href='{url}'>View release</a>"
    
    return message


def format_tweet(tweet: Dict[str, Any]) -> str:
    """Format a tweet for Telegram (HTML format)"""
    text = escape_html(tweet.get('text', ''))
    url = tweet.get('url', '')
    date = tweet.get('date', '')
    author = escape_html(tweet.get('author', '@zama_fhe'))
    
    message = f"🐦 <b>New Tweet from {author}</b>\n\n"
    message += f"{text}\n\n"
    
    if date:
        message += f"📅 {date}\n"
    
    message += f"🔗 <a href='{url}'>View on Twitter</a>"
    
    return message


def format_pr(pr: Dict[str, Any]) -> str:
    """Format a merged PR for Telegram (HTML format)"""
    repo = escape_html(pr.get('repo', 'Unknown'))
    number = pr.get('number', 0)
    title = escape_html(pr.get('title', 'Untitled'))
    author = escape_html(pr.get('author', 'Unknown'))
    url = pr.get('url', '')
    date = pr.get('date', '')
    body = escape_html(pr.get('body', '')[:300])
    
    message = f"🔀 <b>Merged PR: {repo}</b>\n\n"
    message += f"<b>#{number}: {title}</b>\n"
    message += f"by @{author}\n\n"
    
    if body:
        message += f"{body}...\n\n"
    
    if date:
        message += f"📅 {date}\n"
    
    message += f"🔗 <a href='{url}'>View PR</a>"
    
    return message


def format_changelog(entry: Dict[str, Any]) -> str:
    """Format a changelog entry for Telegram (HTML format)"""
    title = escape_html(entry.get('title', 'Changelog Update'))
    content = escape_html(entry.get('content', '')[:400])
    url = entry.get('url', '')
    date = entry.get('date', '')
    
    message = f"📋 <b>Documentation Changelog</b>\n\n"
    message += f"<b>{title}</b>\n\n"
    
    if content:
        message += f"{content}...\n\n"
    
    if date:
        message += f"📅 {date}\n"
    
    message += f"🔗 <a href='{url}'>View Changelog</a>"
    
    return message


def format_litepaper(entry: Dict[str, Any]) -> str:
    """Format a litepaper update for Telegram (HTML format)"""
    title = escape_html(entry.get('title', 'Litepaper Update'))
    url = entry.get('url', '')
    date = entry.get('date', '')
    changes = entry.get('changes', {})
    has_changes = changes.get('has_changes', False)
    
    message = f"📄 <b>Litepaper Updated</b>\n\n"
    message += f"<b>{title}</b>\n\n"
    
    if has_changes:
        message += f"✏️ <b>What Changed:</b>\n"
        
        # Added sections
        added = changes.get('added_sections', [])
        if added:
            message += f"\n📗 <b>Added ({len(added)}):</b>\n"
            for section in added[:3]:  # Show first 3
                message += f"  • {escape_html(section[:50])}\n"
            if len(added) > 3:
                message += f"  • ...and {len(added) - 3} more\n"
        
        # Modified sections
        modified = changes.get('modified_sections', [])
        if modified:
            message += f"\n📝 <b>Modified ({len(modified)}):</b>\n"
            for section in modified[:3]:  # Show first 3
                message += f"  • {escape_html(section[:50])}\n"
            if len(modified) > 3:
                message += f"  • ...and {len(modified) - 3} more\n"
        
        # Removed sections
        removed = changes.get('removed_sections', [])
        if removed:
            message += f"\n📕 <b>Removed ({len(removed)}):</b>\n"
            for section in removed[:3]:  # Show first 3
                message += f"  • {escape_html(section[:50])}\n"
            if len(removed) > 3:
                message += f"  • ...and {len(removed) - 3} more\n"
        
        message += f"\n"
    else:
        message += f"📝 New version of the Zama Protocol Litepaper.\n\n"
    
    if date:
        message += f"📅 {date}\n"
    
    message += f"🔗 <a href='{url}'>Read Full Litepaper</a>"
    
    return message


def format_status(update: Dict[str, Any]) -> str:
    """Format a status update for Telegram (HTML format)"""
    title = escape_html(update.get('title', 'Status Update'))
    content = escape_html(update.get('content', '')[:400])
    url = update.get('url', '')
    date = update.get('date', '')
    status_type = update.get('status_type', 'update')
    
    # Choose emoji based on status type
    emoji_map = {
        'incident': '🔴',
        'resolved': '✅',
        'maintenance': '🔧',
        'degraded': '⚠️',
        'update': '🔵'
    }
    emoji = emoji_map.get(status_type, '🔵')
    
    message = f"{emoji} <b>System Status: {title}</b>\n\n"
    
    if content:
        message += f"{content}...\n\n"
    
    if date:
        message += f"📅 {date}\n"
    
    message += f"🔗 <a href='{url}'>View Status Page</a>"
    
    return message


def format_error_message(source: str, error: str) -> str:
    """Format an error message (for logging/debugging)"""
    return f"⚠️ Error fetching {source}: {error}"


def format_startup_message() -> str:
    """Format bot startup message"""
    return (
        "🤖 <b>Zama News Bot Started</b>\n\n"
        "Monitoring:\n"
        "📝 Zama Blog\n"
        "🚀 GitHub Releases\n"
        "🔀 GitHub Merged PRs\n"
        "📋 Documentation Changelog\n"
        "📄 Protocol Litepaper\n"
        "🔵 System Status\n\n"
        "Stay tuned for updates about Fully Homomorphic Encryption!"
    )

