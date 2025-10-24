# Quick Reference Card

## Essential Commands

### First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with:
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=@your_channel

# 3. Test sources (optional)
python test_sources.py all

# 4. Run bot
python bot.py
```

### Running the Bot

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Manual:**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
python bot.py
```

### Testing

```bash
# Test individual sources
python test_sources.py blog
python test_sources.py github
python test_sources.py twitter
python test_sources.py all
```

### Systemd Service (Linux)

```bash
# Start
sudo systemctl start zamabot

# Stop
sudo systemctl stop zamabot

# Restart
sudo systemctl restart zamabot

# Status
sudo systemctl status zamabot

# Logs
sudo journalctl -u zamabot -f

# Enable on boot
sudo systemctl enable zamabot
```

### Docker

```bash
# Build
docker build -t zamabot .

# Run
docker run -d --name zamabot --env-file .env zamabot

# Logs
docker logs -f zamabot

# Stop
docker stop zamabot

# Remove
docker rm zamabot
```

### Using Screen (Linux/Mac)

```bash
# Start
screen -S zamabot
python bot.py
# Press Ctrl+A, D to detach

# List
screen -ls

# Reattach
screen -r zamabot

# Kill
screen -X -S zamabot quit
```

## File Locations

| File | Purpose |
|------|---------|
| `.env` | Configuration (create this!) |
| `bot.py` | Main bot application |
| `bot.log` | Runtime logs |
| `posted_items.json` | Tracking storage (auto-generated) |
| `requirements.txt` | Dependencies |

## Environment Variables

```env
# Required
TELEGRAM_BOT_TOKEN=123456789:ABC...
TELEGRAM_CHANNEL_ID=@channel

# Update Frequency (choose one approach)
# For LIVE updates (every 5 minutes):
CHECK_INTERVAL_HOURS=0
CHECK_INTERVAL_MINUTES=5

# For hourly updates:
# CHECK_INTERVAL_HOURS=1
# CHECK_INTERVAL_MINUTES=0

# Optional
MAX_TWEETS_PER_CHECK=10
GITHUB_TOKEN=ghp_...  # Recommended for frequent checks
```

## Telegram Setup

1. **Create Bot**: Message @BotFather → `/newbot`
2. **Create Channel**: New channel → Public/Private
3. **Add Bot**: Channel → Admins → Add bot → Post Messages ✓
4. **Get ID**: 
   - Public: `@channelname`
   - Private: Forward message to @raw_data_bot → Copy ID

## Common Issues

| Problem | Solution |
|---------|----------|
| "Bot token required" | Create `.env` file |
| "Chat not found" | Add bot as channel admin |
| "Unauthorized" | Check bot token |
| Twitter fails | Normal, uses fallback |
| Rate limited | Add GITHUB_TOKEN |

## Logs

```bash
# View logs
tail -f bot.log

# Last 50 lines
tail -n 50 bot.log

# Search for errors
grep ERROR bot.log

# Clear logs
> bot.log
```

## Monitoring

```bash
# Check if running (systemd)
systemctl status zamabot

# Check if running (screen)
screen -ls | grep zamabot

# Check if running (docker)
docker ps | grep zamabot

# Check process
ps aux | grep bot.py
```

## Updating

```bash
# Update dependencies
pip install -U -r requirements.txt

# Restart bot
# (use appropriate method based on deployment)
```

## Backup

```bash
# Backup tracking data
cp posted_items.json posted_items.backup.json

# Backup config
cp .env .env.backup
```

## URLs

- **Zama Website**: https://www.zama.ai
- **Zama Blog**: https://www.zama.ai/blog
- **Zama Twitter**: https://twitter.com/zama_fhe
- **GitHub**: https://github.com/zama-ai

## Support Files

- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Step-by-step setup
- `DEPLOYMENT.md` - Production deployment
- `LIVE_UPDATES_GUIDE.md` - Configure real-time updates
- `PROJECT_SUMMARY.md` - Technical overview
- `env.template` - Configuration template

## Need Help?

1. Check `bot.log` for errors
2. Read SETUP_GUIDE.md
3. Test sources: `python test_sources.py all`
4. Verify `.env` configuration
5. Check Telegram channel permissions

---

**Tip**: Keep this file handy for quick reference!

