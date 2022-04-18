import os
from telegram import Message
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
from telegram.parsemode import ParseMode
from downloader import Downloader

API_TOKEN = os.environ['TELEGRAM_TOKEN']
OWNER_CHAT_ID = os.environ['OWNER_CHAT_ID']

updater = Updater(API_TOKEN,use_context=True)

dispatcher = updater.dispatcher

def music(update: Update, context: CallbackContext):

    if len(context.args) == 0:
        msg = 'Send a message in format "/music https://youtu.be/iik25wqIuFo"'
        context.bot.send_message(
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
        context.bot.send_audio(chat_id=update.effective_chat.id,
                                audio=open(dl.song, 'rb'),
                                performer=dl.author,
                                title=dl.title,
                                caption="@invisiblemusicbot")
    except Exception as e:
        context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=
                    str(e),
                    parse_mode=ParseMode.HTML,
        )

def notify_owner(update: Update, context: CallbackContext, err: str):
    msg = f'User @{update.effective_user.username} has tried downloading music, but got an error:\n\n{err}'
    context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=msg,
            parse_mode=ParseMode.HTML,
    )

def send_msg(update: Update, context: CallbackContext):
    music_src = update.effective_message.text
    try:
        dl = Downloader(music_src)
        context.bot.send_audio(chat_id=update.effective_chat.id,
                                audio=open(dl.song, 'rb'),
                                performer=dl.author,
                                title=dl.title,
                                caption="@invisiblemusicbot")
    except Exception as e:
        if str(e) == "Invalid YouTube link":
            context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=
                    "Please, send a valid link to YouTube video",
                    parse_mode=ParseMode.HTML,
        ) 
        else:
            notify_owner(update, context, str(e))
            context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=
                        "Sorry, an error has occured. Please, report the error to @INV1SBLE",
                        parse_mode=ParseMode.HTML,
            )

dispatcher.add_handler(CommandHandler("music", music))
dispatcher.add_handler(MessageHandler(Filters.chat_type.private,send_msg))

updater.start_polling()

