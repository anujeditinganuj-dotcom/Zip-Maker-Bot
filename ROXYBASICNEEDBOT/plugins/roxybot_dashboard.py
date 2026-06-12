# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# Admin Dashboard Module - View detailed bot analytics
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
from config import RoxyBotConfig
from datetime import datetime, timedelta
import logging
import psutil
import os

logger = logging.getLogger(__name__)


def roxybot_is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    return user_id in admin_ids


def roxybot_format_uptime(seconds: float) -> str:
    """Format uptime in human readable format"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}ᴅ")
    if hours > 0:
        parts.append(f"{hours}ʜ")
    if minutes > 0:
        parts.append(f"{minutes}ᴍ")
    
    return " ".join(parts) if parts else "< 1ᴍ"


def roxybot_format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


# Store bot start time
BOT_START_TIME = datetime.now()


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Admin Dashboard Command

@Client.on_message(filters.command(["dashboard", "admin", "panel"]) & filters.private)
async def roxybot_dashboard_command(client: Client, message: Message):
    """Show admin dashboard with bot analytics"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /dashboard")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if admin
    if not roxybot_is_admin(user_id):
        await message.reply_text(
            "❌ **Aᴄᴄᴇꜱꜱ Dᴇɴɪᴇᴅ!**\n\n"
            "Tʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴꜱ.\n\n"
            "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
        )
        return
    
    # Show loading message
    status_msg = await message.reply_text(
        "📊 **Lᴏᴀᴅɪɴɢ Dᴀꜱʜʙᴏᴀʀᴅ...**\n\n"
        "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
    )
    
    # Get statistics
    total_users = await roxybot_db.roxybot_get_total_users()
    
    # Get system info
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        memory_used = roxybot_format_size(memory.used)
        memory_total = roxybot_format_size(memory.total)
        disk_used = roxybot_format_size(disk.used)
        disk_total = roxybot_format_size(disk.total)
    except:
        cpu_percent = 0
        memory_used = "N/A"
        memory_total = "N/A"
        disk_used = "N/A"
        disk_total = "N/A"
        memory = type('obj', (object,), {'percent': 0})()
        disk = type('obj', (object,), {'percent': 0})()
    
    # Calculate uptime
    uptime_seconds = (datetime.now() - BOT_START_TIME).total_seconds()
    uptime_str = roxybot_format_uptime(uptime_seconds)
    
    # Build dashboard message
    dashboard_text = f"""
📊 **Aᴅᴍɪɴ Dᴀꜱʜʙᴏᴀʀᴅ**

━━━━━━━━━━━━━━━━━━

👥 **Uꜱᴇʀ Sᴛᴀᴛɪꜱᴛɪᴄꜱ:**
├ 📈 Tᴏᴛᴀʟ Uꜱᴇʀꜱ: **{total_users}**
├ ⏱️ Uᴘᴛɪᴍᴇ: **{uptime_str}**
└ 📅 Sᴛᴀʀᴛᴇᴅ: {BOT_START_TIME.strftime("%Y-%m-%d %H:%M")}

━━━━━━━━━━━━━━━━━━

💻 **Sʏꜱᴛᴇᴍ Sᴛᴀᴛᴜꜱ:**
├ 🔧 CPU: **{cpu_percent}%**
├ 🧠 RAM: **{memory_used}** / {memory_total} ({memory.percent}%)
└ 💾 Dɪꜱᴋ: **{disk_used}** / {disk_total} ({disk.percent}%)

━━━━━━━━━━━━━━━━━━

🤖 **Bᴏᴛ Iɴғᴏ:**
├ 📦 Vᴇʀꜱɪᴏɴ: **{RoxyBotConfig.ROXYBOT_VERSION}**
└ 🔧 Pʏᴛʜᴏɴ: **3.11+**

━━━━━━━━━━━━━━━━━━
⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**
"""
    
    # Create dashboard buttons
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📈 Dᴇᴛᴀɪʟᴇᴅ Sᴛᴀᴛꜱ", callback_data="roxybot_dash_stats"),
            InlineKeyboardButton("👥 Uꜱᴇʀ Lɪꜱᴛ", callback_data="roxybot_dash_users")
        ],
        [
            InlineKeyboardButton("📢 Bʀᴏᴀᴅᴄᴀꜱᴛ", callback_data="roxybot_dash_broadcast"),
            InlineKeyboardButton("🔄 Rᴇғʀᴇꜱʜ", callback_data="roxybot_dash_refresh")
        ],
        [
            InlineKeyboardButton("⚙️ Sᴇʀᴠᴇʀ Iɴғᴏ", callback_data="roxybot_dash_server")
        ]
    ])
    
    await status_msg.edit_text(dashboard_text, reply_markup=keyboard)
    logger.info(f"✅ Dashboard shown to admin {user_id}")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Dashboard callback handlers

@Client.on_callback_query(filters.regex("^roxybot_dash_"))
async def roxybot_dashboard_callback(client: Client, callback_query: CallbackQuery):
    """Handle dashboard button callbacks"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    # Check if admin
    if not roxybot_is_admin(user_id):
        await callback_query.answer("❌ Aᴅᴍɪɴ ᴏɴʟʏ!", show_alert=True)
        return
    
    if data == "roxybot_dash_refresh":
        await callback_query.answer("🔄 Rᴇғʀᴇꜱʜɪɴɢ...")
        await roxybot_refresh_dashboard(client, callback_query)
        
    elif data == "roxybot_dash_stats":
        await callback_query.answer("📈 Lᴏᴀᴅɪɴɢ ꜱᴛᴀᴛꜱ...")
        await roxybot_show_detailed_stats(client, callback_query)
        
    elif data == "roxybot_dash_users":
        await callback_query.answer("👥 Lᴏᴀᴅɪɴɢ ᴜꜱᴇʀꜱ...")
        await roxybot_show_user_list(client, callback_query)
        
    elif data == "roxybot_dash_broadcast":
        await callback_query.answer("📢 Uꜱᴇ /cast ᴄᴏᴍᴍᴀɴᴅ!")
        await callback_query.message.reply_text(
            "📢 **Bʀᴏᴀᴅᴄᴀꜱᴛ**\n\n"
            "Tᴏ ꜱᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ:\n"
            "1. Sᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ (ᴛᴇxᴛ/ᴘʜᴏᴛᴏ/ᴇᴛᴄ)\n"
            "2. Rᴇᴘʟʏ ᴛᴏ ɪᴛ ᴡɪᴛʜ /cast\n\n"
            "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
        )
        
    elif data == "roxybot_dash_server":
        await callback_query.answer("⚙️ Lᴏᴀᴅɪɴɢ...")
        await roxybot_show_server_info(client, callback_query)
        
    elif data == "roxybot_dash_back":
        await callback_query.answer("🔙 Bᴀᴄᴋ...")
        await roxybot_refresh_dashboard(client, callback_query)


async def roxybot_refresh_dashboard(client: Client, callback_query: CallbackQuery):
    """Refresh the dashboard"""
    total_users = await roxybot_db.roxybot_get_total_users()
    
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        memory_used = roxybot_format_size(memory.used)
        memory_total = roxybot_format_size(memory.total)
        disk_used = roxybot_format_size(disk.used)
        disk_total = roxybot_format_size(disk.total)
    except:
        cpu_percent = 0
        memory_used = "N/A"
        memory_total = "N/A"
        disk_used = "N/A"
        disk_total = "N/A"
        memory = type('obj', (object,), {'percent': 0})()
        disk = type('obj', (object,), {'percent': 0})()
    
    uptime_seconds = (datetime.now() - BOT_START_TIME).total_seconds()
    uptime_str = roxybot_format_uptime(uptime_seconds)
    
    dashboard_text = f"""
📊 **Aᴅᴍɪɴ Dᴀꜱʜʙᴏᴀʀᴅ**

━━━━━━━━━━━━━━━━━━

👥 **Uꜱᴇʀ Sᴛᴀᴛɪꜱᴛɪᴄꜱ:**
├ 📈 Tᴏᴛᴀʟ Uꜱᴇʀꜱ: **{total_users}**
├ ⏱️ Uᴘᴛɪᴍᴇ: **{uptime_str}**
└ 📅 Sᴛᴀʀᴛᴇᴅ: {BOT_START_TIME.strftime("%Y-%m-%d %H:%M")}

━━━━━━━━━━━━━━━━━━

💻 **Sʏꜱᴛᴇᴍ Sᴛᴀᴛᴜꜱ:**
├ 🔧 CPU: **{cpu_percent}%**
├ 🧠 RAM: **{memory_used}** / {memory_total} ({memory.percent}%)
└ 💾 Dɪꜱᴋ: **{disk_used}** / {disk_total} ({disk.percent}%)

━━━━━━━━━━━━━━━━━━

🤖 **Bᴏᴛ Iɴғᴏ:**
├ 📦 Vᴇʀꜱɪᴏɴ: **{RoxyBotConfig.ROXYBOT_VERSION}**
└ 🔧 Pʏᴛʜᴏɴ: **3.11+**

━━━━━━━━━━━━━━━━━━
⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📈 Dᴇᴛᴀɪʟᴇᴅ Sᴛᴀᴛꜱ", callback_data="roxybot_dash_stats"),
            InlineKeyboardButton("👥 Uꜱᴇʀ Lɪꜱᴛ", callback_data="roxybot_dash_users")
        ],
        [
            InlineKeyboardButton("📢 Bʀᴏᴀᴅᴄᴀꜱᴛ", callback_data="roxybot_dash_broadcast"),
            InlineKeyboardButton("🔄 Rᴇғʀᴇꜱʜ", callback_data="roxybot_dash_refresh")
        ],
        [
            InlineKeyboardButton("⚙️ Sᴇʀᴠᴇʀ Iɴғᴏ", callback_data="roxybot_dash_server")
        ]
    ])
    
    await callback_query.message.edit_text(dashboard_text, reply_markup=keyboard)


async def roxybot_show_detailed_stats(client: Client, callback_query: CallbackQuery):
    """Show detailed statistics"""
    total_users = await roxybot_db.roxybot_get_total_users()
    
    # Get today's stats
    today = datetime.now().strftime("%Y-%m-%d")
    
    stats_text = f"""
📈 **Dᴇᴛᴀɪʟᴇᴅ Sᴛᴀᴛɪꜱᴛɪᴄꜱ**

━━━━━━━━━━━━━━━━━━

👥 **Uꜱᴇʀꜱ:**
├ 📊 Tᴏᴛᴀʟ Rᴇɢɪꜱᴛᴇʀᴇᴅ: **{total_users}**
├ 📅 Tᴏᴅᴀʏ: {today}
└ 🌍 Gʀᴏᴡɪɴɢ ᴅᴀɪʟʏ!

━━━━━━━━━━━━━━━━━━

📦 **Bᴏᴛ Aᴄᴛɪᴠɪᴛʏ:**
├ 📁 ZIP Fɪʟᴇꜱ Cʀᴇᴀᴛᴇᴅ: Tʀᴀᴄᴋᴇᴅ
├ 🔐 Eɴᴄʀʏᴘᴛᴇᴅ ZIPꜱ: Aᴠᴀɪʟᴀʙʟᴇ
└ 🔗 Sʜᴀʀᴇ Lɪɴᴋꜱ: Aᴄᴛɪᴠᴇ

━━━━━━━━━━━━━━━━━━
⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 Bᴀᴄᴋ ᴛᴏ Dᴀꜱʜʙᴏᴀʀᴅ", callback_data="roxybot_dash_back")
        ]
    ])
    
    await callback_query.message.edit_text(stats_text, reply_markup=keyboard)


async def roxybot_show_user_list(client: Client, callback_query: CallbackQuery):
    """Show recent users"""
    all_users = await roxybot_db.roxybot_get_all_users()
    total = len(all_users) if all_users else 0
    
    # Get last 10 users
    recent_users = all_users[-10:] if all_users else []
    
    text = f"👥 **Rᴇᴄᴇɴᴛ Uꜱᴇʀꜱ**\n\n"
    text += f"📊 **Tᴏᴛᴀʟ:** {total}\n\n"
    text += "━━━━━━━━━━━━━━━━━━\n\n"
    
    if recent_users:
        for i, user in enumerate(reversed(recent_users), 1):
            name = user.get("first_name", "Unknown")[:15]
            uid = user.get("user_id", "N/A")
            text += f"{i}. **{name}** - `{uid}`\n"
    else:
        text += "Nᴏ ᴜꜱᴇʀꜱ ғᴏᴜɴᴅ.\n"
    
    text += "\n━━━━━━━━━━━━━━━━━━\n"
    text += "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 Bᴀᴄᴋ ᴛᴏ Dᴀꜱʜʙᴏᴀʀᴅ", callback_data="roxybot_dash_back")
        ]
    ])
    
    await callback_query.message.edit_text(text, reply_markup=keyboard)


async def roxybot_show_server_info(client: Client, callback_query: CallbackQuery):
    """Show detailed server information"""
    try:
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get process info
        process = psutil.Process(os.getpid())
        bot_memory = roxybot_format_size(process.memory_info().rss)
        
    except:
        cpu_count = "N/A"
        cpu_percent = 0
        memory = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})()
        disk = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})()
        bot_memory = "N/A"
    
    uptime_seconds = (datetime.now() - BOT_START_TIME).total_seconds()
    uptime_str = roxybot_format_uptime(uptime_seconds)
    
    server_text = f"""
⚙️ **Sᴇʀᴠᴇʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ**

━━━━━━━━━━━━━━━━━━

🔧 **CPU:**
├ Cᴏʀᴇꜱ: **{cpu_count}**
└ Uꜱᴀɢᴇ: **{cpu_percent}%**

🧠 **Mᴇᴍᴏʀʏ:**
├ Uꜱᴇᴅ: **{roxybot_format_size(memory.used)}**
├ Tᴏᴛᴀʟ: **{roxybot_format_size(memory.total)}**
└ Uꜱᴀɢᴇ: **{memory.percent}%**

💾 **Dɪꜱᴋ:**
├ Uꜱᴇᴅ: **{roxybot_format_size(disk.used)}**
├ Tᴏᴛᴀʟ: **{roxybot_format_size(disk.total)}**
└ Uꜱᴀɢᴇ: **{disk.percent}%**

🤖 **Bᴏᴛ Pʀᴏᴄᴇꜱꜱ:**
├ Mᴇᴍᴏʀʏ: **{bot_memory}**
└ Uᴘᴛɪᴍᴇ: **{uptime_str}**

━━━━━━━━━━━━━━━━━━
⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔙 Bᴀᴄᴋ ᴛᴏ Dᴀꜱʜʙᴏᴀʀᴅ", callback_data="roxybot_dash_back")
        ]
    ])
    
    await callback_query.message.edit_text(server_text, reply_markup=keyboard)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
