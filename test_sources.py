"""
Test script for individual source monitors
"""
import sys
import asyncio
import logging
from pprint import pprint

import config
from sources.zama_blog import ZamaBlogMonitor
from sources.github_monitor import GitHubMonitor
from sources.docs_monitor import DocsMonitor
from sources.status_monitor import StatusMonitor

logging.basicConfig(level=logging.INFO)


def test_blog():
    """Test blog monitor"""
    print("\n" + "="*50)
    print("Testing Zama Blog Monitor")
    print("="*50 + "\n")
    
    monitor = ZamaBlogMonitor(
        rss_url=config.ZAMA_BLOG_RSS,
        blog_url=config.ZAMA_BLOG_URL
    )
    
    posts = monitor.get_latest_posts(max_posts=3)
    
    if posts:
        print(f"✓ Found {len(posts)} blog posts:\n")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
            print(f"   URL: {post['url']}")
            print(f"   Date: {post['date']}")
            print(f"   Summary: {post['summary'][:100]}...")
            print()
    else:
        print("✗ No blog posts found")


def test_github():
    """Test GitHub monitor"""
    print("\n" + "="*50)
    print("Testing GitHub Monitor")
    print("="*50 + "\n")
    
    monitor = GitHubMonitor(
        repos=config.ZAMA_REPOS,
        github_token=config.GITHUB_TOKEN
    )
    
    releases = monitor.get_latest_releases()
    
    if releases:
        print(f"✓ Found {len(releases)} releases:\n")
        for i, release in enumerate(releases[:5], 1):  # Show first 5
            print(f"{i}. {release['repo']} - {release['version']}")
            print(f"   URL: {release['url']}")
            print(f"   Date: {release['date']}")
            if release['is_prerelease']:
                print(f"   [PRE-RELEASE]")
            print()
    else:
        print("✗ No releases found")


def test_github_prs():
    """Test GitHub PR monitor"""
    print("\n" + "="*50)
    print("Testing GitHub PR Monitor")
    print("="*50 + "\n")
    
    monitor = GitHubMonitor(
        repos=config.ZAMA_REPOS,
        github_token=config.GITHUB_TOKEN,
        monitor_merges=True
    )
    
    prs = monitor.get_merged_prs(per_repo=3)
    
    if prs:
        print(f"✓ Found {len(prs)} merged PRs:\n")
        for i, pr in enumerate(prs[:5], 1):  # Show first 5
            print(f"{i}. {pr['repo']} #{pr['number']}")
            print(f"   {pr['title']}")
            print(f"   by @{pr['author']}")
            print(f"   URL: {pr['url']}")
            print(f"   Date: {pr['date']}")
            print()
    else:
        print("✗ No merged PRs found")


def test_docs():
    """Test documentation monitor"""
    print("\n" + "="*50)
    print("Testing Documentation Monitor")
    print("="*50 + "\n")
    
    monitor = DocsMonitor(
        changelog_url=config.ZAMA_CHANGELOG_URL,
        litepaper_url=config.ZAMA_LITEPAPER_URL
    )
    
    # Test changelog
    print("Checking Changelog...")
    changelog = monitor.get_changelog_updates()
    if changelog:
        print(f"✓ Found {len(changelog)} changelog entries:\n")
        for i, entry in enumerate(changelog[:3], 1):
            print(f"{i}. {entry['title']}")
            print(f"   URL: {entry['url']}")
            print()
    else:
        print("✗ No changelog entries found\n")
    
    # Test litepaper
    print("Checking Litepaper...")
    litepaper = monitor.get_litepaper_updates()
    if litepaper:
        print(f"✓ Found litepaper updates:\n")
        for entry in litepaper:
            print(f"   {entry['title']}")
            print(f"   URL: {entry['url']}")
            print(f"   Hash: {entry.get('hash', 'N/A')[:16]}...")
            print()
    else:
        print("✗ No litepaper found\n")


def test_status():
    """Test status monitor"""
    print("\n" + "="*50)
    print("Testing Status Monitor")
    print("="*50 + "\n")
    
    monitor = StatusMonitor(
        rss_url=config.ZAMA_STATUS_RSS,
        atom_url=config.ZAMA_STATUS_ATOM
    )
    
    updates = monitor.get_status_updates(max_items=5)
    
    if updates:
        print(f"✓ Found {len(updates)} status updates:\n")
        for i, update in enumerate(updates, 1):
            print(f"{i}. [{update['status_type'].upper()}] {update['title']}")
            print(f"   URL: {update['url']}")
            print(f"   Date: {update['date']}")
            print()
    else:
        print("✗ No status updates found")


def test_all():
    """Test all sources"""
    test_blog()
    test_github()
    test_github_prs()
    test_docs()
    test_status()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python test_sources.py [blog|github|prs|docs|status|all]")
        sys.exit(1)
    
    source = sys.argv[1].lower()
    
    if source == 'blog':
        test_blog()
    elif source == 'github':
        test_github()
    elif source in ['prs', 'pr', 'pulls']:
        test_github_prs()
    elif source == 'docs':
        test_docs()
    elif source == 'status':
        test_status()
    elif source == 'all':
        test_all()
    else:
        print(f"Unknown source: {source}")
        print("Valid options: blog, github, prs, docs, status, all")
        sys.exit(1)


if __name__ == '__main__':
    main()

