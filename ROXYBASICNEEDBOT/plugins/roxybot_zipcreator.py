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
from ROXYBASICNEEDBOT.modules.roxybot_zipmaker import roxybot_zipmaker, EncryptionType
from ROXYBASICNEEDBOT.modules.roxybot_tarmaker import roxybot_tarmaker
from ROXYBASICNEEDBOT.modules.roxybot_7zmaker import roxybot_7zmaker
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
from ROXYBASICNEEDBOT.plugins.roxybot_filehandler import roxybot_user_files
from config import RoxyBotConfig
import logging

logger = logging.getLogger(__name__)

# Helper function to get user thumbnail
async def roxybot_get_thumb(client, user_id: int) -> str:
    """Get user's custom thumbnail or fall back to default"""
    try:
        thumb_file_id = await roxybot_db.roxybot_get_thumbnail(user_id)
        if thumb_file_id:
            thumb_path = await client.download_media(
                thumb_file_id,
                file_name=f"downloads/thumb_{user_id}.jpg"
            )
            if thumb_path:
                return thumb_path
    except Exception as e:
        logger.error(f"Error getting user thumbnail: {e}")
    
    if os.path.exists("thumbnail.jpg"):
        return "thumbnail.jpg"
    return None

# Store user states
# Flow: select_format -> waiting_name -> waiting_password_choice -> waiting_encryption -> waiting_password -> creating
roxybot_user_states = {}
roxybot_user_zips = {}

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Create Command Handler - New Flow
# Step 1: Select Format -> Step 2: Enter Name -> Step 3: Password (if supported) -> Create

@Client.on_message(filters.command("create") & filters.private)
async def roxybot_create_command(client: Client, message: Message):
    """Create archive - Step 1: Select Format"""
    user_id = message.from_user.id
    
    # Check if user is banned
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    if user_id not in admin_ids:
        is_banned = await roxybot_db.roxybot_is_banned(user_id)
        if is_banned:
            return
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /create")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if user has files
    if user_id not in roxybot_user_files or not roxybot_user_files[user_id]:
        await message.reply_text(
            "❌ **Nᴏ ғɪʟᴇꜱ ғᴏᴜɴᴅ!**\n\n"
            "<blockquote>Pʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴍᴇ ꜱᴏᴍᴇ ғɪʟᴇꜱ ғɪʀꜱᴛ (ᴘʜᴏᴛᴏꜱ/ᴠɪᴅᴇᴏꜱ/ᴅᴏᴄᴜᴍᴇɴᴛꜱ)</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    file_count = len(roxybot_user_files[user_id])
    total_size = sum(os.path.getsize(f) for f in roxybot_user_files[user_id] if os.path.exists(f))
    size_str = roxybot_zipmaker.roxybot_format_size(total_size)
    
    # Store initial state
    roxybot_user_states[user_id] = {
        "state": "select_format",
        "files": roxybot_user_files[user_id].copy()
    }
    
    # Check if 7z is available
    sz_available = roxybot_7zmaker.is_available()
    
    # Create format selection buttons
    buttons = [
        [
            InlineKeyboardButton("📦 ZIP", callback_data="roxybot_fmt_zip"),
            InlineKeyboardButton("📚 TAR.GZ", callback_data="roxybot_fmt_tar")
        ]
    ]
    
    if sz_available:
        buttons.append([
            InlineKeyboardButton("🗜️ 7z", callback_data="roxybot_fmt_7z")
        ])
    
    buttons.append([
        InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="roxybot_fmt_cancel")
    ])
    
    keyboard = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(
        f"<b>📦 Cʀᴇᴀᴛᴇ Aʀᴄʜɪᴠᴇ</b>\n\n"
        f"<blockquote>📁 <b>Fɪʟᴇꜱ:</b> {file_count}\n"
        f"💾 <b>Tᴏᴛᴀʟ Sɪᴢᴇ:</b> {size_str}</blockquote>\n\n"
        f"<b>🗂️ Sᴛᴇᴘ 1:</b> Sᴇʟᴇᴄᴛ Aʀᴄʜɪᴠᴇ Fᴏʀᴍᴀᴛ\n\n"
        f"<blockquote>• <b>ZIP</b> - Sᴛᴀɴᴅᴀʀᴅ, ᴜɴɪᴠᴇʀꜱᴀʟ\n"
        f"• <b>TAR.GZ</b> - Bᴇꜱᴛ ғᴏʀ Lɪɴᴜx\n"
        f"• <b>7z</b> - Bᴇꜱᴛ ᴄᴏᴍᴘʀᴇꜱꜱɪᴏɴ</blockquote>\n\n"
        f"<blockquote>⚡ RᴏxʏBᴀꜱɪᴄNᴇᴇᴅBᴏᴛ</blockquote>",
        reply_markup=keyboard
    )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Format Selection Callbacks

@Client.on_callback_query(filters.regex("^roxybot_fmt_"))
async def roxybot_format_callback(client: Client, callback_query: CallbackQuery):
    """Handle format selection - Step 1"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "roxybot_fmt_cancel":
        if user_id in roxybot_user_states:
            del roxybot_user_states[user_id]
        await callback_query.answer("❌ Cᴀɴᴄᴇʟʟᴇᴅ!")
        await callback_query.message.edit_text(
            "❌ **Oᴘᴇʀᴀᴛɪᴏɴ Cᴀɴᴄᴇʟʟᴇᴅ**\n\n"
            "<blockquote>Uꜱᴇ /create ᴛᴏ ꜱᴛᴀʀᴛ ᴀɢᴀɪɴ.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    if user_id not in roxybot_user_states:
        await callback_query.answer("❌ Sᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ! Uꜱᴇ /create ᴀɢᴀɪɴ.", show_alert=True)
        return
    
    # Determine format
    if data == "roxybot_fmt_zip":
        roxybot_user_states[user_id]["format"] = "zip"
        format_name = "ZIP"
        supports_password = True
    elif data == "roxybot_fmt_tar":
        roxybot_user_states[user_id]["format"] = "tar"
        format_name = "TAR.GZ"
        supports_password = False
    elif data == "roxybot_fmt_7z":
        roxybot_user_states[user_id]["format"] = "7z"
        format_name = "7z"
        supports_password = True
    else:
        return
    
    roxybot_user_states[user_id]["supports_password"] = supports_password
    roxybot_user_states[user_id]["state"] = "waiting_name"
    file_count = len(roxybot_user_states[user_id].get("files", []))
    
    await callback_query.answer(f"📦 {format_name} ꜱᴇʟᴇᴄᴛᴇᴅ!")
    
    await callback_query.message.edit_text(
        f"<blockquote>📦 <b>Fᴏʀᴍᴀᴛ:</b> {format_name}\n"
        f"📁 <b>Fɪʟᴇꜱ:</b> {file_count}</blockquote>\n\n"
        f"<b>📝 Sᴛᴇᴘ 2:</b> Eɴᴛᴇʀ ᴀ ɴᴀᴍᴇ ғᴏʀ ʏᴏᴜʀ ᴀʀᴄʜɪᴠᴇ\n\n"
        f"<blockquote>💡 Dᴏɴ'ᴛ ɪɴᴄʟᴜᴅᴇ ᴇxᴛᴇɴꜱɪᴏɴ\n"
        f"Exᴀᴍᴘʟᴇ: <code>MyFiles</code> ᴏʀ <code>Backup_2024</code></blockquote>\n\n"
        f"Uꜱᴇ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ\n\n"
        f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Text Input Handler

@Client.on_message(filters.text & filters.private & ~filters.command(["start", "help", "stats", "create", "cancel", "files", "cast", "ban", "unban"]), group=1)
async def roxybot_handle_text_input(client: Client, message: Message):
    """Handle text input based on current state"""
    user_id = message.from_user.id
    
    if user_id not in roxybot_user_states:
        return
    
    state = roxybot_user_states[user_id].get("state")
    
    # Step 2: Handle name input
    if state == "waiting_name":
        await roxybot_handle_name_input(client, message)
        return
    
    # Step 3: Handle password input
    if state == "waiting_password":
        await roxybot_handle_password_input(client, message)
        return


async def roxybot_handle_name_input(client: Client, message: Message):
    """Handle archive name input - Step 2"""
    user_id = message.from_user.id
    
    # Sanitize name
    archive_name = message.text.strip()
    archive_name = "".join(c for c in archive_name if c.isalnum() or c in (' ', '-', '_'))
    
    if not archive_name:
        await message.reply_text(
            "❌ **Iɴᴠᴀʟɪᴅ ɴᴀᴍᴇ!**\n\n"
            "<blockquote>Pʟᴇᴀꜱᴇ ᴜꜱᴇ ᴀʟᴘʜᴀɴᴜᴍᴇʀɪᴄ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ ᴏɴʟʏ.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    roxybot_user_states[user_id]["name"] = archive_name
    format_type = roxybot_user_states[user_id].get("format", "zip")
    format_name = {"zip": "ZIP", "tar": "TAR.GZ", "7z": "7z"}.get(format_type, "ZIP")
    file_count = len(roxybot_user_states[user_id].get("files", []))
    
    # Check if format supports password
    if roxybot_user_states[user_id].get("supports_password"):
        roxybot_user_states[user_id]["state"] = "waiting_password_choice"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔐 Aᴅᴅ Pᴀꜱꜱᴡᴏʀᴅ", callback_data="roxybot_pwd_yes")
            ],
            [
                InlineKeyboardButton("⏭️ Sᴋɪᴘ (Nᴏ Pᴀꜱꜱᴡᴏʀᴅ)", callback_data="roxybot_pwd_no")
            ],
            [
                InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="roxybot_pwd_cancel")
            ]
        ])
        
        await message.reply_text(
            f"<blockquote>📦 <b>Fᴏʀᴍᴀᴛ:</b> {format_name}\n"
            f"📝 <b>Nᴀᴍᴇ:</b> <code>{archive_name}</code>\n"
            f"📁 <b>Fɪʟᴇꜱ:</b> {file_count}</blockquote>\n\n"
            f"<b>🔐 Sᴛᴇᴘ 3:</b> Aᴅᴅ ᴘᴀꜱꜱᴡᴏʀᴅ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ?\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
            reply_markup=keyboard
        )
    else:
        # TAR doesn't support password, create directly
        await roxybot_create_final_archive(client, message, user_id)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Password Callbacks

@Client.on_callback_query(filters.regex("^roxybot_pwd_"))
async def roxybot_password_callback(client: Client, callback_query: CallbackQuery):
    """Handle password choice - Step 3"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "roxybot_pwd_cancel":
        if user_id in roxybot_user_states:
            del roxybot_user_states[user_id]
        await callback_query.answer("❌ Cᴀɴᴄᴇʟʟᴇᴅ!")
        await callback_query.message.edit_text(
            "❌ **Oᴘᴇʀᴀᴛɪᴏɴ Cᴀɴᴄᴇʟʟᴇᴅ**\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    if user_id not in roxybot_user_states:
        await callback_query.answer("❌ Sᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ!", show_alert=True)
        return
    
    if data == "roxybot_pwd_no":
        # Create without password
        await callback_query.answer("⏭️ Cʀᴇᴀᴛɪɴɢ ᴡɪᴛʜᴏᴜᴛ ᴘᴀꜱꜱᴡᴏʀᴅ...")
        await callback_query.message.edit_text(
            "📦 **Cʀᴇᴀᴛɪɴɢ ᴀʀᴄʜɪᴠᴇ...**\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        await roxybot_create_final_archive(client, callback_query.message, user_id)
    
    elif data == "roxybot_pwd_yes":
        # Show encryption selection for ZIP, or go to password for 7z
        format_type = roxybot_user_states[user_id].get("format", "zip")
        
        if format_type == "zip":
            # Show encryption options for ZIP
            roxybot_user_states[user_id]["state"] = "waiting_encryption"
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔒 AES-256 (Mᴏꜱᴛ Sᴇᴄᴜʀᴇ)", callback_data="roxybot_enc_aes256")
                ],
                [
                    InlineKeyboardButton("🔐 AES-128 (Fᴀꜱᴛ)", callback_data="roxybot_enc_aes128")
                ],
                [
                    InlineKeyboardButton("🔑 ZɪᴘCʀʏᴘᴛᴏ (Cᴏᴍᴘᴀᴛɪʙʟᴇ)", callback_data="roxybot_enc_zipcrypto")
                ],
                [
                    InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data="roxybot_enc_cancel")
                ]
            ])
            
            await callback_query.answer("🔒 Sᴇʟᴇᴄᴛ ᴇɴᴄʀʏᴘᴛɪᴏɴ!")
            await callback_query.message.edit_text(
                "<b>🔒 Sᴇʟᴇᴄᴛ Eɴᴄʀʏᴘᴛɪᴏɴ Tʏᴘᴇ:</b>\n\n"
                "<blockquote>• <b>AES-256</b> - Sᴛʀᴏɴɢᴇꜱᴛ ꜱᴇᴄᴜʀɪᴛʏ\n"
                "• <b>AES-128</b> - Fᴀꜱᴛ & ꜱᴇᴄᴜʀᴇ\n"
                "• <b>ZɪᴘCʀʏᴘᴛᴏ</b> - Wᴏʀᴋꜱ ᴡɪᴛʜ ᴀʟʟ ZIP ᴛᴏᴏʟꜱ</blockquote>\n\n"
                "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>",
                reply_markup=keyboard
            )
        else:
            # 7z - go directly to password
            roxybot_user_states[user_id]["state"] = "waiting_password"
            await callback_query.answer("🔐 Eɴᴛᴇʀ ᴘᴀꜱꜱᴡᴏʀᴅ!")
            await callback_query.message.edit_text(
                "<b>🔐 Eɴᴛᴇʀ ʏᴏᴜʀ ᴘᴀꜱꜱᴡᴏʀᴅ:</b>\n\n"
                "<blockquote>• Mɪɴɪᴍᴜᴍ 4 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ\n"
                "• Uꜱᴇ ᴀ ꜱᴛʀᴏɴɢ ᴘᴀꜱꜱᴡᴏʀᴅ!</blockquote>\n\n"
                "Uꜱᴇ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ\n\n"
                "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
            )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Encryption Selection Callbacks

@Client.on_callback_query(filters.regex("^roxybot_enc_"))
async def roxybot_encryption_callback(client: Client, callback_query: CallbackQuery):
    """Handle encryption selection for ZIP"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    if data == "roxybot_enc_cancel":
        if user_id in roxybot_user_states:
            del roxybot_user_states[user_id]
        await callback_query.answer("❌ Cᴀɴᴄᴇʟʟᴇᴅ!")
        await callback_query.message.edit_text(
            "❌ **Oᴘᴇʀᴀᴛɪᴏɴ Cᴀɴᴄᴇʟʟᴇᴅ**\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    if user_id not in roxybot_user_states:
        await callback_query.answer("❌ Sᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ!", show_alert=True)
        return
    
    # Set encryption type
    if data == "roxybot_enc_aes256":
        roxybot_user_states[user_id]["encryption"] = EncryptionType.AES_256
        enc_name = "AES-256"
    elif data == "roxybot_enc_aes128":
        roxybot_user_states[user_id]["encryption"] = EncryptionType.AES_128
        enc_name = "AES-128"
    elif data == "roxybot_enc_zipcrypto":
        roxybot_user_states[user_id]["encryption"] = EncryptionType.ZIPCRYPTO
        enc_name = "ZɪᴘCʀʏᴘᴛᴏ"
    else:
        return
    
    roxybot_user_states[user_id]["state"] = "waiting_password"
    
    await callback_query.answer(f"🔒 {enc_name} ꜱᴇʟᴇᴄᴛᴇᴅ!")
    await callback_query.message.edit_text(
        f"<blockquote>🔒 <b>Eɴᴄʀʏᴘᴛɪᴏɴ:</b> {enc_name}</blockquote>\n\n"
        "<b>🔐 Eɴᴛᴇʀ ʏᴏᴜʀ ᴘᴀꜱꜱᴡᴏʀᴅ:</b>\n\n"
        "<blockquote>• Mɪɴɪᴍᴜᴍ 4 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ\n"
        "• Uꜱᴇ ᴀ ꜱᴛʀᴏɴɢ ᴘᴀꜱꜱᴡᴏʀᴅ!</blockquote>\n\n"
        "Uꜱᴇ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ\n\n"
        "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )


async def roxybot_handle_password_input(client: Client, message: Message):
    """Handle password input"""
    user_id = message.from_user.id
    password = message.text.strip()
    
    if len(password) < 4:
        await message.reply_text(
            "❌ **Pᴀꜱꜱᴡᴏʀᴅ ᴛᴏᴏ ꜱʜᴏʀᴛ!**\n\n"
            "<blockquote>Pᴀꜱꜱᴡᴏʀᴅ ᴍᴜꜱᴛ ʙᴇ ᴀᴛ ʟᴇᴀꜱᴛ 4 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ.</blockquote>\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        return
    
    roxybot_user_states[user_id]["password"] = password
    await roxybot_create_final_archive(client, message, user_id)


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Final Archive Creation

async def roxybot_create_final_archive(client: Client, message: Message, user_id: int):
    """Create the final archive"""
    
    if user_id not in roxybot_user_states:
        return
    
    state_data = roxybot_user_states[user_id]
    files = state_data.get("files", [])
    archive_name = state_data.get("name", "Archive")
    archive_format = state_data.get("format", "zip")
    password = state_data.get("password", None)
    encryption = state_data.get("encryption", EncryptionType.AES_256)
    
    # Clear state
    del roxybot_user_states[user_id]
    
    format_display = {"zip": "ZIP", "tar": "TAR.GZ", "7z": "7z"}.get(archive_format, "ZIP")
    ext = {"zip": ".zip", "tar": ".tar.gz", "7z": ".7z"}.get(archive_format, ".zip")
    
    status_msg = await message.reply_text(
        f"📦 **Cʀᴇᴀᴛɪɴɢ {format_display} Aʀᴄʜɪᴠᴇ...**\n\n"
        f"<blockquote>📝 Nᴀᴍᴇ: <code>{archive_name}{ext}</code>\n"
        f"📁 Fɪʟᴇꜱ: {len(files)}\n"
        f"🔐 Eɴᴄʀʏᴘᴛᴇᴅ: {'Yᴇꜱ' if password else 'Nᴏ'}</blockquote>\n\n"
        f"⏳ Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...\n\n"
        f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )
    
    try:
        # Create archive based on format
        if archive_format == "zip":
            if password:
                archive_path = await roxybot_zipmaker.roxybot_create_zip(
                    files, archive_name, password, encryption
                )
            else:
                archive_path = await roxybot_zipmaker.roxybot_create_zip(
                    files, archive_name, None, EncryptionType.NONE
                )
        
        elif archive_format == "tar":
            archive_path = await roxybot_tarmaker.roxybot_create_tar(
                files, archive_name, compress=True
            )
        
        elif archive_format == "7z":
            archive_path = await roxybot_7zmaker.roxybot_create_7z(
                files, archive_name, password
            )
        
        # Get size
        archive_size = os.path.getsize(archive_path)
        size_str = roxybot_zipmaker.roxybot_format_size(archive_size)
        
        await status_msg.edit_text(
            f"📤 **Uᴘʟᴏᴀᴅɪɴɢ {format_display}...**\n\n"
            f"<blockquote>📊 Sɪᴢᴇ: {size_str}</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        
        # Get thumbnail
        thumb_path = await roxybot_get_thumb(client, user_id)
        
        # Build caption
        if password:
            caption = (
                f"🔐 **Eɴᴄʀʏᴘᴛᴇᴅ {format_display} Cʀᴇᴀᴛᴇᴅ!**\n\n"
                f"<blockquote>📝 <b>Nᴀᴍᴇ:</b> <code>{archive_name}{ext}</code>\n"
                f"📦 <b>Fɪʟᴇꜱ:</b> {len(files)}\n"
                f"📊 <b>Sɪᴢᴇ:</b> {size_str}</blockquote>\n\n"
                f"<blockquote>⚠️ <b>Pᴀꜱꜱᴡᴏʀᴅ ᴘʀᴏᴛᴇᴄᴛᴇᴅ!</b>\n"
                f"Kᴇᴇᴘ ʏᴏᴜʀ ᴘᴀꜱꜱᴡᴏʀᴅ ꜱᴀғᴇ!</blockquote>\n\n"
                f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
            )
        else:
            caption = (
                f"✅ **{format_display} Cʀᴇᴀᴛᴇᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!**\n\n"
                f"<blockquote>📝 <b>Nᴀᴍᴇ:</b> <code>{archive_name}{ext}</code>\n"
                f"📦 <b>Fɪʟᴇꜱ:</b> {len(files)}\n"
                f"📊 <b>Sɪᴢᴇ:</b> {size_str}</blockquote>\n\n"
                f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
            )
        
        # Upload
        await message.reply_document(
            document=archive_path,
            thumb=thumb_path,
            caption=caption
        )
        
        # Send success sticker
        try:
            from ROXYBASICNEEDBOT.modules.roxybot_images import RoxyBotImages
            sticker = RoxyBotImages.get_zip_success_sticker()
            if sticker:
                await message.reply_sticker(sticker=sticker)
        except:
            pass
        
        # Update stats
        await roxybot_db.roxybot_increment_zip_count(user_id)
        
        # Cleanup
        roxybot_zipmaker.roxybot_cleanup_files(files)
        if user_id in roxybot_user_files:
            roxybot_user_files[user_id] = []
        
        await status_msg.delete()
        
        logger.info(f"✅ Archive created for user {user_id}: {archive_name}{ext}")
        
    except Exception as e:
        logger.error(f"❌ Archive creation error: {e}", exc_info=True)
        await status_msg.edit_text(
            f"❌ **Eʀʀᴏʀ:** {str(e)}\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
        if user_id in roxybot_user_states:
            del roxybot_user_states[user_id]


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Cancel Command

@Client.on_message(filters.command("cancel") & filters.private)
async def roxybot_cancel_command(client: Client, message: Message):
    """Cancel current operation"""
    user_id = message.from_user.id
    
    cancelled_something = False
    
    if user_id in roxybot_user_states:
        del roxybot_user_states[user_id]
        cancelled_something = True
    
    if user_id in roxybot_user_files and roxybot_user_files[user_id]:
        roxybot_zipmaker.roxybot_cleanup_files(roxybot_user_files[user_id])
        file_count = len(roxybot_user_files[user_id])
        roxybot_user_files[user_id] = []
        cancelled_something = True
        
        await message.reply_text(
            f"✅ **Oᴘᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ!**\n\n"
            f"<blockquote>🗑️ Cʟᴇᴀʀᴇᴅ {file_count} ғɪʟᴇ(ꜱ)</blockquote>\n\n"
            f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
    elif cancelled_something:
        await message.reply_text(
            "✅ **Oᴘᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ!**\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )
    else:
        await message.reply_text(
            "ℹ️ **Nᴏ ᴀᴄᴛɪᴠᴇ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴛᴏ ᴄᴀɴᴄᴇʟ**\n\n"
            "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
        )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
