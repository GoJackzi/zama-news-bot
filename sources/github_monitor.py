"""
GitHub releases monitor for Zama repositories
"""
import requests
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GitHubMonitor:
    """Monitor GitHub releases and merged PRs for Zama repositories"""
    
    def __init__(self, repos: List[str], github_token: str = None, monitor_merges: bool = True):
        """
        Initialize GitHub monitor
        
        Args:
            repos: List of repo names in format 'owner/repo'
            github_token: Optional GitHub token for higher rate limits
            monitor_merges: Whether to monitor merged PRs to main branch
        """
        self.repos = repos
        self.monitor_merges = monitor_merges
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Zama-News-Bot'
        }
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
    
    def get_latest_releases(self) -> List[Dict[str, Any]]:
        """
        Fetch latest releases from all monitored repositories
        
        Returns:
            List of release dictionaries
        """
        all_releases = []
        
        for repo in self.repos:
            try:
                releases = self._fetch_repo_releases(repo)
                all_releases.extend(releases)
            except Exception as e:
                logger.error(f"Error fetching releases for {repo}: {e}")
        
        # Sort by date, newest first
        all_releases.sort(key=lambda x: x.get('date_obj', datetime.min), reverse=True)
        
        return all_releases
    
    def get_merged_prs(self, per_repo: int = 3) -> List[Dict[str, Any]]:
        """
        Fetch recently merged PRs from all monitored repositories
        
        Args:
            per_repo: Number of merged PRs to fetch per repository
            
        Returns:
            List of merged PR dictionaries
        """
        if not self.monitor_merges:
            return []
        
        all_prs = []
        
        for repo in self.repos:
            try:
                prs = self._fetch_merged_prs(repo, per_repo)
                all_prs.extend(prs)
            except Exception as e:
                logger.error(f"Error fetching merged PRs for {repo}: {e}")
        
        # Sort by merge date, newest first
        all_prs.sort(key=lambda x: x.get('date_obj', datetime.min), reverse=True)
        
        return all_prs
    
    def _fetch_repo_releases(self, repo: str, per_page: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch releases for a specific repository
        
        Args:
            repo: Repository name in format 'owner/repo'
            per_page: Number of releases to fetch
            
        Returns:
            List of release dictionaries
        """
        url = f'https://api.github.com/repos/{repo}/releases'
        params = {'per_page': per_page}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            releases_data = response.json()
            releases = []
            
            for release in releases_data:
                # Skip drafts and pre-releases if desired
                if release.get('draft'):
                    continue
                
                release_info = {
                    'id': f"{repo}:{release['id']}",
                    'repo': repo,
                    'version': release.get('tag_name', release.get('name', 'Unknown')),
                    'name': release.get('name', ''),
                    'body': self._clean_body(release.get('body', '')),
                    'url': release.get('html_url', ''),
                    'date': self._format_date(release.get('published_at', '')),
                    'date_obj': self._parse_date(release.get('published_at', '')),
                    'is_prerelease': release.get('prerelease', False)
                }
                releases.append(release_info)
            
            logger.info(f"Fetched {len(releases)} releases from {repo}")
            return releases
            
        except requests.RequestException as e:
            logger.error(f"Request error for {repo}: {e}")
            return []
    
    def _clean_body(self, body: str) -> str:
        """Clean and truncate release body"""
        # Remove excessive newlines
        body = '\n'.join(line.strip() for line in body.split('\n') if line.strip())
        # Limit length
        if len(body) > 500:
            body = body[:500]
        return body
    
    def _format_date(self, date_str: str) -> str:
        """Format ISO date string to readable format"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M UTC')
        except:
            return date_str
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse ISO date string to datetime object"""
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.min
    
    def _fetch_merged_prs(self, repo: str, per_page: int = 3) -> List[Dict[str, Any]]:
        """
        Fetch recently merged PRs for a specific repository
        
        Args:
            repo: Repository name in format 'owner/repo'
            per_page: Number of PRs to fetch
            
        Returns:
            List of merged PR dictionaries
        """
        url = f'https://api.github.com/repos/{repo}/pulls'
        params = {
            'state': 'closed',
            'sort': 'updated',
            'direction': 'desc',
            'per_page': per_page * 2  # Fetch extra to filter merged ones
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            prs_data = response.json()
            merged_prs = []
            
            for pr in prs_data:
                # Only include merged PRs (not just closed)
                if not pr.get('merged_at'):
                    continue
                
                # Only include PRs to main/master branch
                base_branch = pr.get('base', {}).get('ref', '')
                if base_branch not in ['main', 'master']:
                    continue
                
                pr_info = {
                    'id': f"{repo}:pr:{pr['number']}",
                    'repo': repo,
                    'number': pr['number'],
                    'title': pr.get('title', 'Untitled PR'),
                    'body': self._clean_body(pr.get('body', '')),
                    'url': pr.get('html_url', ''),
                    'author': pr.get('user', {}).get('login', 'Unknown'),
                    'date': self._format_date(pr.get('merged_at', '')),
                    'date_obj': self._parse_date(pr.get('merged_at', '')),
                    'type': 'pr'
                }
                merged_prs.append(pr_info)
                
                # Stop when we have enough
                if len(merged_prs) >= per_page:
                    break
            
            logger.info(f"Fetched {len(merged_prs)} merged PRs from {repo}")
            return merged_prs
            
        except requests.RequestException as e:
            logger.error(f"Request error for {repo} PRs: {e}")
            return []

