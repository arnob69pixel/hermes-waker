import http.server
import socketserver
from threading import Thread
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Pre-built configuration
TOKEN = "8752464886:AAETK6veju3o3adaapyqyvxeD_92RHpLcJ0"
GITHUB_TOKEN = "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"
CODESPACE_NAME = "legendary-engine-4jxp4wjwrqvc7rg6"

async def wake_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Sending wake-up signal to your GitHub Codespace...")
    
    url = f"https://api.github.com/user/codespaces/{CODESPACE_NAME}/start"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers)
            if response.status_code in [200, 202]:
                await update.message.reply_text("🚀 Signal delivered! Codespace is booting up.")
            else:
                await update.message.reply_text(f"❌ Handshake failed: {response.text}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

def run_render_port_buffer():
    import os
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        httpd.serve_forever()

def main():
   app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("wake", wake_agent))
    print("Remote trigger application is online...")
    app.run_polling()

if __name__ == "__main__":
    main()
