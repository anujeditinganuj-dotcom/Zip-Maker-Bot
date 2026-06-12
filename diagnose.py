# Quick diagnostic to check why bot isn't responding
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 ROXY BOT DIAGNOSTICS")
print("=" * 60)

# Check environment variables
print("\n1. CHECKING ENVIRONMENT VARIABLES:")
print("-" * 60)

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
mongodb_uri = os.getenv('MONGODB_URI')

if api_id:
    print(f"✅ API_ID: {api_id}")
else:
    print("❌ API_ID: NOT SET")

if api_hash:
    print(f"✅ API_HASH: {api_hash[:10]}...")
else:
    print("❌ API_HASH: NOT SET")

if bot_token:
    # Show first and last part only
    parts = bot_token.split(':')
    if len(parts) == 2:
        print(f"✅ BOT_TOKEN: {parts[0]}:...{parts[1][-10:]}")
    else:
        print(f"⚠️ BOT_TOKEN: {bot_token[:20]}... (may be invalid format)")
else:
    print("❌ BOT_TOKEN: NOT SET")

if mongodb_uri:
    print(f"✅ MONGODB_URI: {'mongodb' in mongodb_uri.lower() and 'Connected' or 'Set'}")
else:
    print("⚠️ MONGODB_URI: NOT SET (optional)")

# Check pyrofork installation
print("\n2. CHECKING DEPENDENCIES:")
print("-" * 60)

try:
    import pyrogram
    print(f"✅ pyrogram/pyrofork installed: {pyrogram.__version__}")
except ImportError:
    print("❌ pyrogram/pyrofork: NOT INSTALLED")
    print("   Run: pip install pyrofork")

try:
    import TgCrypto
    print("✅ TgCrypto: installed")
except ImportError:
    print("❌ TgCrypto: NOT INSTALLED")
    print("   Run: pip install TgCrypto")

try:
    from motor import motor_asyncio
    print("✅ motor: installed")
except ImportError:
    print("⚠️ motor: NOT INSTALLED (optional for MongoDB)")

try:
    import flask
    print("✅ flask: installed")
except ImportError:
    print("⚠️ flask: NOT INSTALLED (optional for keep-alive)")

#Check folder structure
print("\n3. CHECKING FOLDER STRUCTURE:")
print("-" * 60)

import pathlib

folders_to_check = [
    "ROXYBASICNEEDBOT",
    "ROXYBASICNEEDBOT/plugins",
    "ROXYBASICNEEDBOT/modules",
]

files_to_check = [
    "bot.py",
    "config.py",
    "requirements.txt",
    ".env",
    "ROXYBASICNEEDBOT/__init__.py",
    "ROXYBASICNEEDBOT/plugins/__init__.py",
    "ROXYBASICNEEDBOT/plugins/roxybot_start.py",
    "ROXYBASICNEEDBOT/plugins/roxybot_filehandler.py",
    "ROXYBASICNEEDBOT/plugins/roxybot_zipcreator.py",
    "ROXYBASICNEEDBOT/plugins/roxybot_rename.py",
    "ROXYBASICNEEDBOT/modules/__init__.py",
    "ROXYBASICNEEDBOT/modules/roxybot_database.py",
    "ROXYBASICNEEDBOT/modules/roxybot_keepalive.py",
    "ROXYBASICNEEDBOT/modules/roxybot_zipmaker.py",
]

for folder in folders_to_check:
    if pathlib.Path(folder).exists():
        print(f"✅ {folder}/")
    else:
        print(f"❌ {folder}/ MISSING")

for file in files_to_check:
    if pathlib.Path(file).exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file} MISSING")

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)

if not bot_token:
    print("\n❌ CRITICAL: BOT_TOKEN is missing!")
    print("   1. Copy .env.example to .env")
    print("   2. Edit .env and add your bot token")
    print("   3. Get token from @BotFather on Telegram")
elif not api_id or not api_hash:
    print("\n❌ CRITICAL: API credentials missing!")
    print("   1. Go to https://my.telegram.org")
    print("   2. Get API_ID and API_HASH")
    print("   3. Add them to .env file")
else:
    print("\n✅ Configuration looks good!")
    print("\nNEXT STEPS:")
    print("1. Stop any running bot instances")
    print("2. Delete old session files:")
    print("   del *.session*")
    print("3. Run: python bot.py")
    print("4. Send /start to your bot")
    print("5. Watch the console for logs")

print("=" * 60)
