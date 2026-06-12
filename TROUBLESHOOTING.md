# 🔧 Bot Not Responding - Troubleshooting Guide

## Quick Diagnosis

Run this test script first:
```bash
python test_bot.py
```

This will verify:
- ✅ Configuration is correct
- ✅ Bot token is valid
- ✅ Plugins are loading
- ✅ Bot account info

## Common Issues & Solutions

### 1. Bot Starting But Not Responding

**Symptoms:**
- Flask server runs fine (shows 200 OK)
- Bot shows "Bot started successfully"
- But doesn't respond to `/start` or any commands

**Solutions:**

#### A. Check if bot is already running elsewhere
```bash
# Stop all Python processes
# Then restart your bot
python bot.py
```

#### B. Delete session file and restart
```bash
# Stop bot (Ctrl+C)
del RoxyZipMakerBot.session
del RoxyZipMakerBot.session-journal
# Restart
python bot.py
```

#### C. Verify you're using the correct bot
- Make sure BOT_TOKEN in `.env` matches the bot you're testing
- Check bot username in startup logs
- Message the correct bot on Telegram

### 2. Import Errors

**Error:** `ModuleNotFoundError: No module named 'pyrogram'`

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

**Error:** `ImportError: cannot import name 'Client'`

**Solution:**
```bash
pip uninstall pyrogram pyrofork -y
pip install pyrofork TgCrypto
```

### 3. Plugin Loading Issues

**Error:** Bot starts but commands don't work

**Check:**
1. Verify all `__init__.py` files exist:
   ```
   ROXYBASICNEEDBOT/__init__.py
   ROXYBASICNEEDBOT/plugins/__init__.py
   ROXYBASICNEEDBOT/modules/__init__.py
   ```

2. Check folder structure:
   ```
   zipmaker/
   ├── bot.py
   ├── config.py
   └── ROXYBASICNEEDBOT/
       ├── __init__.py
       ├── plugins/
       │   ├── __init__.py
       │   ├── roxybot_start.py
       │   ├── roxybot_filehandler.py
       │   ├── roxybot_zipcreator.py
       │   └── roxybot_rename.py
       └── modules/
           ├── __init__.py
           ├── roxybot_database.py
           ├── roxybot_keepalive.py
           └── roxybot_zipmaker.py
   ```

###4. Database Connection Issues

**Error:** MongoDB connection failed

**Solutions:**
1. Check MONGODB_URI in `.env`
2. Verify network access to MongoDB
3. Check MongoDB Atlas IP whitelist (add 0.0.0.0/0 for testing)

Bot will still work without MongoDB, but stats won't be saved.

### 5. Environment Variables

**Error:** Config validation failed

**Check `.env` file:**
```env
API_ID=12345678
API_HASH=your_api_hash_here
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
```

**Get credentials:**
- API_ID & API_HASH: https://my.telegram.org
- BOT_TOKEN: @BotFather on Telegram
- MONGODB_URI: https://mongodb.com/cloud/atlas

### 6. Verify Bot is Connected

**Run test commands:**
1. Start bot: `python bot.py`
2. Look for this output:
   ```
   ✅ RoxyBot: Bot started successfully!
   ✅ RoxyBot: @your_bot_username is now running!
   🆔 Bot ID: 123456789
   ✅ RoxyBot: Plugins loaded from 'ROXYBASICNEEDBOT/plugins'
   ```

3. If you see "Warning - Plugins may not be loaded!":
   - Check folder structure
   - Ensure all `__init__.py` files exist
   - Restart bot

### 7. Test in Telegram

1. Find your bot on Telegram (use username from startup logs)
2. Send `/start`
3. Bot should reply immediately

**If no response:**
- Wait 10 seconds (first message can be slow)
- Check bot isn't muted/blocked
- Verify you're testing the right bot
- Check startup logs for errors

### 8. Flask Health Check

While bot is running, open browser:
```
http://localhost:8080/
```

Should see: "Bot is running successfully!"

### 9. Enable Debug Logging

Add to `bot.py` after imports:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

This will show all Telegram updates received.

### 10. Complete Reset

If nothing works:

```bash
# Stop bot
# Delete session files
del *.session*

# Reinstall dependencies
pip uninstall -y pyrogram pyrofork
pip install -r requirements.txt

# Verify config
python test_bot.py

# Start fresh
python bot.py
```

## Still Not Working?

1. **Check bot token:**
   - Go to @BotFather
   - Send `/mybots`
   - Select your bot
   - Verify token is correct

2. **Create new bot:**
   - Go to @BotFather
   - `/newbot`
   - Get new token
   - Update `.env`

3. **Check system:**
   - Python version: `python --version` (need 3.8+)
   - Pip: `pip --version`
   - Dependencies: `pip list | findstr pyrofork`

---

**© 2025 RoxyBasicNeedBot ⚡**
