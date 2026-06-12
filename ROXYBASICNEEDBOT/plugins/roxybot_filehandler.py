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
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatAction
from config import RoxyBotConfig
from ROXYBASICNEEDBOT.modules.roxybot_zipmaker import roxybot_zipmaker
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
import logging

logger = logging.getLogger(__name__)


# Helper function to check if user is banned
async def roxybot_check_ban(message: Message) -> bool:
    """Check if user is banned. Returns True if banned (should stop processing)."""
    user_id = message.from_user.id
    
    # Admins are never banned
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    if user_id in admin_ids:
        return False
    
    is_banned = await roxybot_db.roxybot_is_banned(user_id)
    if is_banned:
        await message.reply_text(
            "🚫 **Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ!**\n\n"
            "<blockquote>Yᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.\n\n"
            "Iғ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ, ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴀᴅᴍɪɴ.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return True
    return False

# Store user files temporarily
roxybot_user_files = {}

# Store pinned summary message IDs per user
roxybot_pinned_messages = {}

def roxybot_create_progress_bar(current: int, total: int, width: int = 10) -> str:
    """Create a retro checkbox style progress bar"""
    percentage = (current / total) * 100
    filled = int(width * current // total)
    bar = '☒' * filled + '☐' * (width - filled)
    
    return f"[{bar}] {percentage:.1f}%"


def roxybot_get_file_buttons(file_index: int) -> InlineKeyboardMarkup:
    """Create cancel button for individual file"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Tʜɪꜱ Fɪʟᴇ", callback_data=f"roxybot_cancel_file_{file_index}")]
    ])


def roxybot_get_summary_buttons() -> InlineKeyboardMarkup:
    """Create buttons for pinned summary message"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗑️ Cᴀɴᴄᴇʟ Aʟʟ", callback_data="roxybot_clear_all")
        ]
    ])


async def roxybot_update_pinned_message(client: Client, chat_id: int, user_id: int):
    """Update or create the pinned summary message"""
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        # No files, delete pinned message if exists
        if user_id in roxybot_pinned_messages:
            try:
                await client.delete_messages(chat_id, roxybot_pinned_messages[user_id])
            except:
                pass
            del roxybot_pinned_messages[user_id]
        return
    
    file_count = len(roxybot_user_files[user_id])
    
    # Calculate total size
    total_size = 0
    for f in roxybot_user_files[user_id]:
        if os.path.exists(f):
            total_size += os.path.getsize(f)
    
    summary_text = (
        f"<b>📁 Fɪʟᴇ Cᴏʟʟᴇᴄᴛɪᴏɴ Sᴜᴍᴍᴀʀʏ</b>\n\n"
        f"<blockquote>📦 <b>Tᴏᴛᴀʟ Fɪʟᴇꜱ:</b> {file_count}\n"
        f"💾 <b>Tᴏᴛᴀʟ Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(total_size)}\n\n"
        f"💡 Sᴇɴᴅ ᴍᴏʀᴇ ғɪʟᴇꜱ ᴏʀ ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ</blockquote>\n\n"
        f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )
    
    if user_id in roxybot_pinned_messages:
        # Update existing message
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=roxybot_pinned_messages[user_id],
                text=summary_text,
                reply_markup=roxybot_get_summary_buttons()
            )
        except Exception as e:
            logger.warning(f"Failed to update pinned message: {e}")
            # Message may have been deleted, create new one
            del roxybot_pinned_messages[user_id]
            await roxybot_update_pinned_message(client, chat_id, user_id)
    else:
        # Create new pinned message
        try:
            msg = await client.send_message(
                chat_id=chat_id,
                text=summary_text,
                reply_markup=roxybot_get_summary_buttons()
            )
            roxybot_pinned_messages[user_id] = msg.id
            
            # PIN THIS MESSAGE properly using client method
            try:
                await client.pin_chat_message(
                    chat_id=chat_id,
                    message_id=msg.id,
                    disable_notification=True,
                    both_sides=True
                )
                logger.info(f"✅ Pinned summary message for user {user_id}")
            except Exception as e:
                logger.warning(f"Failed to pin message: {e}")
                
        except Exception as e:
            logger.error(f"Failed to create pinned message: {e}")

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# File Handler - Download and process files

@Client.on_message(filters.photo & filters.private)
async def roxybot_handle_photo(client: Client, message: Message):
    """Handle photo messages"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await roxybot_check_ban(message):
        return
    
    logger.info("=" * 50)
    logger.info(f"📸 PHOTO RECEIVED")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info(f"📁 File ID: {message.photo.file_id[:20]}...")
    logger.info("=" * 50)
    
    # Initialize user's file list
    if user_id not in roxybot_user_files:
        roxybot_user_files[user_id] = []
    
    # Show typing indicator
    await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    
    roxy_status_msg = await message.reply_text("📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴘʜᴏᴛᴏ...**\n⚡ Aɴᴜᴊ Kᴜᴍᴀʀ ɪꜱ ᴘʀᴏᴄᴇꜱꜱɪɴɢ")
    
    try:
        # Download photo with progress
        roxy_file_path = await message.download(
            file_name=f"{RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH}/{user_id}_{int(time.time())}_{message.photo.file_unique_id}.jpg",
            progress=roxybot_download_progress,
            progress_args=(roxy_status_msg,)
        )
        
        logger.info(f"✅ Photo downloaded: {roxy_file_path}")
        
        roxybot_user_files[user_id].append(roxy_file_path)
        file_index = len(roxybot_user_files[user_id]) - 1
        file_size = os.path.getsize(roxy_file_path)
        
        await roxy_status_msg.edit_text(
            f"✅ <b>Pʜᴏᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!</b>\n\n"
            f"<blockquote>📦 <b>Fɪʟᴇ #{file_index + 1}</b> ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\n"
            f"📄 <b>Nᴀᴍᴇ:</b> <code>photo.jpg</code>\n"
            f"💾 <b>Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(file_size)}</blockquote>\n\n"
            f"<blockquote>👉 Uꜱᴇ /create ᴛᴏ ᴍᴀᴋᴇ ZIP</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
            reply_markup=roxybot_get_file_buttons(file_index)
        )
        
        # Update pinned summary message
        await roxybot_update_pinned_message(client, message.chat.id, user_id)
        
        logger.info(f"✅ Photo processed for user {user_id}, total files: {len(roxybot_user_files[user_id])}")
        
    except Exception as e:
        logger.error(f"❌ Photo download error for user {user_id}: {type(e).__name__}: {e}", exc_info=True)
        await roxy_status_msg.edit_text(f"❌ **Eʀʀᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴘʜᴏᴛᴏ:** {str(e)}")


@Client.on_message(filters.video & filters.private)
async def roxybot_handle_video(client: Client, message: Message):
    """Handle video messages"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await roxybot_check_ban(message):
        return
    
    logger.info("=" * 50)
    logger.info(f"🎥 VIDEO RECEIVED")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info(f"📁 File: {message.video.file_name or 'unnamed'}")
    logger.info("=" * 50)
    
    if user_id not in roxybot_user_files:
        roxybot_user_files[user_id] = []
    
    # Show typing indicator
    await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
    
    roxy_status_msg = await message.reply_text("📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...**\n⚡ Aɴᴜᴊ Kᴜᴍᴀʀ ɪꜱ ᴘʀᴏᴄᴇꜱꜱɪɴɢ")
    
    try:
        # Get file extension
        roxy_file_name = message.video.file_name or f"video_{message.video.file_unique_id}.mp4"
        
        roxy_file_path = await message.download(
            file_name=f"{RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH}/{user_id}_{int(time.time())}_{roxy_file_name}",
            progress=roxybot_download_progress,
            progress_args=(roxy_status_msg,)
        )
        
        logger.info(f"✅ Video downloaded: {roxy_file_path}")
        
        roxybot_user_files[user_id].append(roxy_file_path)
        file_index = len(roxybot_user_files[user_id]) - 1
        file_size = os.path.getsize(roxy_file_path)
        
        await roxy_status_msg.edit_text(
            f"✅ <b>Vɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!</b>\n\n"
            f"<blockquote>📦 <b>Fɪʟᴇ #{file_index + 1}</b> ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\n"
            f"📄 <b>Nᴀᴍᴇ:</b> <code>{roxy_file_name}</code>\n"
            f"💾 <b>Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(file_size)}</blockquote>\n\n"
            f"<blockquote>👉 Uꜱᴇ /create ᴛᴏ ᴍᴀᴋᴇ ZIP</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
            reply_markup=roxybot_get_file_buttons(file_index)
        )
        
        # Update pinned summary message
        await roxybot_update_pinned_message(client, message.chat.id, user_id)
        
        logger.info(f"✅ Video processed for user {user_id}, total files: {len(roxybot_user_files[user_id])}")
        
    except Exception as e:
        logger.error(f"❌ Video download error for user {user_id}: {type(e).__name__}: {e}", exc_info=True)
        await roxy_status_msg.edit_text(f"❌ **Eʀʀᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ:** {str(e)}")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Document & File Handler

@Client.on_message(filters.document & filters.private)
async def roxybot_handle_document(client: Client, message: Message):
    """Handle document messages"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await roxybot_check_ban(message):
        return
    
    logger.info("=" * 50)
    logger.info(f"📄 DOCUMENT RECEIVED")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info(f"📁 File: {message.document.file_name or 'unnamed'}")
    logger.info(f"📊 Size: {message.document.file_size} bytes")
    logger.info("=" * 50)
    
    if user_id not in roxybot_user_files:
        roxybot_user_files[user_id] = []
    
    # Show typing indicator
    await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    
    roxy_status_msg = await message.reply_text("📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴅᴏᴄᴜᴍᴇɴᴛ...**\n⚡ Aɴᴜᴊ Kᴜᴍᴀʀ ɪꜱ ᴘʀᴏᴄᴇꜱꜱɪɴɢ")
    
    try:
        roxy_file_name = message.document.file_name or f"document_{message.document.file_unique_id}"
        
        roxy_file_path = await message.download(
            file_name=f"{RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH}/{user_id}_{int(time.time())}_{roxy_file_name}",
            progress=roxybot_download_progress,
            progress_args=(roxy_status_msg,)
        )
        
        logger.info(f"✅ Document downloaded: {roxy_file_path}")
        
        roxybot_user_files[user_id].append(roxy_file_path)
        file_index = len(roxybot_user_files[user_id]) - 1
        file_size = os.path.getsize(roxy_file_path)
        
        await roxy_status_msg.edit_text(
            f"✅ <b>Dᴏᴄᴜᴍᴇɴᴛ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!</b>\n\n"
            f"<blockquote>📦 <b>Fɪʟᴇ #{file_index + 1}</b> ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\n"
            f"📄 <b>Nᴀᴍᴇ:</b> <code>{roxy_file_name}</code>\n"
            f"💾 <b>Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(file_size)}</blockquote>\n\n"
            f"<blockquote>👉 Uꜱᴇ /create ᴛᴏ ᴍᴀᴋᴇ ZIP</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
            reply_markup=roxybot_get_file_buttons(file_index)
        )
        
        # Update pinned summary message
        await roxybot_update_pinned_message(client, message.chat.id, user_id)
        
        logger.info(f"✅ Document processed for user {user_id}, total files: {len(roxybot_user_files[user_id])}")
        
    except Exception as e:
        logger.error(f"❌ Document download error for user {user_id}: {type(e).__name__}: {e}", exc_info=True)
        await roxy_status_msg.edit_text(f"❌ **Eʀʀᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴅᴏᴄᴜᴍᴇɴᴛ:** {str(e)}")


async def roxybot_download_progress(current: int, total: int, roxy_status_msg: Message):
    """Progress callback for downloads"""
    try:
        roxy_percentage = (current / total) * 100
        roxy_progress_bar = roxybot_create_progress_bar(current, total)
        
        # Update every 10%
        if int(roxy_percentage) % 10 == 0:
            await roxy_status_msg.edit_text(
                f"📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ...**\n\n"
                f"{roxy_progress_bar}\n\n"
                f"📊 {roxybot_zipmaker.roxybot_format_size(current)} / {roxybot_zipmaker.roxybot_format_size(total)}\n\n"
                f"⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
            )
    except:
        pass


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Callback handler for individual file removal

@Client.on_callback_query(filters.regex(r"^roxybot_cancel_file_(\d+)$"))
async def roxybot_cancel_file_callback(client: Client, callback_query: CallbackQuery):
    """Handle removal of individual file from queue"""
    user_id = callback_query.from_user.id
    
    # Extract file index from callback data
    file_index = int(callback_query.data.split("_")[-1])
    
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        await callback_query.answer("❌ Nᴏ ғɪʟᴇꜱ ɪɴ ǫᴜᴇᴜᴇ!", show_alert=True)
        return
    
    if file_index >= len(roxybot_user_files[user_id]):
        await callback_query.answer("❌ Fɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ!", show_alert=True)
        return
    
    # Remove the file
    removed_file = roxybot_user_files[user_id].pop(file_index)
    
    # Delete the actual file
    try:
        if os.path.exists(removed_file):
            os.remove(removed_file)
    except:
        pass
    
    remaining = len(roxybot_user_files[user_id])
    
    await callback_query.answer(f"✅ Fɪʟᴇ ʀᴇᴍᴏᴠᴇᴅ! {remaining} ғɪʟᴇꜱ ʀᴇᴍᴀɪɴɪɴɢ.")
    
    # Update the message to show file was removed
    await callback_query.message.edit_text(
        "<b>🗑️ Fɪʟᴇ Rᴇᴍᴏᴠᴇᴅ!</b>\n\n"
        f"<blockquote>📦 <b>Rᴇᴍᴀɪɴɪɴɢ ғɪʟᴇꜱ:</b> {remaining}</blockquote>\n\n"
        "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )
    
    # Update pinned summary message
    await roxybot_update_pinned_message(client, callback_query.message.chat.id, user_id)
    
    logger.info(f"✅ User {user_id} removed file at index {file_index}, {remaining} remaining")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
