import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("8198909852:AAEbbVLOBLiHJb8TcjPjJNcCHocUExzn44A")

# Basic AI chart analysis function
def analyze_chart(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 50, 150)

    # Dummy logic: find most intense horizontal/vertical lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=10)
    insight = "🔍 Analysis Summary:\n"

    if lines is not None and len(lines) > 0:
        insight += f"🟩 Detected {len(lines)} major lines (possible trendlines/S&R)\n"
        insight += f"📈 Trend Bias: {'Bullish' if np.mean(lines[:, :, 1]) < np.mean(lines[:, :, 3]) else 'Bearish'}\n"
        insight += f"⚠️ Consider price reaction around these levels for entry/exit.\n"
    else:
        insight += "No major lines detected. Image may lack structure or contrast."

    return insight

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Scalptron AI™\n\nSend me a chart image and I’ll give you trade insights!")

# Image handler
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    image_path = f"/tmp/chart_{update.message.from_user.id}.jpg"
    await photo_file.download_to_drive(image_path)

    await update.message.reply_text("📥 Chart received. Analyzing...")

    # AI chart analysis
    insights = analyze_chart(image_path)
    await update.message.reply_text(insights)

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
