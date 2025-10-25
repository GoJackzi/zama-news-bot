# Complete Railway Deployment Guide

Deploy your Zama News Bot to Railway.app for 24/7 operation without keeping your PC on.

## 📋 Prerequisites

- [ ] GitHub account ([sign up here](https://github.com/join))
- [ ] Railway account ([sign up here](https://railway.app))
- [ ] Git installed on your PC ([download here](https://git-scm.com/downloads))
- [ ] Telegram bot token (from @BotFather)
- [ ] Telegram channel created and bot added as admin

---

## 🚀 Step-by-Step Deployment

### Step 1: Push Your Code to GitHub

#### 1.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `zama-news-bot` (or any name you like)
3. Description: "Zama FHE News Bot for Telegram"
4. Choose: **Private** (recommended) or Public
5. **DO NOT** initialize with README (we already have files)
6. Click **Create repository**

#### 1.2 Push Your Code

Open PowerShell or Command Prompt:

```bash
# Navigate to your project
cd G:\zama-telegram-bot

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Zama News Bot"

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/zama-news-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)
  - Get token at: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select scopes: `repo` (full control)
  - Copy the token and use it as password

---

### Step 2: Deploy to Railway

#### 2.1 Sign Up / Login

1. Go to https://railway.app
2. Click **Login**
3. Choose **Login with GitHub**
4. Authorize Railway to access your GitHub

#### 2.2 Create New Project

1. Click **New Project** (or **Start a New Project**)
2. Select **Deploy from GitHub repo**
3. If first time: Click **Configure GitHub App**
   - Select which repos Railway can access
   - Choose your `zama-news-bot` repository
   - Click **Install & Authorize**
4. Back in Railway, select your `zama-news-bot` repository
5. Railway will automatically:
   - Detect it's a Python project
   - Find `requirements.txt`
   - Find `Procfile`
   - Start building

#### 2.3 Wait for Initial Build

- You'll see "Building..." in the Railway dashboard
- This takes 2-5 minutes for first deployment
- Railway is installing all dependencies from `requirements.txt`

---

### Step 3: Configure Environment Variables

**IMPORTANT:** Your bot won't work until you add these variables!

#### 3.1 Open Variables Section

1. In Railway dashboard, click on your project
2. Click on the **Variables** tab (or **Environment Variables**)

#### 3.2 Add Required Variables

Click **New Variable** and add each of these:

| Variable Name | Value | Example |
|---------------|-------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | `123456789:ABCdefGHI...` |
| `TELEGRAM_CHANNEL_ID` | Your channel username or ID | `@zama_news_updates` |
| `CHECK_INTERVAL_HOURS` | `0` | `0` |
| `CHECK_INTERVAL_MINUTES` | `5` | `5` |

#### 3.3 Optional But Recommended

| Variable Name | Value | Why? |
|---------------|-------|------|
| `GITHUB_TOKEN` | Your GitHub personal access token | Avoids rate limiting for PR monitoring |

To get GitHub token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Scopes: Select `public_repo`
4. Copy token and paste in Railway

#### 3.4 Apply Changes

- Railway auto-saves variables
- After adding all variables, click **Redeploy** or wait for auto-redeploy

---

### Step 4: Monitor Deployment

#### 4.1 View Logs

1. Click on **Deployments** tab
2. Click on the latest deployment
3. Click **Logs**

You should see:
```
Starting Zama News Bot...
Zama News Bot initialized
Starting update check at 2024-10-24...
Checking blog updates...
Checking GitHub updates...
...
```

#### 4.2 Verify in Telegram

Check your Telegram channel - you should see:
```
🤖 Zama News Bot Started

Monitoring:
📝 Zama Blog
🚀 GitHub Releases
🔀 GitHub Merged PRs
📋 Documentation Changelog
📄 Protocol Litepaper
🔵 System Status

Stay tuned for updates...
```

---

### Step 5: Verify It's Working

#### 5.1 Check Logs Regularly

- Look for: `Update check completed`
- Should happen every 5 minutes
- Watch for any ERROR messages

#### 5.2 Test Manual Trigger (Optional)

In Railway dashboard:
1. Go to **Settings**
2. Under **Deploy Triggers**, you can manually trigger a redeploy
3. Or just wait for next scheduled check

---

## 🎛️ Railway Dashboard Overview

### Key Sections

**Deployments**
- See all deployments
- View build logs
- Check deployment status

**Logs**
- Real-time application logs
- See bot activity
- Debug errors

**Metrics**
- CPU usage (should be very low)
- Memory usage (~100-200 MB)
- Network usage (minimal)

**Variables**
- Manage environment variables
- Add/edit/delete variables

**Settings**
- Deployment settings
- Custom domains (not needed for bot)
- Sleep settings (keep bot awake)

---

## 💰 Railway Pricing

### Free Trial
- $5 credit when you sign up
- Good for ~1 month
- No credit card required initially

### After Free Trial
- Pay as you go
- ~$5-7/month for this bot
- Based on:
  - Compute time
  - Memory usage
  - Network egress

### Resource Usage
Your bot uses:
- **Memory**: ~100-200 MB
- **CPU**: Very low (only active during checks)
- **Network**: Minimal

---

## 🔧 Managing Your Bot

### Update Bot Code

When you make changes to your bot:

```bash
cd G:\zama-telegram-bot

# Make your changes to files

# Commit changes
git add .
git commit -m "Update: description of changes"

# Push to GitHub
git push

# Railway auto-deploys!
```

Railway will automatically:
1. Detect the push
2. Rebuild your bot
3. Redeploy with new code

### View Logs

```
Railway Dashboard → Your Project → Logs
```

### Restart Bot

```
Railway Dashboard → Deployments → Click latest → Restart
```

### Stop Bot Temporarily

```
Railway Dashboard → Settings → Pause Project
```

### Delete Deployment

```
Railway Dashboard → Settings → Danger Zone → Delete Project
```

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check:**
1. Variables are set correctly
2. `TELEGRAM_BOT_TOKEN` is valid
3. Bot is admin in channel
4. Logs for error messages

**Fix:**
- Verify all environment variables
- Check bot token with @BotFather
- Re-add bot to channel as admin

### "Chat not found" Error

**Problem:** Channel ID is wrong

**Fix:**
- For public channels: Use `@channelname`
- For private channels: Get numeric ID
  - Forward message from channel to @raw_data_bot
  - Look for `forward_from_chat` → `id`
  - Use that number (like `-1001234567890`)

### GitHub Rate Limiting

**Problem:** Too many API calls

**Fix:**
- Add `GITHUB_TOKEN` environment variable
- Increases limit from 60/hour to 5,000/hour

### Bot Stops After Some Time

**Problem:** Railway put it to sleep

**Fix:**
- Railway shouldn't sleep worker processes
- Check "Settings" → Make sure it's not paused
- Upgrade to paid plan if on free tier

### Updates Not Posting

**Check Logs:**
```
Found X new blog posts
Found X new releases
```

If all zeros:
- Sources might be down
- Run test locally: `python test_sources.py all`
- Check if bot has already posted those updates

---

## 📊 Expected Log Output

### Normal Operation

```
Starting Zama News Bot...
Scheduler started. Checking every 5 minutes
==================================================
Starting update check at 2024-10-24 10:00:00
Checking blog updates...
Found 0 new blog posts
Checking GitHub updates...
Found 0 new releases
Checking GitHub PR updates...
Found 1 new merged PRs
Message sent successfully
Checking documentation updates...
Found 0 changelog + 0 litepaper updates
Checking system status updates...
Found 0 new status updates
Update check completed
==================================================
```

### When New Content Found

```
Checking blog updates...
Fetched 3 posts from RSS feed
Found 1 new blog posts
Message sent successfully
```

---

## 🔄 Updating Configuration

### Change Check Interval

1. Go to Railway → Variables
2. Edit `CHECK_INTERVAL_MINUTES`
3. Change to desired value (e.g., `10` for 10 minutes)
4. Bot will auto-restart with new interval

### Add/Remove Monitored Repos

1. Edit `config.py` in your local files
2. Modify `ZAMA_REPOS` list
3. Commit and push to GitHub
4. Railway auto-deploys

---

## ✅ Success Checklist

After deployment, verify:

- [ ] Bot appears online in Railway logs
- [ ] Startup message posted to Telegram channel
- [ ] Logs show "Update check completed" every 5 minutes
- [ ] No ERROR messages in logs
- [ ] Environment variables all set
- [ ] GitHub token added (if monitoring PRs)

---

## 🆘 Getting Help

### Railway Support

- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app
- Status: https://status.railway.app

### Bot Issues

- Check `bot.log` locally: `python bot.py`
- Test sources: `python test_sources.py all`
- Review Railway logs for errors

---

## 📱 Railway Mobile App

Railway has a mobile app to monitor your bot:

- iOS: Search "Railway" in App Store
- Android: Search "Railway" in Play Store

You can:
- View logs on the go
- Check deployment status
- See resource usage
- Restart deployments

---

## 🎉 You're Done!

Your Zama News Bot is now running 24/7 on Railway!

**What happens next:**
1. Bot checks sources every 5 minutes
2. New content posted to your channel automatically
3. Railway keeps it running even when your PC is off
4. You can monitor via Railway dashboard

**Monthly cost:** ~$5-7 (after free trial)

**Maintenance:** Minimal - just monitor logs occasionally

---

**Need to make changes?** Edit code locally → commit → push → Railway auto-deploys!

**Want to stop?** Railway Dashboard → Settings → Pause Project

**Questions?** Check the logs first, then Railway Discord!


