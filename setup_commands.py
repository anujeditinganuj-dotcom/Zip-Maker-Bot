# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# Bot Menu Commands Setup Script
# Run this script once to set up the bot menu commands
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import asyncio
from pyrogram import Client
from pyrogram.types import BotCommand
from config import RoxyBotConfig

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Bot Menu Commands Configuration
# These will appear in Telegram's menu button

BOT_COMMANDS = [
    BotCommand("start", "Sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
    BotCommand("help", "Sʜᴏᴡ ʜᴇʟᴘ ᴍᴇꜱꜱᴀɢᴇ"),
    BotCommand("create", "Cʀᴇᴀᴛᴇ ZIP ғʀᴏᴍ ғɪʟᴇꜱ"),
    BotCommand("files", "Vɪᴇᴡ ǫᴜᴇᴜᴇᴅ ғɪʟᴇꜱ"),
    BotCommand("cancel", "Cᴀɴᴄᴇʟ ᴏᴘᴇʀᴀᴛɪᴏɴ"),
    BotCommand("stats", "Vɪᴇᴡ ʏᴏᴜʀ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ"),
    BotCommand("folder", "Mᴀɴᴀɢᴇ ғᴏʟᴅᴇʀ ꜱᴛʀᴜᴄᴛᴜʀᴇ"),
    BotCommand("share", "Cʀᴇᴀᴛᴇ ꜱʜᴀʀᴇ ʟɪɴᴋ"),
    BotCommand("mylinks", "Vɪᴇᴡ ᴍʏ ꜱʜᴀʀᴇ ʟɪɴᴋꜱ"),
    BotCommand("addthumb", "Sᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ"),
    BotCommand("delthumb", "Rᴇᴍᴏᴠᴇ ᴛʜᴜᴍʙɴᴀɪʟ"),
    BotCommand("viewthumb", "Vɪᴇᴡ ᴛʜᴜᴍʙɴᴀɪʟ"),
]

# Admin-only commands
ADMIN_COMMANDS = [
    BotCommand("dashboard", "Aᴅᴍɪɴ ᴅᴀꜱʜʙᴏᴀʀᴅ"),
    BotCommand("cast", "Bʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ"),
]


async def setup_bot_commands():
    """Set up bot menu commands"""
    print("🔧 Setting up bot menu commands...")
    
    app = Client(
        "roxybot_commands_setup",
        api_id=RoxyBotConfig.ROXYBOT_API_ID,
        api_hash=RoxyBotConfig.ROXYBOT_API_HASH,
        bot_token=RoxyBotConfig.ROXYBOT_BOT_TOKEN
    )
    
    async with app:
        # Set commands for all users
        await app.set_bot_commands(BOT_COMMANDS)
        print(f"✅ Set {len(BOT_COMMANDS)} public commands")
        
        # Set additional commands for admins
        admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
        all_admin_commands = BOT_COMMANDS + ADMIN_COMMANDS
        
        for admin_id in admin_ids:
            try:
                await app.set_bot_commands(
                    all_admin_commands,
                    scope="chat",
                    chat_id=admin_id
                )
                print(f"✅ Set admin commands for user {admin_id}")
            except Exception as e:
                print(f"⚠️ Could not set commands for {admin_id}: {e}")
        
        print("\n🎉 Bot menu commands set up successfully!")
        print("\n📋 Commands visible to users:")
        for cmd in BOT_COMMANDS:
            print(f"  /{cmd.command} - {cmd.description}")


if __name__ == "__main__":
    asyncio.run(setup_bot_commands())


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# To run this script:
# python setup_commands.py
# 
# This will set up the menu button for your bot.
# You only need to run this once!
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
