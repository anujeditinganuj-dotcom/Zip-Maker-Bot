# Clear webhook if it's blocking updates
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('BOT_TOKEN', "8626274039:AAHwM-Xl_FZ6FI6C0Kju7gRY1Gz8CPllBU8")

if bot_token:
    # Delete webhook
    url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    response = requests.get(url)
    print(f"Webhook delete response: {response.json()}")
    
    # Get updates method
    url2 = f"https://api.telegram.org/bot{bot_token}/getme"
    response2 = requests.get(url2)
    print(f"\nBot info: {response2.json()}")
    
    print("\n✅ Now restart your bot with: python bot.py")
else:
    print("❌ BOT_TOKEN not found in .env")
