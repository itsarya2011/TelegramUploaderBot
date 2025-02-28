import os
import requests
from pyrogram import Client, filters

# Bot Credentials (Taken from Render Environment Variables)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("file_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Send me a direct download link, and I'll upload it to Telegram.")

@app.on_message(filters.text)
def download_and_upload(client, message):
    url = message.text.strip()

    if not url.startswith("http"):
        message.reply_text("❌ Invalid link! Please send a valid direct download link.")
        return

    try:
        filename = url.split("/")[-1]  # Get filename from URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the link is valid

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        message.reply_text(f"✅ Downloaded: {filename}. Uploading to Telegram...")

        client.send_document(message.chat.id, filename)

        os.remove(filename)  # Delete the file after upload

    except Exception as e:
        message.reply_text(f"❌ Error: {str(e)}")

app.run()
