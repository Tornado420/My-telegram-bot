import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# OpenAI API Key
openai.api_key = "your-openai-api-key"

# Telegram Bot Token
BOT_TOKEN = "your-telegram-bot-token"

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Function to generate images
async def generate_image(prompt: str):
    try:
        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        return response["data"][0]["url"]
    except Exception as e:
        return str(e)

# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a text prompt, and I'll generate an image for you.")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("Generating image... This may take a moment.")
    
    image_url = await generate_image(prompt)
    if image_url.startswith("http"):
        await update.message.reply_photo(image_url)
    else:
        await update.message.reply_text(f"Error: {image_url}")

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()