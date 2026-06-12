# 🐳 Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

### 1️⃣ Setup Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MONGODB_URI=your_mongodb_uri
DATABASE_NAME=roxyzipmakerbotdb
PORT=8080
OWNER_ID=your_telegram_user_id
```

### 2️⃣ Build and Run with Docker Compose

```bash
# Build and start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### 3️⃣ Or Build and Run with Docker

```bash
# Build the image
docker build -t roxy-zip-bot .

# Run the container
docker run -d \
  --name roxy-zip-bot \
  --env-file .env \
  -p 8080:8080 \
  -v $(pwd)/downloads:/app/downloads \
  -v $(pwd)/zips:/app/zips \
  roxy-zip-bot

# View logs
docker logs -f roxy-zip-bot

# Stop the bot
docker stop roxy-zip-bot
docker rm roxy-zip-bot
```

## 🚀 Deploy to Cloud

### Deploy to Railway

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login and deploy:
   ```bash
   railway login
   railway init
   railway up
   ```

3. Add environment variables in Railway dashboard

### Deploy to Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Select Docker as the environment
4. Add environment variables
5. Deploy!

### Deploy to DigitalOcean

1. Create a Droplet with Docker
2. SSH into your droplet
3. Clone your repository
4. Run with docker-compose:
   ```bash
   git clone https://github.com/vyneet/zip.git
   cd zip
   cp .env.example .env
   # Edit .env with your credentials
   docker-compose up -d
   ```

## 📊 Monitoring

### Check container status
```bash
docker ps
```

### View logs
```bash
docker-compose logs -f
```

### Check health
```bash
curl http://localhost:8080/health
```

### Restart bot
```bash
docker-compose restart
```

## 🔧 Troubleshooting

**Container keeps restarting?**
- Check logs: `docker-compose logs`
- Verify environment variables in `.env`
- Ensure MongoDB URI is correct

**Can't connect to bot?**
- Verify BOT_TOKEN is correct
- Check if port 8080 is accessible
- Ensure firewall allows incoming connections

**Out of disk space?**
- Clean up old images: `docker system prune -a`
- Check downloads/zips folders

## 🛑 Stop and Remove

```bash
# Stop containers
docker-compose down

# Remove volumes (deletes downloaded files)
docker-compose down -v

# Remove images
docker rmi roxy-zip-bot
```

---

**© 2025 RoxyBasicNeedBot ⚡**
