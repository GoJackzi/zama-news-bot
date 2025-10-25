# Deploy to Railway.app (5 minutes)

Railway is the easiest way to deploy your bot 24/7 without keeping your PC on.

## Prerequisites
- GitHub account
- Railway account (sign up at railway.app)

## Step 1: Prepare Your Bot

Create a `Procfile` in `G:\zama-telegram-bot\`:
```
worker: python bot.py
```

## Step 2: Push to GitHub

```bash
cd G:\zama-telegram-bot

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/yourusername/zama-bot.git
git push -u origin main
```

## Step 3: Deploy to Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your `zama-bot` repository
6. Railway will auto-detect Python and deploy

## Step 4: Set Environment Variables

In Railway dashboard:
1. Go to your project → Variables
2. Add:
   - `TELEGRAM_BOT_TOKEN` = your_token
   - `TELEGRAM_CHANNEL_ID` = @your_channel
   - `CHECK_INTERVAL_HOURS` = 0
   - `CHECK_INTERVAL_MINUTES` = 5

## Step 5: Deploy

Click "Deploy" - your bot will start running 24/7!

## View Logs

Click "Logs" tab to see your bot activity in real-time.

## Cost

- Free trial: $5 credit
- After: ~$5/month
- Bot uses minimal resources

---

**Done!** Your bot now runs 24/7 without your PC being on! 🚀


