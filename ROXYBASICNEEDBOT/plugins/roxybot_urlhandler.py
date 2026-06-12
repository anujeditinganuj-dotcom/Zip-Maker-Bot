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

import os
import re
import time
import aiohttp
import aiofiles
from urllib.parse import urlparse, unquote
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction
from config import RoxyBotConfig
from ROXYBASICNEEDBOT.modules.roxybot_zipmaker import roxybot_zipmaker
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
import logging

logger = logging.getLogger(__name__)

# Import user files from file handler
from ROXYBASICNEEDBOT.plugins.roxybot_filehandler import roxybot_user_files, roxybot_update_pinned_message, roxybot_get_file_buttons


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# URL Pattern Matching

# Direct link URL pattern
ROXYBOT_URL_PATTERN = re.compile(
    r'https?://(?:www\.)?'
    r'(?:'
    r'(?P<pixeldrain>pixeldrain\.com/u/[a-zA-Z0-9]+)|'
    r'(?P<gofile>gofile\.io/d/[a-zA-Z0-9]+)|'
    r'(?P<mediafire>mediafire\.com/file/[a-zA-Z0-9]+(?:/[^/\s]+)?)|'
    r'(?P<github>github\.com/[^/]+/[^/]+/releases/download/[^\s]+)|'
    r'(?P<dropbox>dropbox\.com/(?:s|scl)/[^\s]+)|'
    r'(?P<onedrive>1drv\.ms/[^\s]+)|'
    r'(?P<mega>mega\.nz/(?:file|folder)/[^\s]+)|'
    r'(?P<gdrive>drive\.google\.com/(?:file/d/[a-zA-Z0-9_-]+|uc\?[^\s]+))|'
    r'(?P<direct>[^\s]+\.(?:zip|rar|7z|tar|gz|mp4|mkv|avi|mp3|wav|pdf|doc|docx|xls|xlsx|jpg|jpeg|png|gif|apk|exe))(?:\?[^\s]*)?'
    r')',
    re.IGNORECASE
)

# Simple URL pattern for any HTTP/HTTPS link
ROXYBOT_SIMPLE_URL_PATTERN = re.compile(r'https?://[^\s]+', re.IGNORECASE)


def roxybot_is_valid_url(url: str) -> bool:
    """Check if string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def roxybot_get_filename_from_url(url: str, content_disposition: str = None) -> str:
    """Extract filename from URL or Content-Disposition header"""
    # Try Content-Disposition first
    if content_disposition:
        # Look for filename= or filename*=
        match = re.search(r'filename[*]?=["\']?([^"\';\s]+)', content_disposition)
        if match:
            return unquote(match.group(1))
    
    # Extract from URL path
    parsed = urlparse(url)
    path = parsed.path
    
    if path:
        filename = os.path.basename(unquote(path))
        if filename and '.' in filename:
            return filename
    
    # Default filename with timestamp
    return f"download_{int(time.time())}"


def roxybot_create_progress_bar(current: int, total: int, width: int = 10) -> str:
    """Create a retro checkbox style progress bar"""
    if total == 0:
        return "[☐☐☐☐☐☐☐☐☐☐] 0%"
    percentage = (current / total) * 100
    filled = int(width * current // total)
    bar = '☒' * filled + '☐' * (width - filled)
    return f"[{bar}] {percentage:.1f}%"


# Helper function to check if user is banned
async def roxybot_check_ban_url(message: Message) -> bool:
    """Check if user is banned. Returns True if banned."""
    user_id = message.from_user.id
    
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    if user_id in admin_ids:
        return False
    
    is_banned = await roxybot_db.roxybot_is_banned(user_id)
    if is_banned:
        await message.reply_text(
            "🚫 **Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ!**\n\n"
            "<blockquote>Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return True
    return False


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Main URL Download Function

async def roxybot_download_url(url: str, download_path: str, status_msg: Message) -> tuple:
    """
    Download file from URL with progress updates
    Returns: (success: bool, file_path: str, error: str)
    """
    try:
        # Create download directory if not exists
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        
        # Custom headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        timeout = aiohttp.ClientTimeout(total=3600)  # 1 hour timeout
        
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(url, allow_redirects=True) as response:
                if response.status != 200:
                    return False, None, f"HTTP Error: {response.status}"
                
                # Get file size
                total_size = int(response.headers.get('content-length', 0))
                
                # Get filename from headers or URL
                content_disposition = response.headers.get('content-disposition', '')
                filename = roxybot_get_filename_from_url(url, content_disposition)
                
                # Update download path with proper filename
                file_path = os.path.join(os.path.dirname(download_path), filename)
                
                # Download with progress
                downloaded = 0
                last_update = 0
                
                async with aiofiles.open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024 * 1024):  # 1MB chunks
                        await f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Update progress every 5%
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if progress - last_update >= 5:
                                last_update = progress
                                progress_bar = roxybot_create_progress_bar(downloaded, total_size)
                                try:
                                    await status_msg.edit_text(
                                        f"📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ғʀᴏᴍ URL...**\n\n"
                                        f"<blockquote>📄 {filename[:30]}...</blockquote>\n\n"
                                        f"{progress_bar}\n\n"
                                        f"📊 {roxybot_zipmaker.roxybot_format_size(downloaded)} / {roxybot_zipmaker.roxybot_format_size(total_size)}\n\n"
                                        f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
                                    )
                                except:
                                    pass
                
                return True, file_path, None
                
    except aiohttp.ClientError as e:
        return False, None, f"Connection error: {str(e)}"
    except Exception as e:
        return False, None, f"Download error: {str(e)}"


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# URL Message Handler

@Client.on_message(filters.text & filters.private & filters.regex(r'https?://'))
async def roxybot_handle_url(client: Client, message: Message):
    """Handle direct URL messages"""
    user_id = message.from_user.id
    
    # Skip if it's a command
    if message.text.startswith('/'):
        return
    
    # Check if user is banned
    if await roxybot_check_ban_url(message):
        return
    
    # Extract URL from message
    url_match = ROXYBOT_SIMPLE_URL_PATTERN.search(message.text)
    if not url_match:
        return
    
    url = url_match.group(0).strip()
    
    # Validate URL
    if not roxybot_is_valid_url(url):
        await message.reply_text(
            "❌ **Iɴᴠᴀʟɪᴅ URL!**\n\n"
            "<blockquote>Pʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ URL.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    logger.info("=" * 50)
    logger.info(f"🔗 URL RECEIVED")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info(f"🌐 URL: {url[:60]}...")
    logger.info("=" * 50)
    
    # Initialize user's file list
    if user_id not in roxybot_user_files:
        roxybot_user_files[user_id] = []
    
    # Show typing indicator
    await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    
    # Send status message
    status_msg = await message.reply_text(
        "🔗 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ғʀᴏᴍ URL...**\n\n"
        f"<blockquote>🌐 {url[:50]}...</blockquote>\n\n"
        "<blockquote>⚡ RᴏxʏBᴏᴛ ɪꜱ ᴘʀᴏᴄᴇꜱꜱɪɴɢ</blockquote>"
    )
    
    try:
        # Create download path
        download_path = f"{RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH}/{user_id}_{int(time.time())}_url_download"
        
        # Download the file
        success, file_path, error = await roxybot_download_url(url, download_path, status_msg)
        
        if not success:
            await status_msg.edit_text(
                f"❌ **Dᴏᴡɴʟᴏᴀᴅ Fᴀɪʟᴇᴅ!**\n\n"
                f"<blockquote>🚫 {error}</blockquote>\n\n"
                "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
            )
            return
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        # Add to user's file list
        roxybot_user_files[user_id].append(file_path)
        file_index = len(roxybot_user_files[user_id]) - 1
        
        logger.info(f"✅ URL downloaded: {file_path}")
        
        await status_msg.edit_text(
            f"✅ <b>URL Dᴏᴡɴʟᴏᴀᴅᴇᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!</b>\n\n"
            f"<blockquote>📦 <b>Fɪʟᴇ #{file_index + 1}</b> ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\n"
            f"📄 <b>Nᴀᴍᴇ:</b> <code>{file_name[:40]}</code>\n"
            f"💾 <b>Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(file_size)}</blockquote>\n\n"
            f"<blockquote>👉 Uꜱᴇ /create ᴛᴏ ᴍᴀᴋᴇ ZIP</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
            reply_markup=roxybot_get_file_buttons(file_index)
        )
        
        # Update pinned summary message
        await roxybot_update_pinned_message(client, message.chat.id, user_id)
        
        logger.info(f"✅ URL processed for user {user_id}, total files: {len(roxybot_user_files[user_id])}")
        
    except Exception as e:
        logger.error(f"❌ URL download error for user {user_id}: {type(e).__name__}: {e}", exc_info=True)
        await status_msg.edit_text(
            f"❌ **Eʀʀᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ URL:**\n\n"
            f"<blockquote>{str(e)}</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
