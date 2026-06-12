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
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from ROXYBASICNEEDBOT.modules.roxybot_database import roxybot_db
from config import RoxyBotConfig
import logging

logger = logging.getLogger(__name__)

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Broadcast Module - Send message to all users (Admin Only)

def roxybot_is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
    return user_id in admin_ids


@Client.on_message(filters.command("cast") & filters.private)
async def roxybot_broadcast_command(client: Client, message: Message):
    """Broadcast message to all users - Admin Only"""
    user_id = message.from_user.id
    
    logger.info("=" * 50)
    logger.info(f"📨 COMMAND RECEIVED: /cast")
    logger.info(f"👤 User: {message.from_user.first_name} (@{message.from_user.username})")
    logger.info(f"🆔 User ID: {user_id}")
    logger.info("=" * 50)
    
    # Check if user is admin
    if not roxybot_is_admin(user_id):
        logger.warning(f"⚠️ Non-admin user {user_id} tried to use /cast")
        await message.reply_text(
            "❌ **Aᴄᴄᴇꜱꜱ Dᴇɴɪᴇᴅ!**\n\n"
            "Tʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴꜱ.\n\n"
            "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
        )
        return
    
    # Check if replying to a message
    if not message.reply_to_message:
        await message.reply_text(
            "📢 **Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴍᴀɴᴅ**\n\n"
            "**Uꜱᴀɢᴇ:** Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ /cast\n\n"
            "Tʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ꜱᴇɴᴛ ᴛᴏ ᴀʟʟ ʙᴏᴛ ᴜꜱᴇʀꜱ.\n\n"
            "**Sᴜᴘᴘᴏʀᴛᴇᴅ:** Tᴇxᴛ, Pʜᴏᴛᴏꜱ, Vɪᴅᴇᴏꜱ, Dᴏᴄᴜᴍᴇɴᴛꜱ, Aᴜᴅɪᴏ\n\n"
            "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
        )
        return
    
    # Get the message to broadcast
    broadcast_msg = message.reply_to_message
    
    # Get all users from database
    all_users = await roxybot_db.roxybot_get_all_users()
    
    if not all_users:
        await message.reply_text(
            "❌ **Nᴏ ᴜꜱᴇʀꜱ ғᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ!**\n\n"
            "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
        )
        return
    
    total_users = len(all_users)
    
    # Send status message
    status_msg = await message.reply_text(
        f"📢 **Sᴛᴀʀᴛɪɴɢ Bʀᴏᴀᴅᴄᴀꜱᴛ...**\n\n"
        f"👥 Tᴏᴛᴀʟ Uꜱᴇʀꜱ: {total_users}\n"
        f"⏳ Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...\n\n"
        f"⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
    )
    
    logger.info(f"📢 Starting broadcast to {total_users} users")
    
    # Broadcast statistics
    success_count = 0
    failed_count = 0
    blocked_count = 0
    deleted_count = 0
    
    for user in all_users:
        user_id_to_send = user.get("user_id")
        
        if not user_id_to_send:
            continue
        
        try:
            # Copy the message to user
            await broadcast_msg.copy(chat_id=user_id_to_send)
            success_count += 1
            
            # Small delay to avoid flood
            await asyncio.sleep(0.05)
            
        except FloodWait as e:
            logger.warning(f"⏳ FloodWait: Sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
            # Retry after flood wait
            try:
                await broadcast_msg.copy(chat_id=user_id_to_send)
                success_count += 1
            except:
                failed_count += 1
                
        except UserIsBlocked:
            blocked_count += 1
            logger.info(f"🚫 User {user_id_to_send} blocked the bot")
            
        except InputUserDeactivated:
            deleted_count += 1
            logger.info(f"💀 User {user_id_to_send} account deleted")
            
        except PeerIdInvalid:
            failed_count += 1
            logger.info(f"❌ Invalid peer ID: {user_id_to_send}")
            
        except Exception as e:
            failed_count += 1
            logger.error(f"❌ Failed to send to {user_id_to_send}: {e}")
        
        # Update status every 50 users
        if (success_count + failed_count + blocked_count + deleted_count) % 50 == 0:
            try:
                await status_msg.edit_text(
                    f"📢 **Bʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ...**\n\n"
                    f"✅ Sᴜᴄᴄᴇꜱꜱ: {success_count}\n"
                    f"❌ Fᴀɪʟᴇᴅ: {failed_count}\n"
                    f"🚫 Bʟᴏᴄᴋᴇᴅ: {blocked_count}\n"
                    f"💀 Dᴇʟᴇᴛᴇᴅ: {deleted_count}\n"
                    f"📊 Pʀᴏɢʀᴇꜱꜱ: {success_count + failed_count + blocked_count + deleted_count}/{total_users}\n\n"
                    f"⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
                )
            except:
                pass
    
    # Final status
    await status_msg.edit_text(
        f"<b>✅ Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴘʟᴇᴛᴇ!</b>\n\n"
        f"<blockquote>📊 <b>Sᴛᴀᴛɪꜱᴛɪᴄꜱ:</b>\n"
        f"├ ✅ Sᴜᴄᴄᴇꜱꜱ: {success_count}\n"
        f"├ ❌ Fᴀɪʟᴇᴅ: {failed_count}\n"
        f"├ 🚫 Bʟᴏᴄᴋᴇᴅ: {blocked_count}\n"
        f"├ 💀 Dᴇʟᴇᴛᴇᴅ: {deleted_count}\n"
        f"└ 👥 Tᴏᴛᴀʟ: {total_users}</blockquote>\n\n"
        f"<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )
    
    logger.info(f"✅ Broadcast complete: {success_count} success, {failed_count} failed, {blocked_count} blocked, {deleted_count} deleted")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
