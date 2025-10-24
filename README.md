# Zama Telegram News Bot

A Telegram bot that automatically monitors and posts updates about Zama (Fully Homomorphic Encryption) from multiple sources.

## Features

- 📝 **Blog Monitoring**: Tracks new posts from the Zama blog
- 🚀 **GitHub Releases**: Monitors releases from Zama repositories
- 🐦 **Twitter Updates**: Scrapes tweets from @zama_fhe
- 🤖 **Automatic Posting**: Posts updates to a Telegram channel
- 💾 **Smart Deduplication**: Tracks posted items to prevent spam
- ⏰ **Scheduled Checks**: Configurable interval for checking sources

## Requirements

- Python 3.8+
- Telegram Bot Token
- Telegram Channel (where bot will post)

## Installation

### 1. Clone or Download

Download this project to your local machine.

### 2. Create Virtual Environment

```bash
cd zama-telegram-bot
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Save your bot token

### 5. Create Telegram Channel

1. Create a new Telegram channel
2. Add your bot as an administrator
3. Get your channel ID:
   - For public channels: Use `@yourchannel`
   - For private channels: Use the numeric ID (e.g., `-1001234567890`)

### 6. Configure Environment

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_or_chat_id
CHECK_INTERVAL_HOURS=6
MAX_TWEETS_PER_CHECK=10
```

**Configuration Options:**

- `TELEGRAM_BOT_TOKEN` (required): Your bot token from BotFather
- `TELEGRAM_CHANNEL_ID` (required): Your channel username or ID
- `CHECK_INTERVAL_HOURS` (optional): Hours between checks (default: 6)
- `MAX_TWEETS_PER_CHECK` (optional): Maximum tweets per check (default: 10)
- `GITHUB_TOKEN` (optional): GitHub personal access token for higher rate limits

## Usage

### Running the Bot

```bash
python bot.py
```

The bot will:
1. Send a startup message to your channel
2. Check all sources immediately
3. Continue checking every N hours (configured interval)

### Testing Individual Sources

You can test each source independently:

```bash
# Test blog scraper
python test_sources.py blog

# Test GitHub monitor
python test_sources.py github

# Test Twitter scraper
python test_sources.py twitter
```

## Project Structure

```
zama-telegram-bot/
├── bot.py                      # Main bot application
├── config.py                   # Configuration loader
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
├── sources/
│   ├── __init__.py
│   ├── zama_blog.py           # Blog RSS/scraper
│   ├── github_monitor.py      # GitHub releases monitor
│   └── twitter_scraper.py     # Twitter scraper
├── utils/
│   ├── __init__.py
│   ├── storage.py             # JSON storage for tracking
│   └── formatter.py           # Message formatting
└── posted_items.json          # Auto-generated tracking file
```

## Deployment

### Option 1: Local Machine

Run the bot on your local machine:

```bash
python bot.py
```

Keep the terminal open. The bot will run indefinitely.

### Option 2: Background Process (Linux/Mac)

Use `screen` or `tmux`:

```bash
# Using screen
screen -S zamabot
python bot.py
# Press Ctrl+A, then D to detach

# Reattach later
screen -r zamabot
```

### Option 3: Systemd Service (Linux)

Create `/etc/systemd/system/zamabot.service`:

```ini
[Unit]
Description=Zama Telegram News Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/zama-telegram-bot
Environment="PATH=/path/to/zama-telegram-bot/venv/bin"
ExecStart=/path/to/zama-telegram-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable zamabot
sudo systemctl start zamabot
sudo systemctl status zamabot
```

### Option 4: Docker (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build and run:

```bash
docker build -t zamabot .
docker run -d --name zamabot --env-file .env zamabot
```

## Monitored Sources

### Blog
- Zama blog RSS feed: `https://www.zama.ai/rss.xml`
- Fallback: Web scraping from `https://www.zama.ai/blog`

### GitHub Repositories
- `zama-ai/fhevm`
- `zama-ai/tfhe-rs`
- `zama-ai/concrete-ml`
- `zama-ai/concrete`

### Twitter
- Account: `@zama_fhe`
- Method: Nitter instances (Twitter scraping alternatives)

## Troubleshooting

### Bot doesn't post

1. Check bot token is correct
2. Verify bot is admin in the channel
3. Check channel ID format (@ for public, numeric for private)
4. View logs in `bot.log`

### Twitter scraping fails

Nitter instances can be unreliable. The bot tries multiple instances automatically. Consider:
- Adjusting `MAX_TWEETS_PER_CHECK`
- Checking if nitter instances are operational
- Disabling Twitter if too problematic (comment out in `bot.py`)

### GitHub rate limiting

If you hit GitHub rate limits:
1. Create a GitHub Personal Access Token
2. Add to `.env`: `GITHUB_TOKEN=your_token`

### RSS feed issues

If blog RSS fails:
- Bot automatically falls back to web scraping
- Check internet connectivity
- Verify Zama blog URL is accessible

## Logs

Logs are written to:
- Console output (INFO level)
- `bot.log` file (all levels)

## Customization

### Adding More Repositories

Edit `config.py`:

```python
ZAMA_REPOS = [
    'zama-ai/fhevm',
    'zama-ai/tfhe-rs',
    'your-org/your-repo',  # Add here
]
```

### Changing Check Interval

Edit `.env`:

```env
CHECK_INTERVAL_HOURS=3  # Check every 3 hours
```

### Customizing Message Format

Edit `utils/formatter.py` to change how messages appear.

## Contributing

Feel free to submit issues or pull requests for improvements!

## License

MIT License - feel free to use and modify as needed.

## About Zama

Zama is building FHE (Fully Homomorphic Encryption) solutions for blockchain and AI. Learn more at [zama.ai](https://www.zama.ai).

---

**Note**: This bot scrapes public information and respects rate limits. Always comply with terms of service for all platforms.

