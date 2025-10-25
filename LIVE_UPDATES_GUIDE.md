# Live Updates Configuration Guide

Your Zama News Bot now supports **near-real-time updates** by checking sources every few minutes instead of hours.

## 🚀 Quick Configuration for Live Updates

Edit your `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=@your_channel

# For LIVE updates - check every 5 minutes
CHECK_INTERVAL_HOURS=0
CHECK_INTERVAL_MINUTES=5
```

That's it! Your bot will now check for updates every 5 minutes.

## ⚡ Update Frequency Options

| Interval | Configuration | Use Case |
|----------|--------------|----------|
| **5 minutes** | `HOURS=0, MINUTES=5` | 🔥 **Maximum responsiveness** |
| **10 minutes** | `HOURS=0, MINUTES=10` | ⚡ Near real-time, less intensive |
| **15 minutes** | `HOURS=0, MINUTES=15` | 🚀 Fast updates, balanced |
| **30 minutes** | `HOURS=0, MINUTES=30` | ⚙️ Frequent but efficient |
| **1 hour** | `HOURS=1, MINUTES=0` | 📊 Regular updates |
| **6 hours** | `HOURS=6, MINUTES=0` | 💤 Periodic digest |

## 📊 Recommended Settings

### For News/Breaking Updates (Your Use Case)
```env
CHECK_INTERVAL_HOURS=0
CHECK_INTERVAL_MINUTES=5
```
**Why:** Zama posts are infrequent, so 5-10 minute checks ensure you catch everything quickly without overwhelming the sources.

### For High-Volume Feeds
```env
CHECK_INTERVAL_HOURS=0
CHECK_INTERVAL_MINUTES=10
```
**Why:** Prevents rate limiting and reduces server load.

### For Digest/Summary Style
```env
CHECK_INTERVAL_HOURS=1
CHECK_INTERVAL_MINUTES=0
```
**Why:** Good for less time-sensitive content.

## 🎯 How It Works

```
Bot starts → Immediate check
     ↓
Wait 5 minutes
     ↓
Check all sources (Blog, GitHub, Twitter)
     ↓
Post new items to channel
     ↓
Wait 5 minutes → Repeat
```

## ⚠️ Important Considerations

### 1. **Rate Limiting**

**Twitter (Nitter):**
- Nitter instances may block frequent requests
- 5-10 minutes is usually safe
- Bot automatically tries multiple instances

**GitHub API:**
- Free tier: 60 requests/hour (1 per minute)
- Authenticated: 5,000 requests/hour
- Bot checks 4 repos = 4 requests per check
- **Recommendation:** Add GitHub token for frequent checks

**Zama Blog:**
- RSS feed, virtually unlimited
- No rate limiting issues

### 2. **Resource Usage**

| Interval | Daily Checks | Network Usage | CPU Usage |
|----------|-------------|---------------|-----------|
| 5 min | 288 | Low | Very Low |
| 10 min | 144 | Very Low | Minimal |
| 30 min | 48 | Minimal | Negligible |
| 1 hour | 24 | Minimal | Negligible |

**Verdict:** Even at 5 minutes, resource usage is negligible.

### 3. **Add GitHub Token for Frequent Checks**

For checks more frequent than 15 minutes, add a GitHub token:

1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scope: `public_repo` (read access)
4. Copy token
5. Add to `.env`:
```env
GITHUB_TOKEN=ghp_your_token_here
```

This increases your rate limit from 60/hour to 5,000/hour.

## 📈 Expected Behavior

### With 5-Minute Checks:

**Scenario 1: New Blog Post**
- Zama publishes post at 10:00 AM
- Bot checks at 10:05 AM
- Post appears in channel at 10:05 AM
- **Latency: ~5 minutes maximum**

**Scenario 2: GitHub Release**
- Release published at 2:30 PM
- Bot checks at 2:35 PM
- Posted to channel at 2:35 PM
- **Latency: ~5 minutes maximum**

**Scenario 3: Tweet**
- Tweet posted at 5:12 PM
- Bot checks at 5:15 PM
- Posted to channel at 5:15 PM
- **Latency: ~3 minutes**

### Comparison to 6-Hour Checks:
- **Old:** Up to 6 hours latency
- **New (5 min):** Up to 5 minutes latency
- **72x faster!** 🚀

## 🔧 Advanced: Even Faster Updates

If you need updates faster than 5 minutes:

```env
# Check every 2 minutes (very aggressive)
CHECK_INTERVAL_HOURS=0
CHECK_INTERVAL_MINUTES=2
```

**⚠️ Warnings:**
- More likely to hit rate limits
- Requires GitHub token
- Twitter scraping may fail more often
- Only do this if you really need it

## 🎮 Testing Your Configuration

Test how fast your bot responds:

1. Change interval to `MINUTES=1` temporarily
2. Start bot: `python bot.py`
3. Watch the logs: you'll see checks every minute
4. Verify it's working
5. Change back to your preferred interval

## 📱 Real-World Performance

Based on typical Zama activity:

**Blog Posts:** ~1-2 per week
- With 5-min checks: Posted within 5 minutes ✓

**GitHub Releases:** ~2-4 per month
- With 5-min checks: Posted within 5 minutes ✓

**Tweets:** ~3-10 per week
- With 5-min checks: Posted within 5 minutes ✓
- Note: Twitter scraping can be unreliable

## 🚦 Monitoring Your Bot

Watch the logs to see activity:

```bash
tail -f bot.log
```

You'll see:
```
Scheduler started. Checking every 5 minutes
Starting update check at 2024-10-24 10:00:00
Checking blog updates...
Checking GitHub updates...
Checking Twitter updates...
Update check completed
```

## 💡 Pro Tips

1. **Start with 5 minutes** - It's fast enough for news
2. **Add GitHub token** - Prevents rate limiting
3. **Monitor logs** - Watch for errors
4. **Adjust as needed** - If too frequent, increase to 10 minutes

## 🎯 Your Optimal Configuration

For Zama news bot specifically:

```env
# Near-real-time updates, balanced performance
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=@your_channel
CHECK_INTERVAL_HOURS=0
CHECK_INTERVAL_MINUTES=5
MAX_TWEETS_PER_CHECK=10
GITHUB_TOKEN=your_github_token  # Recommended but optional
```

This gives you:
- ✅ Fast updates (5 min max latency)
- ✅ No rate limiting issues
- ✅ Low resource usage
- ✅ Reliable operation

## 🔄 Switching Between Modes

You can change the interval anytime:

1. Stop the bot (Ctrl+C)
2. Edit `.env` file
3. Restart: `python bot.py`
4. New interval takes effect immediately

No code changes needed!

---

**Ready for live updates?** Just set `CHECK_INTERVAL_MINUTES=5` and run your bot! 🚀


