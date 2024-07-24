import os
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackContext, CommandHandler, MessageHandler, filters, Updater
from downloader import Downloader

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID')

async def music(update: Update, context: CallbackContext):

    if len(context.args) == 0:
        msg = 'Send a message in format "/music https://youtu.be/iik25wqIuFo"'
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=msg,
                    reply_to_message_id=update.effective_message.message_id,
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.HTML,
        )
        return

    music_src = context.args[0]
    try:
        dl = Downloader(music_src)
        await context.bot.send_audio(chat_id=update.effective_chat.id,
                                audio=open(dl.song, 'rb'),
                                performer=dl.author,
                                title=dl.title,
                                caption="@invisiblemusicbot")
        dl.delete_downloaded_file()
    except Exception as e:
        print('An error has occured', e)
        await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=str(e),
                    parse_mode=ParseMode.HTML,
        )

async def notify_owner(update: Update, context: CallbackContext, err: str):
    user_ref = update.effective_user.username or update.effective_user.full_name
    msg = f'User @{user_ref} has tried downloading music, but got an error:\n\n{err}'
    await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=msg,
            parse_mode=ParseMode.HTML,
    )

async def send_msg(update: Update, context: CallbackContext):
    music_src = update.effective_message.text
    print('HERE')
    try:
        dl = Downloader(music_src)
        await context.bot.send_audio(chat_id=update.effective_chat.id,
                                audio=open(dl.song, 'rb'),
                                performer=dl.author,
                                title=dl.title,
                                caption="@invisiblemusicbot")
    except Exception as e:
        if str(e) == "Invalid YouTube link":
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=
                    "Please, send a valid link to YouTube video",
                    parse_mode=ParseMode.HTML,
        ) 
        else:
            await notify_owner(update, context, str(e))
            await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=
                        "Sorry, an error has occured. Please, report the error to @INV1SBLE",
                        parse_mode=ParseMode.HTML,
            )


if __name__ == '__main__':
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("music", music))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE,send_msg))

    # Start the Bot
    print(f"Starting the bot...")
    application.run_polling()

