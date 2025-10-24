# Quick Setup Guide

Follow these steps to get your Zama News Bot running in under 10 minutes!

## Step 1: Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Choose a name (e.g., "Zama News Bot")
4. Choose a username (e.g., "zama_news_bot")
5. Copy the token that BotFather gives you (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Create Your Channel

1. In Telegram, create a new channel (not a group!)
2. Give it a name (e.g., "Zama Updates")
3. Make it public and choose a username (e.g., `@zama_updates_channel`)
   - OR keep it private (you'll need the channel ID)

## Step 3: Add Bot to Channel

1. Go to your channel settings
2. Click "Administrators"
3. Click "Add Administrator"
4. Search for your bot username
5. Add the bot and give it permission to "Post Messages"

## Step 4: Install Python Dependencies

Open a terminal/command prompt:

```bash
# Navigate to the project folder
cd zama-telegram-bot

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Or activate it (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Configure the Bot

Create a file named `.env` in the `zama-telegram-bot` folder:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL_ID=@zama_updates_channel
CHECK_INTERVAL_HOURS=6
```

Replace:
- `TELEGRAM_BOT_TOKEN` with your token from Step 1
- `TELEGRAM_CHANNEL_ID` with your channel username from Step 2 (including the @)

## Step 6: Test the Sources (Optional but Recommended)

Test if the bot can fetch data:

```bash
python test_sources.py blog
python test_sources.py github
python test_sources.py twitter
```

If you see data, you're good to go!

## Step 7: Run the Bot

```bash
python bot.py
```

You should see:
- A startup message posted to your channel
- Log messages showing the bot is checking sources
- Any new updates posted to the channel

## Step 8: Keep it Running

### Windows
Leave the terminal window open, or use:
```bash
pythonw bot.py
```

### Linux/Mac
Use screen:
```bash
screen -S zamabot
python bot.py
# Press Ctrl+A then D to detach
```

Reattach later with:
```bash
screen -r zamabot
```

## Troubleshooting

### "Error: TELEGRAM_BOT_TOKEN is required"
- Make sure you created the `.env` file
- Check the token is correctly copied
- No spaces around the `=` sign

### "Telegram error: Unauthorized"
- Double-check your bot token
- Make sure you copied it completely

### "Telegram error: Chat not found"
- Make sure bot is added as admin in the channel
- For public channels, use `@channelname`
- For private channels, use the numeric ID like `-1001234567890`

### How to get private channel ID?
1. Add the bot to your channel as admin
2. Forward any message from the channel to `@raw_data_bot`
3. Look for `forward_from_chat` -> `id` (use this number)

### Twitter scraping doesn't work
- This is normal - Nitter instances can be unreliable
- The bot will try multiple instances
- You can disable Twitter checking if needed

## Next Steps

- The bot will check for updates every 6 hours by default
- Adjust `CHECK_INTERVAL_HOURS` in `.env` to change frequency
- Check `bot.log` for detailed logs
- Monitor your channel for updates!

## Need Help?

Check the full README.md for more detailed information and advanced configuration options.

---

Happy monitoring! 🚀

