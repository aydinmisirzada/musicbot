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
    with open('file.txt','w') as f:
        f.write('hello')
    yt = YouTube(music_src).streams.filter(only_audio=True).first().download()
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(yt, 'rb'))


dispatcher.add_handler(CommandHandler("music", music))

updater.start_polling()
# updater.idle()
