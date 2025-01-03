import yt_dlp
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Bot API Key
API_KEY = '7124918669:AAE-QrV_ClXNzA_Lc1Y5u-7B7LmykhBMUwA'

# yt-dlp options
async def download_song(update: Update, context: CallbackContext):
    # YouTube URL
    url = " ".join(context.args)
    
    if not url:
        await update.message.reply_text("You must provide a YouTube URL.")
        return
    
    # cookie.txt file and 320kbps MP3 options
    cookie_file = 'cookie.txt'
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'cookiefile': cookie_file,  # Use the cookie file
        'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',  # Save to the Downloads folder
    }

    # yt-dlp to download the song
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            audio_file = f'/storage/emulated/0/Download/{video_title}.mp3'
            
            # Send audio file via Telegram
            if os.path.exists(audio_file):
                await update.message.reply_text(f"Downloading and sending: {video_title}")
                await update.message.reply_audio(audio=open(audio_file, 'rb'))
                os.remove(audio_file)  # Delete the file after sending
            else:
                await update.message.reply_text("Error in downloading the song.")
        except yt_dlp.DownloadError as e:
            await update.message.reply_text(f"Download Error: {str(e)}")
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {str(e)}")

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Send a YouTube URL to download the song.")

# Main function to set up the bot
def main():
    application = Application.builder().token(API_KEY).build()

    # Adding command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("download", download_song))  # /download URL

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
