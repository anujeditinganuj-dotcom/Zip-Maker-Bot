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
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ROXYBASICNEEDBOT.plugins.roxybot_filehandler import roxybot_user_files
from ROXYBASICNEEDBOT.modules.roxybot_zipmaker import roxybot_zipmaker
import logging

logger = logging.getLogger(__name__)

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Files List Module - View and manage queued files

def roxybot_get_file_info(file_path: str) -> dict:
    """Get file information from path"""
    try:
        basename = os.path.basename(file_path)
        # Remove user_id and timestamp prefix
        parts = basename.split("_", 2)
        if len(parts) >= 3:
            display_name = parts[2]
        else:
            display_name = basename
        
        # Get file size
        size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        # Get file type from extension
        ext = os.path.splitext(display_name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            file_type = "📸 Pʜᴏᴛᴏ"
        elif ext in ['.mp4', '.mkv', '.avi', '.mov', '.webm']:
            file_type = "🎥 Vɪᴅᴇᴏ"
        elif ext in ['.mp3', '.flac', '.wav', '.ogg', '.m4a']:
            file_type = "🎵 Aᴜᴅɪᴏ"
        elif ext in ['.pdf']:
            file_type = "📄 PDF"
        elif ext in ['.zip', '.rar', '.7z', '.tar']:
            file_type = "📦 Aʀᴄʜɪᴠᴇ"
        else:
            file_type = "📁 Dᴏᴄᴜᴍᴇɴᴛ"
        
        return {
            "name": display_name[:30] + "..." if len(display_name) > 30 else display_name,
            "size": roxybot_zipmaker.roxybot_format_size(size),
            "type": file_type,
            "full_path": file_path
        }
    except:
        return {
            "name": os.path.basename(file_path),
            "size": "Unknown",
            "type": "📁 Fɪʟᴇ",
            "full_path": file_path
        }


@Client.on_message(filters.command("files") & filters.private)
async def roxybot_files_command(client: Client, message: Message):
    """Show list of queued files with management buttons"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /files")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if user has files
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        await message.reply_text(
            "<b>📁 Yᴏᴜʀ Fɪʟᴇ Qᴜᴇᴜᴇ</b>\n\n"
            "<blockquote>❌ Nᴏ ғɪʟᴇꜱ ɪɴ ǫᴜᴇᴜᴇ!\n\n"
            "Sᴇɴᴅ ᴍᴇ ꜱᴏᴍᴇ ғɪʟᴇꜱ ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ:\n"
            "• 📸 Pʜᴏᴛᴏꜱ\n"
            "• 🎥 Vɪᴅᴇᴏꜱ\n"
            "• 📄 Dᴏᴄᴜᴍᴇɴᴛꜱ\n"
            "• 🎵 Aᴜᴅɪᴏ ғɪʟᴇꜱ\n"
            "• 🎙 Vᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇꜱ</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    files = roxybot_user_files[user_id]
    file_count = len(files)
    
    # Calculate total size
    total_size = 0
    for f in files:
        if os.path.exists(f):
            total_size += os.path.getsize(f)
    
    # Build file list text
    text = f"<b>📁 Yᴏᴜʀ Fɪʟᴇ Qᴜᴇᴜᴇ</b>\n\n"
    text += f"<blockquote>📊 <b>Tᴏᴛᴀʟ Fɪʟᴇꜱ:</b> {file_count}\n"
    text += f"💾 <b>Tᴏᴛᴀʟ Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(total_size)}\n\n"
    
    # Show last 10 files (to avoid message being too long)
    display_files = files[-10:] if len(files) > 10 else files
    
    if len(files) > 10:
        text += f"*(Sʜᴏᴡɪɴɢ ʟᴀꜱᴛ 10 ᴏғ {file_count} ғɪʟᴇꜱ)*\n\n"
    
    for i, file_path in enumerate(display_files, 1):
        info = roxybot_get_file_info(file_path)
        text += f"{i}. {info['type']} `{info['name']}`\n"
        text += f"   💾 {info['size']}\n\n"
    
    text += "</blockquote>\n\n"
    text += "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    
    # Create inline buttons (removed password option - now in /create)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📦 Cʀᴇᴀᴛᴇ ZIP", callback_data="roxybot_quick_create")
        ],
        [
            InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Lᴀꜱᴛ", callback_data="roxybot_remove_last"),
            InlineKeyboardButton("🗑️ Cʟᴇᴀʀ Aʟʟ", callback_data="roxybot_clear_all")
        ],
        [
            InlineKeyboardButton("🔄 Rᴇғʀᴇꜱʜ", callback_data="roxybot_refresh_files")
        ]
    ])
    
    await message.reply_text(text, reply_markup=keyboard)
    logger.info(f"✅ Files list sent to user {user_id}")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Callback Handlers for file management buttons

@Client.on_callback_query(filters.regex("^roxybot_remove_last$"))
async def roxybot_remove_last_callback(client: Client, callback_query: CallbackQuery):
    """Remove the last file from queue"""
    user_id = callback_query.from_user.id
    
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        await callback_query.answer("❌ Nᴏ ғɪʟᴇꜱ ᴛᴏ ʀᴇᴍᴏᴠᴇ!", show_alert=True)
        return
    
    # Remove last file
    removed_file = roxybot_user_files[user_id].pop()
    
    # Delete the actual file
    try:
        if os.path.exists(removed_file):
            os.remove(removed_file)
    except:
        pass
    
    remaining = len(roxybot_user_files[user_id])
    
    await callback_query.answer(f"✅ Rᴇᴍᴏᴠᴇᴅ ʟᴀꜱᴛ ғɪʟᴇ! {remaining} ғɪʟᴇꜱ ʀᴇᴍᴀɪɴɪɴɢ.")
    
    # Update the message
    if remaining > 0:
        # Refresh the file list
        await roxybot_refresh_files_list(callback_query)
    else:
        await callback_query.message.edit_text(
            "<b>📁 Yᴏᴜʀ Fɪʟᴇ Qᴜᴇᴜᴇ</b>\n\n"
            "<blockquote>✅ Aʟʟ ғɪʟᴇꜱ ʀᴇᴍᴏᴠᴇᴅ!\n\n"
            "Sᴇɴᴅ ᴍᴇ ꜱᴏᴍᴇ ғɪʟᴇꜱ ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
    
    logger.info(f"✅ User {user_id} removed last file, {remaining} remaining")


@Client.on_callback_query(filters.regex("^roxybot_clear_all$"))
async def roxybot_clear_all_callback(client: Client, callback_query: CallbackQuery):
    """Show confirmation dialog before clearing all files"""
    user_id = callback_query.from_user.id
    
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        await callback_query.answer("❌ Nᴏ ғɪʟᴇꜱ ᴛᴏ ᴄʟᴇᴀʀ!", show_alert=True)
        return
    
    file_count = len(roxybot_user_files[user_id])
    
    # Show confirmation dialog
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Yᴇꜱ, Cʟᴇᴀʀ Aʟʟ", callback_data="roxybot_confirm_clear"),
            InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="roxybot_cancel_clear")
        ]
    ])
    
    await callback_query.answer("⚠️ Cᴏɴғɪʀᴍ ᴅᴇʟᴇᴛɪᴏɴ?")
    
    await callback_query.message.edit_text(
        f"<b>⚠️ Cᴏɴғɪʀᴍ Dᴇʟᴇᴛɪᴏɴ</b>\n\n"
        f"<blockquote>Yᴏᴜ ᴀʀᴇ ᴀʙᴏᴜᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ <b>{file_count}</b> ғɪʟᴇ(ꜱ).\n\n"
        f"Tʜɪꜱ ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ!</blockquote>\n\n"
        f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex("^roxybot_confirm_clear$"))
async def roxybot_confirm_clear_callback(client: Client, callback_query: CallbackQuery):
    """Actually clear all files after confirmation"""
    user_id = callback_query.from_user.id
    
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        await callback_query.answer("❌ Nᴏ ғɪʟᴇꜱ ᴛᴏ ᴄʟᴇᴀʀ!", show_alert=True)
        return
    
    # Delete all files
    file_count = len(roxybot_user_files[user_id])
    for file_path in roxybot_user_files[user_id]:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
    
    # Clear the list
    roxybot_user_files[user_id] = []
    
    await callback_query.answer(f"🗑️ Cʟᴇᴀʀᴇᴅ {file_count} ғɪʟᴇꜱ!")
    
    await callback_query.message.edit_text(
        "<b>📁 Yᴏᴜʀ Fɪʟᴇ Qᴜᴇᴜᴇ</b>\n\n"
        f"<blockquote>🗑️ Cʟᴇᴀʀᴇᴅ {file_count} ғɪʟᴇ(ꜱ)!\n\n"
        "Sᴇɴᴅ ᴍᴇ ꜱᴏᴍᴇ ғɪʟᴇꜱ ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ.</blockquote>\n\n"
        "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )
    
    logger.info(f"✅ User {user_id} cleared all {file_count} files")


@Client.on_callback_query(filters.regex("^roxybot_cancel_clear$"))
async def roxybot_cancel_clear_callback(client: Client, callback_query: CallbackQuery):
    """Cancel the clear all operation and go back"""
    await callback_query.answer("✅ Cᴀɴᴄᴇʟʟᴇᴅ!")
    # Refresh the file list
    await roxybot_refresh_files_list(callback_query)


@Client.on_callback_query(filters.regex("^roxybot_refresh_files$"))
async def roxybot_refresh_files_callback(client: Client, callback_query: CallbackQuery):
    """Refresh the files list"""
    await callback_query.answer("🔄 Rᴇғʀᴇꜱʜɪɴɢ...")
    await roxybot_refresh_files_list(callback_query)


async def roxybot_refresh_files_list(callback_query: CallbackQuery):
    """Helper function to refresh the files list message"""
    user_id = callback_query.from_user.id
    
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        await callback_query.message.edit_text(
            "<b>📁 Yᴏᴜʀ Fɪʟᴇ Qᴜᴇᴜᴇ</b>\n\n"
            "<blockquote>❌ Nᴏ ғɪʟᴇꜱ ɪɴ ǫᴜᴇᴜᴇ!\n\n"
            "Sᴇɴᴅ ᴍᴇ ꜱᴏᴍᴇ ғɪʟᴇꜱ ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    files = roxybot_user_files[user_id]
    file_count = len(files)
    
    # Calculate total size
    total_size = 0
    for f in files:
        if os.path.exists(f):
            total_size += os.path.getsize(f)
    
    # Build file list text
    text = f"<b>📁 Yᴏᴜʀ Fɪʟᴇ Qᴜᴇᴜᴇ</b>\n\n"
    text += f"<blockquote>📊 <b>Tᴏᴛᴀʟ Fɪʟᴇꜱ:</b> {file_count}\n"
    text += f"💾 <b>Tᴏᴛᴀʟ Sɪᴢᴇ:</b> {roxybot_zipmaker.roxybot_format_size(total_size)}\n\n"
    
    # Show last 10 files
    display_files = files[-10:] if len(files) > 10 else files
    
    if len(files) > 10:
        text += f"*(Sʜᴏᴡɪɴɢ ʟᴀꜱᴛ 10 ᴏғ {file_count} ғɪʟᴇꜱ)*\n\n"
    
    for i, file_path in enumerate(display_files, 1):
        info = roxybot_get_file_info(file_path)
        text += f"{i}. {info['type']} `{info['name']}`\n"
        text += f"   💾 {info['size']}\n\n"
    
    text += "</blockquote>\n\n"
    text += "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    
    # Create inline buttons
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📦 Cʀᴇᴀᴛᴇ ZIP", callback_data="roxybot_quick_create")
        ],
        [
            InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Lᴀꜱᴛ", callback_data="roxybot_remove_last"),
            InlineKeyboardButton("🗑️ Cʟᴇᴀʀ Aʟʟ", callback_data="roxybot_clear_all")
        ],
        [
            InlineKeyboardButton("🔄 Rᴇғʀᴇꜱʜ", callback_data="roxybot_refresh_files")
        ]
    ])
    
    await callback_query.message.edit_text(text, reply_markup=keyboard)


@Client.on_callback_query(filters.regex("^roxybot_quick_create$"))
async def roxybot_quick_create_callback(client: Client, callback_query: CallbackQuery):
    """Quick redirect to create command"""
    await callback_query.answer("💡 Uꜱᴇ /create ᴄᴏᴍᴍᴀɴᴅ!")
    await callback_query.message.reply_text(
        "<b>📦 Cʀᴇᴀᴛᴇ ZIP Aʀᴄʜɪᴠᴇ</b>\n\n"
        "<blockquote>Uꜱᴇ ᴛʜᴇ /create ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ:\n"
        "• Nᴀᴍᴇ ʏᴏᴜʀ ZIP ғɪʟᴇ\n"
        "• Aᴅᴅ ᴘᴀꜱꜱᴡᴏʀᴅ (ᴏᴘᴛɪᴏɴᴀʟ)\n"
        "• Cʜᴏᴏꜱᴇ ᴇɴᴄʀʏᴘᴛɪᴏɴ ᴛʏᴘᴇ</blockquote>\n\n"
        "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
