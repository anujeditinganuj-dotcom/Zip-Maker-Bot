# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Test script to verify bot plugins are working

import asyncio
from pyrogram import Client
from config import RoxyBotConfig

async def test_bot():
    """Test bot connectivity and plugin loading"""
    
    print("🔍 Testing Roxy Zip Maker Bot...\n")
    
    # Validate config
    try:
        RoxyBotConfig.roxybot_validate_config()
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Create client
    app = Client(
        name="RoxyZipMakerBot",
        api_id=RoxyBotConfig.ROXYBOT_API_ID,
        api_hash=RoxyBotConfig.ROXYBOT_API_HASH,
        bot_token=RoxyBotConfig.ROXYBOT_BOT_TOKEN,
        plugins=dict(root="ROXYBASICNEEDBOT/plugins"),
        workdir="."
    )
    
    async with app:
        # Get bot info
        me = await app.get_me()
        print(f"✅ Bot Username: @{me.username}")
        print(f"✅ Bot ID: {me.id}")
        print(f"✅ Bot Name: {me.first_name}")
        
        # Check plugin handlers
        if hasattr(app, 'dispatcher'):
            print(f"\n📱 Total handlers registered: {len(app.dispatcher.groups)}")
        
        print("\n🎯 Bot is working! Now test these commands:")
        print("   1. Send /start to your bot")
        print("   2. Send /help")
        print("   3. Send a photo or video")
        print("\nIf bot doesn't respond:")
        print("   - Make sure BOT_TOKEN is correct")
        print("   - Check if bot is not already running elsewhere")
        print("   - Verify you're messaging the correct bot")

if __name__ == "__main__":
    asyncio.run(test_bot())

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
