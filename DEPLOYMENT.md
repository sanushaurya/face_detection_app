# Deployment Guide

Complete guide for deploying the Face Attendance System.

## Pre-Deployment Checklist

- [ ] All training data prepared in `ml_model/data/`
- [ ] Embeddings trained with `python register.py`
- [ ] All tests passing
- [ ] Configuration reviewed in `ml_model/config.py`
- [ ] Database backup created (if upgrading)
- [ ] Documentation reviewed

## Local Deployment

### Option 1: Using Startup Scripts (Recommended)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

### Option 2: Manual Startup

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. **Install dependencies**
   ```bash
   cd ml_model
   pip install -r requirements.txt
   ```

3. **Train embeddings**
   ```bash
   python register.py
   ```

4. **Start backend**
   ```bash
   python app.py
   ```

5. **Open web interface**
   - Open `web_app/index.html` in browser
   - Allow camera access

## Production Deployment

### Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8+
- Nginx or Apache (for reverse proxy)
- SSL certificate (for HTTPS)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv -y

# Install system dependencies for OpenCV
sudo apt install libsm6 libxext6 libxrender-dev -y
```

### Step 2: Application Setup

```bash
# Clone repository
git clone <repository-url> /opt/face-attendance
cd /opt/face-attendance

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd ml_model
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Create database directory
mkdir -p /var/lib/face-attendance
chmod 755 /var/lib/face-attendance

# Update config to use production database
# Edit ml_model/config.py:
# SQLALCHEMY_DATABASE_URI = 'sqlite:////var/lib/face-attendance/attendance.db'
```

### Step 4: Systemd Service

Create `/etc/systemd/system/face-attendance.service`:

```ini
[Unit]
Description=Face Attendance System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/face-attendance/ml_model
Environment="PATH=/opt/face-attendance/venv/bin"
ExecStart=/opt/face-attendance/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable face-attendance
sudo systemctl start face-attendance
```

### Step 5: Nginx Configuration

Create `/etc/nginx/sites-available/face-attendance`:

```nginx
upstream face_attendance {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    # API proxy
    location /api/ {
        proxy_pass http://face_attendance;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location / {
        root /opt/face-attendance/web_app;
        try_files $uri $uri/ =404;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/face-attendance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --nginx -d your-domain.com
```

### Step 7: Firewall Configuration

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Monitoring

### Check Service Status

```bash
sudo systemctl status face-attendance
```

### View Logs

```bash
sudo journalctl -u face-attendance -f
```

### Monitor Database

```bash
# Check database size
ls -lh /var/lib/face-attendance/attendance.db

# Backup database
cp /var/lib/face-attendance/attendance.db /backup/attendance.db.$(date +%Y%m%d)
```

## Maintenance

### Regular Backups

```bash
# Create backup script
cat > /opt/face-attendance/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/face-attendance"
mkdir -p $BACKUP_DIR
cp /var/lib/face-attendance/attendance.db $BACKUP_DIR/attendance.db.$(date +%Y%m%d_%H%M%S)
# Keep only last 30 days
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
EOF

chmod +x /opt/face-attendance/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /opt/face-attendance/backup.sh
```

### Update Dependencies

```bash
cd /opt/face-attendance
source venv/bin/activate
cd ml_model
pip install --upgrade -r requirements.txt
sudo systemctl restart face-attendance
```

### Clean Old Records

```bash
# Create cleanup script
cat > /opt/face-attendance/cleanup.py << 'EOF'
from datetime import datetime, timedelta
from app import app, db, Attendance

with app.app_context():
    # Delete records older than 90 days
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    deleted = Attendance.query.filter(Attendance.timestamp < cutoff_date).delete()
    db.session.commit()
    print(f"Deleted {deleted} old records")
EOF

# Add to crontab
# 0 3 * * 0 cd /opt/face-attendance && source venv/bin/activate && python cleanup.py
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u face-attendance -n 50

# Check if port 5000 is in use
sudo lsof -i :5000

# Check permissions
ls -la /var/lib/face-attendance/
```

### High CPU Usage

- Reduce `VERIFY_INTERVAL` in `web_app/script.js`
- Reduce canvas resolution
- Limit `MAX_NUM_FACES` in config

### Database Locked

```bash
# Restart service
sudo systemctl restart face-attendance

# Check for stuck processes
ps aux | grep python
```

### SSL Certificate Issues

```bash
# Renew certificate
sudo certbot renew --force-renewal

# Check certificate expiry
sudo certbot certificates
```

## Performance Optimization

### Database Optimization

```bash
# Vacuum database
sqlite3 /var/lib/face-attendance/attendance.db "VACUUM;"

# Create indexes
sqlite3 /var/lib/face-attendance/attendance.db << 'EOF'
CREATE INDEX IF NOT EXISTS idx_name ON attendance(name);
CREATE INDEX IF NOT EXISTS idx_timestamp ON attendance(timestamp);
EOF
```

### Caching

Add to `ml_model/app.py`:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/embeddings')
@cache.cached(timeout=300)
def get_embeddings():
    # ... existing code
```

### Load Balancing

For multiple servers, use Nginx upstream:
```nginx
upstream face_attendance {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

## Security Hardening

### Update Configuration

Edit `ml_model/config.py`:
```python
DEBUG = False
TESTING = False
SECRET_KEY = 'generate-strong-random-key'
```

### Enable HTTPS Only

```python
# In app.py
@app.before_request
def enforce_https():
    if not request.is_secure and not app.debug:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

### Rate Limiting

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/attendance', methods=['POST'])
@limiter.limit("10 per minute")
def log_attendance():
    # ... existing code
```

## Rollback Procedure

```bash
# Stop service
sudo systemctl stop face-attendance

# Restore from backup
cp /backup/attendance.db.20240101 /var/lib/face-attendance/attendance.db

# Restart service
sudo systemctl start face-attendance
```

## Support

For deployment issues, check:
1. Service logs: `sudo journalctl -u face-attendance -f`
2. Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. System resources: `top`, `df -h`, `free -h`
