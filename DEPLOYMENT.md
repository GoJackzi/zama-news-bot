# Deployment Guide

This guide covers different deployment options for running your Zama Telegram News Bot in production.

## Option 1: Local Machine (Simplest)

Good for: Testing, personal use

```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

**Pros:**
- Very simple
- Good for testing
- No additional services needed

**Cons:**
- Stops when you close the terminal/computer
- Not suitable for 24/7 operation

## Option 2: Screen/Tmux (Linux/Mac)

Good for: Small VPS, long-running processes

### Using Screen

```bash
# Start a new screen session
screen -S zamabot

# Inside screen, activate venv and run
cd zama-telegram-bot
source venv/bin/activate
python bot.py

# Detach: Press Ctrl+A, then D

# List sessions
screen -ls

# Reattach
screen -r zamabot

# Kill session
screen -X -S zamabot quit
```

### Using Tmux

```bash
# Start new session
tmux new -s zamabot

# Inside tmux, run the bot
cd zama-telegram-bot
source venv/bin/activate
python bot.py

# Detach: Press Ctrl+B, then D

# List sessions
tmux ls

# Reattach
tmux attach -t zamabot

# Kill session
tmux kill-session -t zamabot
```

**Pros:**
- Simple to use
- Easy to monitor
- Can reattach to see logs

**Cons:**
- Doesn't restart on system reboot
- Manual management

## Option 3: Systemd Service (Linux) - Recommended

Good for: Production VPS, automatic restarts

### Create Service File

```bash
sudo nano /etc/systemd/system/zamabot.service
```

Add this content (adjust paths):

```ini
[Unit]
Description=Zama Telegram News Bot
After=network.target

[Service]
Type=simple
User=yourusername
Group=yourusername
WorkingDirectory=/home/yourusername/zama-telegram-bot
Environment="PATH=/home/yourusername/zama-telegram-bot/venv/bin"
ExecStart=/home/yourusername/zama-telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

# Logging
StandardOutput=append:/home/yourusername/zama-telegram-bot/systemd.log
StandardError=append:/home/yourusername/zama-telegram-bot/systemd-error.log

[Install]
WantedBy=multi-user.target
```

### Enable and Start

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable zamabot

# Start the service
sudo systemctl start zamabot

# Check status
sudo systemctl status zamabot

# View logs
sudo journalctl -u zamabot -f

# Restart
sudo systemctl restart zamabot

# Stop
sudo systemctl stop zamabot
```

**Pros:**
- Automatic restart on failure
- Starts on system boot
- Professional logging
- Easy management

**Cons:**
- Linux only
- Requires sudo/root access

## Option 4: Docker (Advanced)

Good for: Containerized deployments, cloud platforms

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run bot
CMD ["python", "bot.py"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  zamabot:
    build: .
    container_name: zama-news-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./posted_items.json:/app/posted_items.json
      - ./bot.log:/app/bot.log
```

### Build and Run

```bash
# Build image
docker build -t zamabot .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Or run directly
docker run -d \
  --name zamabot \
  --env-file .env \
  -v $(pwd)/posted_items.json:/app/posted_items.json \
  -v $(pwd)/bot.log:/app/bot.log \
  --restart unless-stopped \
  zamabot
```

**Pros:**
- Isolated environment
- Easy to move between systems
- Version control
- Works on any platform with Docker

**Cons:**
- Requires Docker knowledge
- Slightly more complex setup

## Option 5: Cloud Platforms

### Railway.app

1. Install Railway CLI
2. Login: `railway login`
3. Initialize: `railway init`
4. Add environment variables in dashboard
5. Deploy: `railway up`

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create zama-news-bot`
4. Set env vars: `heroku config:set TELEGRAM_BOT_TOKEN=...`
5. Create Procfile: `worker: python bot.py`
6. Deploy: `git push heroku main`
7. Scale: `heroku ps:scale worker=1`

### DigitalOcean/Linode/AWS EC2

1. Create a small droplet/instance ($5-10/month)
2. SSH into server
3. Clone repository
4. Follow systemd setup (Option 3)

### Replit

1. Import GitHub repo to Replit
2. Add secrets (environment variables)
3. Click Run
4. Use "Always On" feature (paid)

**Cloud Pros:**
- Professional hosting
- High uptime
- Managed services
- Scalable

**Cloud Cons:**
- Usually costs money
- May have restrictions
- More complex setup

## Monitoring and Maintenance

### Health Checks

Add to `bot.py` for monitoring:

```python
# Send daily status update
async def send_health_check(self):
    stats = {
        'blog': self.storage.get_posted_count('blog'),
        'github': self.storage.get_posted_count('github'),
        'twitter': self.storage.get_posted_count('twitter')
    }
    message = f"🤖 Bot Status: Running\n"
    message += f"Posted: {stats['blog']} blog, {stats['github']} releases, {stats['twitter']} tweets"
    await self.send_message(message)
```

### Log Rotation

For systemd:

```bash
sudo nano /etc/logrotate.d/zamabot
```

```
/home/yourusername/zama-telegram-bot/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### Backup

Backup the `posted_items.json` file periodically:

```bash
# Cron job (daily backup)
0 2 * * * cp /path/to/zama-telegram-bot/posted_items.json /path/to/backups/posted_items_$(date +\%Y\%m\%d).json
```

## Recommendations

| Use Case | Best Option |
|----------|-------------|
| Quick testing | Local Machine |
| Small VPS | Screen/Tmux |
| Production VPS | Systemd |
| Cloud deployment | Docker |
| Minimal setup | Railway/Heroku |

## Security Notes

1. **Never commit .env file** - Already in .gitignore
2. **Secure your VPS** - Use SSH keys, disable root login
3. **Keep dependencies updated** - Run `pip install -U -r requirements.txt` periodically
4. **Monitor logs** - Check for unusual activity
5. **Backup data** - Save `posted_items.json` regularly

## Troubleshooting

### Bot stops unexpectedly

- Check logs: `tail -f bot.log`
- Check system resources: `htop`
- Verify network connectivity
- Check if rate limited

### High memory usage

- Normal for Python bots
- Should stay under 100MB
- If higher, check for memory leaks

### Updates not posting

- Verify sources are accessible
- Check Telegram channel permissions
- Review logs for errors
- Test individual sources: `python test_sources.py all`

---

Need help? Check the main README.md or open an issue on GitHub.

