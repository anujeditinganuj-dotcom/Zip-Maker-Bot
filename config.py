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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RoxyBotConfig:
    """Configuration class for Roxy Zip Maker Bot"""
    
    # Bot Configuration
    ROXYBOT_API_ID = int(os.environ.get("API_ID", "34446649"))
    ROXYBOT_API_HASH = os.environ.get("API_HASH", "8dc570c08d8e35e88fb9bfc73c65d7fa")
    ROXYBOT_BOT_TOKEN = os.environ.get("BOT_TOKEN", "8626274039:AAHwM-Xl_FZ6FI6C0Kju7gRY1Gz8CPllBU8")
    
    # MongoDB Configuration
    ROXYBOT_MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://Anujedit:Anujedit@cluster0.7cs2nhd.mongodb.net/?appName=Cluster0")
    ROXYBOT_DATABASE_NAME = os.environ.get("DATABASE_NAME", "Anujedit")
    
    # Flask Configuration
    ROXYBOT_FLASK_PORT = int(os.environ.get("PORT", "8080"))
    ROXYBOT_FLASK_HOST = os.environ.get("HOST", "0.0.0.0")
    
    # Bot Settings
    ROXYBOT_OWNER_ID = int(os.environ.get("OWNER_ID", "7892805795"))
    ROXYBOT_LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003951808679"))
    
    # Admin IDs (space or comma separated for multiple admins)
    @staticmethod
    def roxybot_get_admin_ids():
        """Get list of admin IDs from environment variable"""
        admin_str = os.environ.get("ADMIN_IDS", "7892805795")
        if not admin_str:
            # Fallback to OWNER_ID if ADMIN_IDS not set
            owner = os.environ.get("OWNER_ID", "7892805795")
            return [int(owner)] if owner != "7892805795" else []
        # Split by space or comma
        admin_str = admin_str.replace(",", "7892805795")
        return [int(x.strip()) for x in admin_str.split() if x.strip().isdigit()]
    
    # Force Subscribe Settings
    ROXYBOT_FORCE_SUB_ENABLED = os.environ.get("FORCE_SUB_ENABLED", "false").lower() == "true"
    
    @staticmethod
    def roxybot_get_force_sub_channels():
        """Get list of force subscribe channel IDs (max 3)"""
        channels_str = os.environ.get("FORCE_SUB_CHANNELS", "-1003951808679")
        if not channels_str:
            return []
        # Split by space or comma
        channels_str = channels_str.replace(",", "-1003951808679")
        channels = []
        for x in channels_str.split():
            x = x.strip()
            if x.lstrip("-").isdigit():
                channels.append(int(x))
        return channels[:3]  # Max 3 channels
    
    # File Settings
    ROXYBOT_DOWNLOAD_PATH = "downloads"
    ROXYBOT_ZIP_PATH = "zips"
    
    # Bot Info
    ROXYBOT_CREATOR = "@Anujedits76"
    ROXYBOT_VERSION = "1.0.0"
    
    @staticmethod
    def roxybot_validate_config():
        """Validate required configuration"""
        if not RoxyBotConfig.ROXYBOT_API_ID:
            raise ValueError("API_ID is required!")
        if not RoxyBotConfig.ROXYBOT_API_HASH:
            raise ValueError("API_HASH is required!")
        if not RoxyBotConfig.ROXYBOT_BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required!")
        if not RoxyBotConfig.ROXYBOT_MONGODB_URI:
            raise ValueError("MONGODB_URI is required!")
        return True

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
