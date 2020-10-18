from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, JobQueue, Job
from time import sleep

def test(update, context):
    s = "Seja bem-vinde ao chat da Pizzaria X, qual seria o seu pedido?"
    text = context.bot.send_message(chat_id=update.effective_chat.id, text=s)
    context.bot_data['message_ids'].append(text.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=text.message_id)
    context.job_queue.start()

def delete_message(update, context):
    message_id = context.bot_data['message_ids'].pop(0)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)

