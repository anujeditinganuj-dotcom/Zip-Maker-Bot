# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
# Instagram: roxybasicneedbot1
# Portfolio: https://aratt.ai/@roxybasicneedbot
# 
# Bot & Website Developer 🤖
# Creator of Roxy BasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
# 
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import asyncio
import logging
import requests
from datetime import datetime
from pyrogram import Client
from pyrogram.types import BotCommand
from pyrogram.errors import ChatWriteForbidden, ChatIdInvalid, ChannelPrivate
from config import RoxyBotConfig
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
from ROXYBASICNEEDBOT.modules.roxybot_keepalive import roxybot_start_server

# Configure logging with detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('roxybot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ASCII Art Banner
ROXYBOT_BANNER = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗  ██████╗ ██╗  ██╗██╗   ██╗    ██████╗  ██████╗ ║
║   ██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝    ██╔══██╗██╔═══██╗║
║   ██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝     ██████╔╝██║   ██║║
║   ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝      ██╔══██╗██║   ██║║
║   ██║  ██║╚██████╔╝██╔╝ ██╗   ██║       ██████╔╝╚██████╔╝║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚═════╝  ╚═════╝ ║
║                                                           ║
║              🤖 ZIP MAKER BOT ⚡                     ║
║              Created by Anuj Kumar                  ║
║              Version 1.0.0                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Main Bot Application

class RoxyZipMakerBot:
    """Main Bot Class"""
    
    def __init__(self):
        logger.info("🔧 RoxyBot: Initializing bot configuration...")
        
        # Validate configuration
        RoxyBotConfig.roxybot_validate_config()
        logger.info("✅ RoxyBot: Configuration validated successfully")
        
        # Initialize Pyrogram Client
        self.roxybot_app = Client(
            name="RoxyZipMakerBot",
            api_id=RoxyBotConfig.ROXYBOT_API_ID,
            api_hash=RoxyBotConfig.ROXYBOT_API_HASH,
            bot_token=RoxyBotConfig.ROXYBOT_BOT_TOKEN,
            plugins=dict(root="ROXYBASICNEEDBOT/plugins"),
            workdir="."
        )
        logger.info("✅ RoxyBot: Pyrogram client initialized")
        logger.info(f"📂 RoxyBot: Plugins directory: ROXYBASICNEEDBOT/plugins")

    def roxybot_clear_webhook(self):
        """Force clear webhook before starting"""
        try:
            url = f"https://api.telegram.org/bot{RoxyBotConfig.ROXYBOT_BOT_TOKEN}/deleteWebhook?drop_pending_updates=False"
            response = requests.get(url, timeout=10)
            result = response.json()
            logger.info(f"🔄 RoxyBot: Webhook clear status: {result}")
            return result.get('ok', False)
        except Exception as e:
            logger.error(f"⚠️ RoxyBot: Failed to clear webhook: {e}")
            return False

    async def roxybot_send_log_message(self, message: str):
        """Send message to log channel"""
        log_channel = RoxyBotConfig.ROXYBOT_LOG_CHANNEL
        
        if not log_channel or log_channel == 0:
            logger.warning("⚠️ RoxyBot: LOG_CHANNEL not configured, skipping log message")
            return False
        
        try:
            logger.info(f"📤 RoxyBot: Sending log message to channel {log_channel}")
            await self.roxybot_app.send_message(
                chat_id=log_channel,
                text=message,
                disable_web_page_preview=True
            )
            logger.info(f"✅ RoxyBot: Log message sent successfully to {log_channel}")
            return True
        except ChatWriteForbidden:
            logger.error(f"❌ RoxyBot: Bot cannot write to log channel {log_channel}. Make sure bot is admin!")
        except ChatIdInvalid:
            logger.error(f"❌ RoxyBot: Invalid log channel ID: {log_channel}")
        except ChannelPrivate:
            logger.error(f"❌ RoxyBot: Log channel {log_channel} is private or bot was kicked")
        except Exception as e:
            logger.error(f"❌ RoxyBot: Failed to send log message: {type(e).__name__}: {e}")
        
        return False
    
    async def roxybot_start(self):
        """Start the bot"""
        print(ROXYBOT_BANNER)
        print("\n🔄 RoxyBot: Initializing...")
        logger.info("=" * 60)
        logger.info("🚀 RoxyBot: Starting Roxy Zip Maker Bot...")
        logger.info("=" * 60)
        
        # Clear webhook first
        webhook_cleared = self.roxybot_clear_webhook()
        logger.info(f"🔄 RoxyBot: Webhook cleared: {webhook_cleared}")
        
        # Start Flask keep-alive server
        roxybot_start_server()
        logger.info("✅ RoxyBot: Keep-alive server started")
        
        # Connect to database
        db_connected = await roxybot_db.roxybot_connect()
        if db_connected:
            print("✅ RoxyBot: Database connected!")
            logger.info("✅ RoxyBot: MongoDB database connected successfully")
        else:
            print("⚠️ RoxyBot: Database connection failed (will retry)")
            logger.warning("⚠️ RoxyBot: MongoDB connection failed")
        
        # Start bot
        logger.info("🔄 RoxyBot: Starting Pyrogram client...")
        await self.roxybot_app.start()
        logger.info("✅ RoxyBot: Pyrogram client started successfully")
        
        # Register Commands with Telegram (auto-appear in menu when user types /)
        try:
            # Define all bot commands
            bot_commands = [
                BotCommand("start", "⚡ Sᴛᴀʀᴛ Tʜᴇ Bᴏᴛ"),
                BotCommand("help", "🆘 Gᴇᴛ Hᴇʟᴘ & Gᴜɪᴅᴇ"),
                BotCommand("create", "📦 Cʀᴇᴀᴛᴇ Aʀᴄʜɪᴠᴇ (ZIP/RAR/7z)"),
                BotCommand("files", "📁 Vɪᴇᴡ Qᴜᴇᴜᴇᴅ Fɪʟᴇꜱ"),
                BotCommand("addthumb", "🖼️ Sᴇᴛ Cᴜꜱᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ"),
                BotCommand("delthumb", "🗑️ Dᴇʟᴇᴛᴇ Tʜᴜᴍʙɴᴀɪʟ"),
                BotCommand("viewthumb", "👀 Vɪᴇᴡ Yᴏᴜʀ Tʜᴜᴍʙɴᴀɪʟ"),
                BotCommand("stats", "📊 Bᴏᴛ Sᴛᴀᴛɪꜱᴛɪᴄꜱ"),
                BotCommand("cancel", "🚫 Cᴀɴᴄᴇʟ Oᴘᴇʀᴀᴛɪᴏɴ"),
                BotCommand("ban", "⛔ Bᴀɴ Uꜱᴇʀ (Aᴅᴍɪɴ)"),
                BotCommand("unban", "✅ Uɴʙᴀɴ Uꜱᴇʀ (Aᴅᴍɪɴ)"),
                BotCommand("cast", "📢 Bʀᴏᴀᴅᴄᴀꜱᴛ (Aᴅᴍɪɴ)")
            ]
            
            # Register commands with specific scope
            from pyrogram.types import BotCommandScopeAllPrivateChats
            
            # Register using AllPrivateChats scope which is main one for bots
            try:
                await self.roxybot_app.set_bot_commands(
                    commands=bot_commands,
                    scope=BotCommandScopeAllPrivateChats()
                )
                logger.info(f"✅ RoxyBot: Commands registered with ScopeAllPrivateChats")
                print(f"✅ RoxyBot: {len(bot_commands)} commands registered successfully!")
            except Exception as e:
                logger.warning(f"⚠️ RoxyBot: Start scope failed, trying default: {e}")
                # Fallback to default
                await self.roxybot_app.set_bot_commands(
                    commands=bot_commands
                )
                print(f"✅ RoxyBot: Commands registered (Default scope)")
                
        except Exception as e:
            logger.error(f"❌ RoxyBot: Failed to register commands: {type(e).__name__}: {e}", exc_info=True)
            print(f"❌ RoxyBot: Command registration error: {e}")

        # Get bot info
        roxy_me = await self.roxybot_app.get_me()
        logger.info(f"✅ RoxyBot: Bot info retrieved - @{roxy_me.username} (ID: {roxy_me.id})")
        print("✅ RoxyBot: Bot started successfully!")
        print(f"✅ RoxyBot: @{roxy_me.username} is now running!")
        print(f"🆔 Bot ID: {roxy_me.id}")
        
        # Send startup message to log channel
        startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        startup_message = f"""
<b>🚀 ZIP MAKER BOT STARTED</b>

<blockquote>🤖 <b>Bot Info:</b>
├ Username: @{roxy_me.username}
├ Bot ID: <code>{roxy_me.id}</code>
├ Version: {RoxyBotConfig.ROXYBOT_VERSION}
└ Started: {startup_time}</blockquote>

<blockquote>📊 <b>System Status:</b>
├ Database: {'✅ Connected' if db_connected else '❌ Failed'}
├ Webhook: {'✅ Cleared' if webhook_cleared else '⚠️ Issue'}
└ Commands: ✅ Registered</blockquote>

<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>
"""
        
        log_sent = await self.roxybot_send_log_message(startup_message)
        if log_sent:
            print("✅ RoxyBot: Startup message sent to log channel!")
        else:
            print("⚠️ RoxyBot: Could not send startup message to log channel")
        
        # Check if plugins are loaded
        if hasattr(self.roxybot_app, 'plugins'):
            print(f"✅ RoxyBot: Plugins loaded from 'ROXYBASICNEEDBOT/plugins'")
            logger.info("✅ RoxyBot: Plugins loaded successfully")
        else:
            print("⚠️ RoxyBot: Warning - Plugins may not be loaded!")
            logger.warning("⚠️ RoxyBot: Plugins attribute not found")
        
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("⚡ RoxyBasicNeedBot - Zip Maker Bot")
        print("📱 Telegram: https://t.me/anujedits76")
        print("🌐 Website: https://t.me/anujedits76")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("💡 Send /start to your bot to test!")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        logger.info("=" * 60)
        logger.info("🎉 RoxyBot: Bot is fully operational and waiting for messages!")
        logger.info("=" * 60)
        
        # Keep bot running
        await asyncio.Event().wait()
    
    async def roxybot_stop(self):
        """Stop the bot"""
        print("\n🛑 RoxyBot: Stopping bot...")
        logger.info("🛑 RoxyBot: Shutting down...")
        
        # Send shutdown message to log channel
        shutdown_message = f"""
🛑 **ROXY ZIP MAKER BOT STOPPED**

━━━━━━━━━━━━━━━━━━━━━━
📅 Stopped: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━━━━━━━━━━━━━
"""
        await self.roxybot_send_log_message(shutdown_message)
        
        await self.roxybot_app.stop()
        print("✅ RoxyBot: Bot stopped successfully!")
        logger.info("✅ RoxyBot: Bot stopped successfully")

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Main Entry Point

async def main():
    """Main function"""
    logger.info("🔧 RoxyBot: Entering main function...")
    roxybot = RoxyZipMakerBot()
    try:
        await roxybot.roxybot_start()
    except KeyboardInterrupt:
        logger.info("⌨️ RoxyBot: Keyboard interrupt received")
        await roxybot.roxybot_stop()
    except Exception as e:
        logger.critical(f"❌ RoxyBot: Fatal error: {e}", exc_info=True)
        print(f"❌ RoxyBot: Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
