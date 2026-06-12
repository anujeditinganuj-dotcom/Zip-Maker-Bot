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

from flask import Flask
from werkzeug.serving import run_simple
import threading
from config import RoxyBotConfig

# Initialize Flask app
roxybot_flask_app = Flask(__name__)

@roxybot_flask_app.route('/')
def roxybot_home():
    """Home route for keep-alive"""
    return f"""
    <html>
        <head>
            <title>Ak Zip Maker Bot</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .container {{
                    text-align: center;
                    padding: 40px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }}
                h1 {{ margin: 0; font-size: 3em; }}
                p {{ font-size: 1.2em; }}
                a {{ color: #fff; text-decoration: none; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Ak Zip Maker Bot</h1>
                <p>✅ Bot is running successfully!</p>
                <p>Created by <strong>RoxyBasicNeedBot</strong> ⚡</p>
                <p>Version: {RoxyBotConfig.ROXYBOT_VERSION}</p>
                <hr>
                <p>
                    <a href="https://t.me/anujedits76" target="_blank">📱 Telegram</a> | 
                    <a href="https://roxybasicneedbot.unaux.com/?i=1" target="_blank">🌐 Website</a> | 
                    <a href="https://www.youtube.com/@roxybasicneedbot" target="_blank">📺 YouTube</a>
                </p>
            </div>
        </body>
    </html>
    """

@roxybot_flask_app.route('/health')
def roxybot_health():
    """Health check endpoint"""
    return {"status": "healthy", "bot": "RoxyZipMakerBot", "version": RoxyBotConfig.ROXYBOT_VERSION}

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Flask Keep-Alive Server for Render Deployment

def roxybot_run_flask():
    """Run Flask server in a separate thread"""
    try:
        print(f"🌐 RoxyBot: Starting Flask server on {RoxyBotConfig.ROXYBOT_FLASK_HOST}:{RoxyBotConfig.ROXYBOT_FLASK_PORT}")
        run_simple(
            RoxyBotConfig.ROXYBOT_FLASK_HOST,
            RoxyBotConfig.ROXYBOT_FLASK_PORT,
            roxybot_flask_app,
            use_reloader=False,
            use_debugger=False
        )
    except Exception as e:
        print(f"❌ RoxyBot: Flask server error: {e}")

def roxybot_start_server():
    """Start Flask server in background thread"""
    flask_thread = threading.Thread(target=roxybot_run_flask, daemon=True)
    flask_thread.start()
    print("✅ RoxyBot: Flask keep-alive server started!")

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
