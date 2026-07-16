import os
import http.server
import socketserver
from threading import Thread
from telegram.ext import Application

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def run_render_port_buffer():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        httpd.serve_forever()

def main():
    Thread(target=run_render_port_buffer, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    
    print("Remote trigger application is online...")
    app.run_polling()

if __name__ == "__main__":
    main()
