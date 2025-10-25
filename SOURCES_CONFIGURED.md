# Zama Bot - Configured Sources

Your bot has been customized to monitor exactly what you requested!

## ✅ What Your Bot Now Monitors

### 1. 📝 **Zama Blog** (Unchanged)
- **URL**: https://www.zama.ai/blog
- **RSS**: https://www.zama.ai/rss.xml
- **Posts about**: Official blog posts, articles, announcements

### 2. 🚀 **GitHub Releases** (Unchanged)
Monitoring 4 repositories:
- `zama-ai/fhevm`
- `zama-ai/tfhe-rs`
- `zama-ai/concrete-ml`
- `zama-ai/concrete`
- **Posts about**: New version releases

### 3. 🔀 **GitHub Merged PRs** (NEW!)
Same 4 repositories as above
- **What it monitors**: Pull requests merged to main/master branch
- **Posts about**: Code changes, features, bug fixes
- **Format**: Shows PR number, title, author, description

### 4. 📋 **Documentation Changelog** (NEW!)
- **URL**: https://docs.zama.ai/change-log
- **Posts about**: Documentation updates, new guides, API changes

### 5. 📄 **Protocol Litepaper** (NEW!)
- **URL**: https://docs.zama.ai/protocol/zama-protocol-litepaper
- **Posts about**: Updates to the Zama Protocol Litepaper
- **How it works**: Monitors page hash - posts only when content changes

### 6. 🔵 **System Status** (NEW!)
- **RSS**: https://status.zama.ai/feed.rss
- **Atom**: https://status.zama.ai/feed.atom
- **Posts about**: 
  - 🔴 Incidents & outages
  - ✅ Resolved issues
  - 🔧 Maintenance windows
  - ⚠️ Performance degradation
  - 🔵 General status updates

### 7. ❌ **Twitter** (REMOVED)
- Removed as requested (redundant with Zama's Telegram channel)

---

## 📊 Expected Update Frequency

| Source | Frequency | Updates Per Week (Est.) |
|--------|-----------|-------------------------|
| Blog | Weekly | 1-2 posts |
| GitHub Releases | Monthly | 2-4 releases |
| **GitHub PRs** | Daily | **10-30 merges** |
| **Changelog** | Weekly | **2-5 updates** |
| **Litepaper** | Rare | **~1 per month** |
| **Status** | As needed | **0-5 (during issues)** |

**Note**: GitHub PRs will be the most active source!

---

## 🎯 Sample Updates

### Merged PR:
```
🔀 Merged PR: zama-ai/fhevm

#123: Add new FHE multiplication operator
by @developer_name

Implements optimized multiplication for encrypted integers...

📅 2024-10-24 15:30 UTC
🔗 View PR
```

### Changelog:
```
📋 Documentation Changelog

v2.1.0 - API Updates

Added new documentation for the Gateway API, updated examples for...

📅 2024-10-24
🔗 View Changelog
```

### Litepaper:
```
📄 Litepaper Updated

Zama Protocol Litepaper

The Zama Protocol Litepaper has been updated with new information.

📅 2024-10-24
🔗 Read Litepaper
```

### System Status:
```
🔴 System Status: API Gateway Incident

The API Gateway is experiencing intermittent connectivity issues...

📅 2024-10-24 10:15 UTC
🔗 View Status Page
```

---

## 🔧 Configuration

All settings in `config.py`:

```python
# GitHub Repos (4 repos)
ZAMA_REPOS = [
    'zama-ai/fhevm',
    'zama-ai/tfhe-rs',
    'zama-ai/concrete-ml',
    'zama-ai/concrete'
]

# Documentation
ZAMA_CHANGELOG_URL = 'https://docs.zama.ai/change-log'
ZAMA_LITEPAPER_URL = 'https://docs.zama.ai/protocol/zama-protocol-litepaper'

# Status Page
ZAMA_STATUS_RSS = 'https://status.zama.ai/feed.rss'
ZAMA_STATUS_ATOM = 'https://status.zama.ai/feed.atom'

# Features
MONITOR_GITHUB_RELEASES = True
MONITOR_GITHUB_MERGES = True  # NEW!
```

---

## 🧪 Testing Your Sources

Test each source individually before running the bot:

```bash
# Test blog
python test_sources.py blog

# Test GitHub releases
python test_sources.py github

# Test GitHub PRs (NEW!)
python test_sources.py prs

# Test docs (changelog + litepaper) (NEW!)
python test_sources.py docs

# Test status page (NEW!)
python test_sources.py status

# Test everything
python test_sources.py all
```

---

## 📝 .env Configuration

Your `.env` file should look like this:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@your_channel

# Update Frequency (5 minutes for live updates)
CHECK_INTERVAL_HOURS=0
CHECK_INTERVAL_MINUTES=5

# Optional (recommended for PR monitoring)
GITHUB_TOKEN=your_github_token
```

---

## 📈 Storage Categories

The bot now tracks 6 types of content:

1. `blog` - Blog posts
2. `github` - Releases
3. `github_pr` - Merged PRs (NEW!)
4. `changelog` - Docs changelog (NEW!)
5. `litepaper` - Litepaper updates (NEW!)
6. `status` - Status updates (NEW!)

All stored in `posted_items.json` to prevent duplicates.

---

## 🚀 What Happens When You Run

```
Bot starts
    ↓
Sends startup message (lists all 6 sources)
    ↓
Checks all sources immediately
    ↓
Posts new content to channel
    ↓
Waits 5 minutes
    ↓
Repeats...
```

---

## ⚙️ Customization Options

### Disable PR Monitoring
Edit `config.py`:
```python
MONITOR_GITHUB_MERGES = False
```

### Add More Repos
Edit `config.py`:
```python
ZAMA_REPOS = [
    'zama-ai/fhevm',
    'zama-ai/tfhe-rs',
    'zama-ai/concrete-ml',
    'zama-ai/concrete',
    'your-org/your-repo',  # Add here
]
```

### Change PR Limit Per Repo
Edit `bot.py`, line ~154:
```python
prs = self.github_monitor.get_merged_prs(per_repo=5)  # Default: 3
```

---

## 📊 Performance Notes

### API Rate Limits

**Without GitHub Token:**
- 60 requests/hour
- With 4 repos + PRs = ~8 requests per check
- Can handle 7-8 checks/hour
- **5-minute checks may hit limits!**

**With GitHub Token:**
- 5,000 requests/hour
- No problems with 5-minute checks ✅

**Recommendation**: Add GitHub token to `.env` for reliable operation!

---

## 🎯 Ready to Run?

1. **Create `.env`** with your tokens
2. **Add GitHub token** (recommended)
3. **Test sources**: `python test_sources.py all`
4. **Run bot**: `python bot.py`
5. **Watch your channel** for updates!

---

## 🆘 Need Help?

- **Test failing?** Check URLs are accessible
- **No updates?** Run test_sources.py to debug
- **Rate limited?** Add GitHub token
- **Want to change sources?** Edit config.py

---

**Your bot is now configured exactly as requested!** 🎉

It will monitor all Zama sources except Twitter, with emphasis on:
- ✅ Documentation changes (changelog + litepaper)
- ✅ Code merges (GitHub PRs)
- ✅ System status (incidents & maintenance)


