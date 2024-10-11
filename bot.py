from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update: Update, context) -> None:
   await update.message.reply_text(f'Hello {update.effective_user.first_name}!')

if __name__ == '__main__':
   application = ApplicationBuilder().token('7617166979:AAH22S6YiW6jsYkTBttWGLc4bmuV2VGzIhw').build()
   application.add_handler(CommandHandler('start', start))
   application.run_polling()