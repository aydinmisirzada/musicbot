import os
from pytube import YouTube
from telegram import Message
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
from telegram.parsemode import ParseMode
import re

API_TOKEN = os.environ['TELEGRAM_TOKEN']


updater = Updater(API_TOKEN,use_context=True)

dispatcher = updater.dispatcher

def music(update: Update, context: CallbackContext):

    if len(context.args) == 0:
        msg = 'Send a message in format "/music link_to_youtube"'
        context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=
                    msg,
                    reply_to_message_id=update.effective_message.message_id,
                    parse_mode=ParseMode.HTML,
        )
        return

    music_src = context.args[0]
    yt = YouTube(music_src)
    music = yt.streams.filter(only_audio=True).first()
    msg = "Sorry, the audio can't be downloaded"
    if music is None:
        context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=
                    msg,
                    parse_mode=ParseMode.HTML,
        )
    music_title = yt.title
    music = music.download()
    pattern = "(.*) -(.*)"
    matchObject = re.match(pattern,music_title)
    performer = yt.author or "Unknown Author"
    if matchObject is not None:
        performer =  matchObject.group(1)
        music_title = matchObject.group(2).strip() or music_title
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(music, 'rb'),
                        performer=performer,title=music_title)


dispatcher.add_handler(CommandHandler("music", music))

updater.start_polling()









#
