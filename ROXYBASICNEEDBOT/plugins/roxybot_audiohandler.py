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
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import RoxyBotConfig
from ROXYBASICNEEDBOT.modules.roxybot_zipmaker import roxybot_zipmaker
from ROXYBASICNEEDBOT.plugins.roxybot_filehandler import roxybot_user_files, roxybot_pinned_messages, roxybot_get_file_buttons, roxybot_update_pinned_message
import logging

logger = logging.getLogger(__name__)

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Audio Handler Module - Handle audio and voice messages

def roxybot_create_progress_bar(current: int, total: int, width: int = 10) -> str:
    """Create a retro checkbox style progress bar"""
    percentage = (current / total) * 100
    filled = int(width * current // total)
    bar = '☒' * filled + '☐' * (width - filled)
    
    return f"[{bar}] {percentage:.1f}%"


@Client.on_message(filters.audio & filters.private)
async def roxybot_handle_audio(client: Client, message: Message):
    """Handle audio messages (MP3, etc.)"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"🎵 AUDIO RECEIVED")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info(f"📁 File: {message.audio.file_name or 'unnamed'}")
    logger.info(f"📊 Size: {message.audio.file_size} bytes")
    logger.info(f"⏱️ Duration: {message.audio.duration} seconds")
    logger.info("=" * 50)
    
    # Initialize user's file list
    if user_id not in roxybot_user_files:
        roxybot_user_files[user_id] = []
    
    roxy_status_msg = await message.reply_text("📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...**\n⚡ Aɴᴜᴊ Kᴜᴍᴀʀ ɪꜱ ᴘʀᴏᴄᴇꜱꜱɪɴɢ")
    
    try:
        # Get file extension and name
        roxy_file_name = message.audio.file_name or f"audio_{message.audio.file_unique_id}.mp3"
        
        roxy_file_path = await message.download(
            file_name=f"{RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH}/{user_id}_{int(time.time())}_{roxy_file_name}",
            progress=roxybot_audio_progress,
            progress_args=(roxy_status_msg,)
        )
        
        logger.info(f"✅ Audio downloaded: {roxy_file_path}")
        
        roxybot_user_files[user_id].append(roxy_file_path)
        file_index = len(roxybot_user_files[user_id]) - 1
        file_size = os.path.getsize(roxy_file_path)
        
        await roxy_status_msg.edit_text(
            f"✅ <b>Aᴜᴅɪᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!</b>\n\n"
            f"<blockquote>📦 <b>Fɪʟᴇ #{file_index + 1}</b> ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\n"
            f"📄 <b>Nᴀᴍᴇ:</b> <code>{roxy_file_name}</code>\n"
            f"💾 <b>Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(file_size)}</blockquote>\n\n"
            f"<blockquote>👉 Uꜱᴇ /create ᴛᴏ ᴍᴀᴋᴇ ZIP</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
            reply_markup=roxybot_get_file_buttons(file_index)
        )
        
        # Update pinned summary message
        await roxybot_update_pinned_message(client, message.chat.id, user_id)
        
        logger.info(f"✅ Audio processed for user {user_id}, total files: {len(roxybot_user_files[user_id])}")
        
    except Exception as e:
        logger.error(f"❌ Audio download error for user {user_id}: {type(e).__name__}: {e}", exc_info=True)
        await roxy_status_msg.edit_text(f"❌ **Eʀʀᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ:** {str(e)}")


@Client.on_message(filters.voice & filters.private)
async def roxybot_handle_voice(client: Client, message: Message):
    """Handle voice messages"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"🎤 VOICE MESSAGE RECEIVED")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info(f"⏱️ Duration: {message.voice.duration} seconds")
    logger.info("=" * 50)
    
    # Initialize user's file list
    if user_id not in roxybot_user_files:
        roxybot_user_files[user_id] = []
    
    roxy_status_msg = await message.reply_text("📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ...**\n⚡ Aɴᴜᴊ Kᴜᴍᴀʀ ɪꜱ ᴘʀᴏᴄᴇꜱꜱɪɴɢ")
    
    try:
        # Voice messages are OGG format
        roxy_file_name = f"voice_{message.voice.file_unique_id}.ogg"
        
        roxy_file_path = await message.download(
            file_name=f"{RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH}/{user_id}_{int(time.time())}_{roxy_file_name}",
            progress=roxybot_audio_progress,
            progress_args=(roxy_status_msg,)
        )
        
        logger.info(f"✅ Voice message downloaded: {roxy_file_path}")
        
        roxybot_user_files[user_id].append(roxy_file_path)
        file_index = len(roxybot_user_files[user_id]) - 1
        file_size = os.path.getsize(roxy_file_path)
        
        await roxy_status_msg.edit_text(
            f"✅ <b>Vᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!</b>\n\n"
            f"<blockquote>📦 <b>Fɪʟᴇ #{file_index + 1}</b> ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\n"
            f"📄 <b>Nᴀᴍᴇ:</b> <code>voice_msg.ogg</code>\n"
            f"💾 <b>Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(file_size)}</blockquote>\n\n"
            f"<blockquote>👉 Uꜱᴇ /create ᴛᴏ ᴍᴀᴋᴇ ZIP</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
            reply_markup=roxybot_get_file_buttons(file_index)
        )
        
        # Update pinned summary message
        await roxybot_update_pinned_message(client, message.chat.id, user_id)
        
        logger.info(f"✅ Voice processed for user {user_id}, total files: {len(roxybot_user_files[user_id])}")
        
    except Exception as e:
        logger.error(f"❌ Voice download error for user {user_id}: {type(e).__name__}: {e}", exc_info=True)
        await roxy_status_msg.edit_text(f"❌ **Eʀʀᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ:** {str(e)}")


async def roxybot_audio_progress(current: int, total: int, roxy_status_msg: Message):
    """Progress callback for audio downloads"""
    try:
        roxy_percentage = (current / total) * 100
        roxy_progress_bar = roxybot_create_progress_bar(current, total)
        
        # Update every 10%
        if int(roxy_percentage) % 10 == 0:
            await roxy_status_msg.edit_text(
                f"📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...**\n\n"
                f"{roxy_progress_bar}\n\n"
                f"📊 {roxybot_zipmaker.roxybot_format_size(current)} / {roxybot_zipmaker.roxybot_format_size(total)}\n\n"
                f"⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
            )
    except:
        pass


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
