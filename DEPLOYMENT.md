# Deployment Guide

Deploy the Job Scraper to production environments.

## 🚀 Deployment Options

### Option 1: Local Server with Systemd (Linux)

1. **Create systemd service file**
   ```bash
   sudo nano /etc/systemd/system/job-scraper.service
   ```

2. **Add configuration**
   ```ini
   [Unit]
   Description=Job Scraper Service
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/path/to/Job-search-engine
   Environment="PATH=/path/to/Job-search-engine/venv/bin"
   ExecStart=/path/to/Job-search-engine/venv/bin/python app.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Start service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start job-scraper
   sudo systemctl enable job-scraper
   sudo systemctl status job-scraper
   ```

4. **View logs**
   ```bash
   sudo journalctl -u job-scraper -f
   ```

---

### Option 2: Docker Deployment

#### Local Docker
```bash
# Build image
docker build -t job-scraper:latest .

# Run container
docker run -d \
  --name job-scraper \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  job-scraper:latest

# View logs
docker logs -f job-scraper
```

#### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

### Option 3: Cloud Deployment

#### Heroku
1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create Procfile**
   ```
   web: python app.py
   ```

3. **Deploy**
   ```bash
   heroku create job-scraper
   git push heroku main
   heroku logs --tail
   ```

#### AWS EC2
1. **Launch instance** (Ubuntu 20.04 or later)

2. **Install dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip python3-venv \
     chromium-browser chromium-driver
   ```

3. **Setup project**
   ```bash
   git clone https://github.com/yourusername/Job-search-engine.git
   cd Job-search-engine
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Setup systemd service** (see Option 1)

5. **Configure security groups**
   - Allow inbound traffic on port 5000

#### Google Cloud Run
1. **Deploy with gcloud**
   ```bash
   gcloud run deploy job-scraper \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

#### Azure Container Instances
1. **Build image**
   ```bash
   az acr build --registry myregistry \
     --image job-scraper:latest .
   ```

2. **Deploy**
   ```bash
   az container create \
     --resource-group mygroup \
     --name job-scraper \
     --image myregistry.azurecr.io/job-scraper:latest \
     --ports 5000 \
     --cpu 1 \
     --memory 1
   ```

---

## 🔒 Production Security

### 1. SSL/TLS Configuration

Using Nginx as reverse proxy:
```nginx
server {
    listen 443 ssl;
    server_name job-scraper.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Environment Variables

Create `.env` file:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
```

### 3. Rate Limiting

Implement with Flask extensions:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/scrape', methods=['POST'])
@limiter.limit("5 per hour")
def start_scrape():
    pass
```

### 4. Authentication (Optional)

Add authentication for API endpoints:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == 'secret'

@app.route('/api/scrape', methods=['POST'])
@auth.login_required
def start_scrape():
    pass
```

---

## 📊 Monitoring & Logging

### 1. Application Monitoring

```bash
# Install monitoring tools
pip install prometheus-client

# Add to app.py
from prometheus_client import Counter, Histogram

scrape_requests = Counter('scrape_requests_total', 'Total scrape requests')
scrape_duration = Histogram('scrape_duration_seconds', 'Scrape duration')
```

### 2. Log Aggregation

Set up centralized logging:
```python
import logging.handlers

handler = logging.handlers.SysLogHandler(address=('logs.example.com', 514))
logger.addHandler(handler)
```

### 3. Health Checks

```python
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200
```

---

## 🔄 Continuous Deployment

### GitHub Actions Workflow

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push image
        run: |
          docker build -t job-scraper:latest .
          docker push myregistry/job-scraper:latest
      
      - name: Deploy to production
        run: |
          ssh user@server 'cd /path && docker-compose pull && docker-compose up -d'
```

---

## ⚙️ Performance Optimization

### 1. Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/jobs')
@cache.cached(timeout=3600)
def get_jobs():
    pass
```

### 2. Database

For production, consider adding database:
```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost/jobs')
```

### 3. Worker Queue

For long-running tasks:
```python
from celery import Celery

celery = Celery(app.name)

@celery.task
def scrape_jobs_async(role, location):
    scraper = JobScraper()
    return scraper.scrape_all_sources(role, location)
```

---

## 📋 Pre-deployment Checklist

- [ ] All tests passing
- [ ] Dependencies updated
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Rate limiting enabled
- [ ] Error handling tested
- [ ] Load testing done
- [ ] Documentation updated

---

## 🚨 Troubleshooting

### Container fails to start
```bash
docker logs <container_id>
```

### High memory usage
- Reduce `max_scrolls` parameter
- Implement job queue system
- Use process pooling

### Slow performance
- Add caching layer
- Use CDN for static files
- Implement database indexing

### Connection errors
- Check network connectivity
- Verify firewall rules
- Check proxy configuration

---

## 📞 Support

For deployment issues:
1. Check logs: `docker logs` or `journalctl`
2. Review deployment platform docs
3. Check GitHub issues
4. Contact maintainers

---

## 🔗 References

- [Docker Documentation](https://docs.docker.com/)
- [Heroku Deployment](https://devcenter.heroku.com/)
- [AWS EC2](https://docs.aws.amazon.com/ec2/)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.0.x/deploying/)
- [Nginx Proxy](https://nginx.org/en/docs/)
