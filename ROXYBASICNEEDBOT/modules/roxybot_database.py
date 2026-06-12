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

from motor.motor_asyncio import AsyncIOMotorClient
from config import RoxyBotConfig

class RoxyBotDatabase:
    """MongoDB Database Handler for Roxy Zip Maker Bot"""
    
    def __init__(self):
        self.roxybot_client = None
        self.roxybot_db = None
        self.roxybot_users_collection = None
        
    async def roxybot_connect(self):
        """Connect to MongoDB"""
        try:
            self.roxybot_client = AsyncIOMotorClient(RoxyBotConfig.ROXYBOT_MONGODB_URI)
            self.roxybot_db = self.roxybot_client[RoxyBotConfig.ROXYBOT_DATABASE_NAME]
            self.roxybot_users_collection = self.roxybot_db['roxybot_users']
            print("✅ RoxyBot: Successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(f"❌ RoxyBot: MongoDB connection error: {e}")
            return False
    
    async def roxybot_add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add or update user in database"""
        try:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "zip_count": 0
            }
            await self.roxybot_users_collection.update_one(
                {"user_id": user_id},
                {"$setOnInsert": user_data},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ RoxyBot: Error adding user: {e}")
            return False
    
    # 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
    # MongoDB Handler - Storing user data and statistics
    
    async def roxybot_increment_zip_count(self, user_id: int):
        """Increment zip creation count for user"""
        try:
            await self.roxybot_users_collection.update_one(
                {"user_id": user_id},
                {"$inc": {"zip_count": 1}}
            )
            return True
        except Exception as e:
            print(f"❌ RoxyBot: Error incrementing zip count: {e}")
            return False
    
    async def roxybot_get_user_stats(self, user_id: int):
        """Get user statistics"""
        try:
            user = await self.roxybot_users_collection.find_one({"user_id": user_id})
            return user if user else None
        except Exception as e:
            print(f"❌ RoxyBot: Error getting user stats: {e}")
            return None
    
    async def roxybot_get_total_users(self):
        """Get total number of users"""
        try:
            count = await self.roxybot_users_collection.count_documents({})
            return count
        except Exception as e:
            print(f"❌ RoxyBot: Error getting total users: {e}")
            return 0
    
    async def roxybot_get_all_users(self):
        """Get all users from database (for broadcast)"""
        try:
            users = []
            cursor = self.roxybot_users_collection.find({})
            async for user in cursor:
                users.append(user)
            return users
        except Exception as e:
            print(f"❌ RoxyBot: Error getting all users: {e}")
            return []
    
    # 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
    # Thumbnail Management
    
    async def roxybot_set_thumbnail(self, user_id: int, file_id: str):
        """Set user's custom thumbnail file_id"""
        try:
            await self.roxybot_users_collection.update_one(
                {"user_id": user_id},
                {"$set": {"thumbnail_file_id": file_id}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ RoxyBot: Error setting thumbnail: {e}")
            return False
    
    async def roxybot_get_thumbnail(self, user_id: int):
        """Get user's custom thumbnail file_id"""
        try:
            user = await self.roxybot_users_collection.find_one({"user_id": user_id})
            if user and "thumbnail_file_id" in user:
                return user["thumbnail_file_id"]
            return None
        except Exception as e:
            print(f"❌ RoxyBot: Error getting thumbnail: {e}")
            return None
    
    async def roxybot_delete_thumbnail(self, user_id: int):
        """Delete user's custom thumbnail"""
        try:
            await self.roxybot_users_collection.update_one(
                {"user_id": user_id},
                {"$unset": {"thumbnail_file_id": ""}}
            )
            return True
        except Exception as e:
            print(f"❌ RoxyBot: Error deleting thumbnail: {e}")
            return False
    
    # 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
    # Ban/Unban User Management
    
    async def roxybot_ban_user(self, user_id: int, banned_by: int, reason: str = None):
        """Ban a user from using the bot"""
        try:
            await self.roxybot_users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "is_banned": True,
                        "banned_by": banned_by,
                        "ban_reason": reason
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ RoxyBot: Error banning user: {e}")
            return False
    
    async def roxybot_unban_user(self, user_id: int):
        """Unban a user"""
        try:
            await self.roxybot_users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {"is_banned": False},
                    "$unset": {"banned_by": "", "ban_reason": ""}
                }
            )
            return True
        except Exception as e:
            print(f"❌ RoxyBot: Error unbanning user: {e}")
            return False
    
    async def roxybot_is_banned(self, user_id: int):
        """Check if user is banned"""
        try:
            user = await self.roxybot_users_collection.find_one({"user_id": user_id})
            if user and user.get("is_banned", False):
                return True
            return False
        except Exception as e:
            print(f"❌ RoxyBot: Error checking ban status: {e}")
            return False
    
    async def roxybot_get_ban_info(self, user_id: int):
        """Get ban info including reason for a user"""
        try:
            user = await self.roxybot_users_collection.find_one({"user_id": user_id})
            if user and user.get("is_banned", False):
                return {
                    "is_banned": True,
                    "reason": user.get("ban_reason", "No reason provided"),
                    "banned_by": user.get("banned_by", None)
                }
            return {"is_banned": False, "reason": None, "banned_by": None}
        except Exception as e:
            print(f"❌ RoxyBot: Error getting ban info: {e}")
            return {"is_banned": False, "reason": None, "banned_by": None}

# Initialize database instance
roxybot_db = RoxyBotDatabase()

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
