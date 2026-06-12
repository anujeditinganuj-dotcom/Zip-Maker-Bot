# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Quick Start Guide for Roxy Zip Maker Bot

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get API Credentials

1. **Get API_ID and API_HASH:**
   - Go to https://my.telegram.org
   - Login with your phone number
   - Go to "API Development Tools"
   - Create an app and get your API_ID and API_HASH

2. **Get BOT_TOKEN:**
   - Open Telegram and search for @BotFather
   - Send `/newbot`
   - Follow instructions to create your bot
   - Copy the bot token

3. **Get MongoDB URI:**
   - Go to https://www.mongodb.com/cloud/atlas
   - Create a free account
   - Create a cluster
   - Click "Connect" → "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database password

### Step 2: Configure Bot

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your credentials:
   ```env
   API_ID=12345678
   API_HASH=your_api_hash_here
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=roxyzipmakerbotdb
   PORT=8080
   OWNER_ID=your_telegram_user_id
   ```

### Step 3: Install and Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

## 📱 Testing Your Bot

1. Open Telegram and search for your bot
2. Send `/start`
3. Send some photos or videos
4. Use `/create` to create a ZIP
5. Try `/rename` to rename the ZIP

## 🌐 Deploy on Render

### Quick Deploy Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial bot setup"
   git push origin main
   ```

2. **Create Web Service on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `roxy-zip-maker-bot`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python bot.py`

3. **Add Environment Variables:**
   - Add all variables from your `.env` file
   - Click "Create Web Service"

4. **Done!** Your bot is now live 24/7!

## 🎯 Bot Commands Reference

| Command | What it does |
|---------|--------------|  
| `/start` | Welcome message and bot info |
| `/help` | Show help guide |
| `/create` | Create ZIP from your files |
| `/stats` | See your usage stats |
| `/rename` | Rename your ZIP file |
| `/cancel` | Clear all collected files |

## 💡 Tips

- Send multiple files before using `/create`
- You can send photos, videos, and documents in any format
- Progress bars show download/upload progress
- Files are automatically deleted after ZIP creation
- Use simple, easy-to-remember commands

## 🔧 Troubleshooting

**Bot not responding?**
- Check if your BOT_TOKEN is correct
- Verify API_ID and API_HASH are numbers/text (not swapped)

**Database errors?**
- Check MongoDB URI is correct
- Ensure your IP is whitelisted in MongoDB Atlas
- Try using "0.0.0.0/0" for network access (development only)

**Files not downloading?**
- Check bot has permission to download files
- Ensure enough disk space is available

## 🌟 Features Overview

✅ **Clean Design:**
- Simple standard commands
- Custom copyright headers on every file
- Organized ROXYBASICNEEDBOT folder structure

✅ **Production Ready:**
- Flask keep-alive for 24/7 uptime
- MongoDB for user data storage
- Automatic file cleanup
- Beautiful progress indicators

✅ **Secure & Clean:**
- Environment variables for sensitive data
- Proper error handling
- No hardcoded credentials

---

**Need Help?**
- 📱 Telegram: https://t.me/roxybasicneedbot1
- 🌐 Website: https://roxybasicneedbot.unaux.com
- 📺 YouTube: @roxybasicneedbot

**© 2025 RoxyBasicNeedBot ⚡**
