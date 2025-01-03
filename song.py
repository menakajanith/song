import yt_dlp
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Bot API Key එක
API_KEY = '7124918669:AAE-QrV_ClXNzA_Lc1Y5u-7B7LmykhBMUwA'

# yt-dlp options
async def download_song(update: Update, context: CallbackContext):
    # YouTube URL එකක් ලබා ගන්න
    url = " ".join(context.args)
    
    if not url:
        await update.message.reply_text("You must provide a YouTube URL.")
        return
    
    # cookie.txt ගොනුව සහ 320kbps MP3 options
    cookie_file = 'cookie.txt'
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # FFmpegExtractAudio භාවිතා කිරීම
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # 320kbps MP3
        }],
        'cookiefile': cookie_file,  # cookie.txt ගොනුව භාවිතා කිරීම
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Downloads ෆෝල්ඩර් එකේ සින්දු
    }

    # yt-dlp එක මඟින් සින්දු බාගත කිරීම
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            audio_file = f'downloads/{video_title}.mp3'
            
            # Telegram එකට සින්දු ගොනුව එවීම
            if os.path.exists(audio_file):
                await update.message.reply_text(f"Downloading and sending: {video_title}")
                await update.message.reply_audio(audio=open(audio_file, 'rb'))
                os.remove(audio_file)  # After sending, remove the file
            else:
                await update.message.reply_text("Error in downloading the song.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

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
