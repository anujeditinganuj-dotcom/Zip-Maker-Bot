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

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChannelPrivate
from config import RoxyBotConfig
import logging

logger = logging.getLogger(__name__)

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Force Subscribe Module - Check if user is subscribed to required channels

async def roxybot_check_force_sub(client: Client, user_id: int) -> dict:
    """
    Check if user is subscribed to all required channels
    Returns: {"is_subscribed": bool, "not_joined": [list of channel info]}
    """
    if not RoxyBotConfig.ROXYBOT_FORCE_SUB_ENABLED:
        return {"is_subscribed": True, "not_joined": []}
    
    channels = RoxyBotConfig.roxybot_get_force_sub_channels()
    if not channels:
        return {"is_subscribed": True, "not_joined": []}
    
    not_joined = []
    
    for channel_id in channels:
        try:
            member = await client.get_chat_member(channel_id, user_id)
            if member.status in ["left", "kicked", "banned"]:
                # User not subscribed
                try:
                    chat = await client.get_chat(channel_id)
                    not_joined.append({
                        "id": channel_id,
                        "title": chat.title,
                        "username": chat.username,
                        "invite_link": chat.invite_link
                    })
                except:
                    not_joined.append({
                        "id": channel_id,
                        "title": f"Channel {channel_id}",
                        "username": None,
                        "invite_link": None
                    })
        except UserNotParticipant:
            # User not subscribed
            try:
                chat = await client.get_chat(channel_id)
                not_joined.append({
                    "id": channel_id,
                    "title": chat.title,
                    "username": chat.username,
                    "invite_link": chat.invite_link
                })
            except:
                not_joined.append({
                    "id": channel_id,
                    "title": f"Channel {channel_id}",
                    "username": None,
                    "invite_link": None
                })
        except ChatAdminRequired:
            logger.warning(f"⚠️ Bot is not admin in channel {channel_id}")
        except ChannelPrivate:
            logger.warning(f"⚠️ Channel {channel_id} is private or bot was kicked")
        except Exception as e:
            logger.error(f"❌ Error checking subscription for channel {channel_id}: {e}")
    
    return {
        "is_subscribed": len(not_joined) == 0,
        "not_joined": not_joined
    }


def roxybot_create_force_sub_buttons(not_joined: list) -> InlineKeyboardMarkup:
    """Create inline keyboard with join channel buttons"""
    buttons = []
    
    for channel in not_joined:
        if channel["username"]:
            url = f"https://t.me/{channel['username']}"
        elif channel["invite_link"]:
            url = channel["invite_link"]
        else:
            url = f"https://t.me/c/{str(channel['id']).replace('-100', '')}"
        
        buttons.append([
            InlineKeyboardButton(f"📢 Jᴏɪɴ {channel['title']}", url=url)
        ])
    
    # Add refresh button
    buttons.append([
        InlineKeyboardButton("✅ I'ᴠᴇ Jᴏɪɴᴇᴅ - Rᴇғʀᴇꜱʜ", callback_data="roxybot_check_sub")
    ])
    
    return InlineKeyboardMarkup(buttons)


async def roxybot_send_force_sub_message(message: Message, not_joined: list):
    """Send force subscribe message to user"""
    text = (
        "🔒 **Aᴄᴄᴇꜱꜱ Rᴇꜱᴛʀɪᴄᴛᴇᴅ!**\n\n"
        "<blockquote>Tᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ, ʏᴏᴜ ᴍᴜꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ(ꜱ) ғɪʀꜱᴛ:\n\n"
    )
    
    for i, channel in enumerate(not_joined, 1):
        text += f"{i}. **{channel['title']}**\n"
    
    text += (
        "</blockquote>\n\n"
        "<blockquote>👆 Cʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴊᴏɪɴ\n"
        "Tʜᴇɴ ᴄʟɪᴄᴋ **'I'ᴠᴇ Jᴏɪɴᴇᴅ - Rᴇғʀᴇꜱʜ'**</blockquote>\n\n"
        "<blockquote>⚡ Aɴᴜᴊ Kᴜᴍᴀʀ</blockquote>"
    )
    
    # Try to send with image if configured (uses URL from RoxyBotImages)
    try:
        from ROXYBASICNEEDBOT.modules.roxybot_images import RoxyBotImages
        forcesub_image = RoxyBotImages.get_forcesub_image()
        
        if forcesub_image:
            await message.reply_photo(
                photo=forcesub_image,
                caption=text,
                reply_markup=roxybot_create_force_sub_buttons(not_joined)
            )
        else:
            await message.reply_text(
                text=text,
                reply_markup=roxybot_create_force_sub_buttons(not_joined),
                disable_web_page_preview=True
            )
    except Exception as e:
        # Fallback to text only
        await message.reply_text(
            text=text,
            reply_markup=roxybot_create_force_sub_buttons(not_joined),
            disable_web_page_preview=True
        )


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Callback handler for refresh button

@Client.on_callback_query(filters.regex("^roxybot_check_sub$"))
async def roxybot_check_sub_callback(client: Client, callback_query: CallbackQuery):
    """Handle refresh subscription check"""
    user_id = callback_query.from_user.id
    
    logger.info(f"🔄 Checking subscription for user {user_id}")
    
    result = await roxybot_check_force_sub(client, user_id)
    
    if result["is_subscribed"]:
        await callback_query.message.edit_text(
            "✅ **Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Vᴇʀɪғɪᴇᴅ!**\n\n"
            "Yᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ.\n"
            "Sᴇɴᴅ /start ᴛᴏ ʙᴇɢɪɴ!\n\n"
            "⚡ **Aɴᴜᴊ Kᴜᴍᴀʀ**"
        )
        logger.info(f"✅ User {user_id} subscription verified")
    else:
        # Still not subscribed, update message
        await callback_query.answer(
            "❌ Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟꜱ ʏᴇᴛ!",
            show_alert=True
        )
        logger.info(f"❌ User {user_id} still not subscribed to all channels")


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Decorator function to check force subscribe

def roxybot_force_sub_check(func):
    """Decorator to check force subscription before command execution"""
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        
        # Skip check for admins
        admin_ids = RoxyBotConfig.roxybot_get_admin_ids()
        if user_id in admin_ids:
            return await func(client, message)
        
        # Check subscription
        result = await roxybot_check_force_sub(client, user_id)
        
        if not result["is_subscribed"]:
            await roxybot_send_force_sub_message(message, result["not_joined"])
            return
        
        return await func(client, message)
    
    return wrapper


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
