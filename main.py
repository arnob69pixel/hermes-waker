import os
import http.server
import socketserver
from threading import Thread
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
CODESPACE_NAME = os.environ.get("CODESPACE_NAME")

async def wake_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Sending wake-up signal to your GitHub Codespace...")
    
    url = f"https://api.github.com/user/codespaces/{CODESPACE_NAME}/start"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        response = requests.post(url, headers=headers)
        if response.status_code in [200, 202]:
            await update.message.reply_text("🚀 Signal delivered! Codespace is booting up.")
        else:
            await update.message.reply_text(f"❌ Handshake failed: {response.text}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def run_render_port_buffer():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        httpd.serve_forever()

def main():
    Thread(target=run_render_port_buffer, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("wake", wake_agent))
    print("Remote trigger application is online...")
    app.run_polling()

if __name__ == "__main__":
    main()
