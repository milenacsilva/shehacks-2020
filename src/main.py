from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from env import TOKEN
import logging
from menu import display_real_menu, swap_menu
from commands import get_help
from register_user import registration, edit_info, user_data
from utils import write_JSON, USERS


def start(update, context):
    update.message.reply_text("Bem-vindo(a) à Pizzaria Hortênsia!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(display_real_menu)
    dp.add_handler(swap_menu)
    dp.add_handler(get_help)
    dp.add_handler(registration)
    dp.add_handler(edit_info)

    updater.start_polling()
    print("++++++ STARTING BOT ++++++")
    updater.idle()
    print("+++++++ KILLING BOT ++++++")
    write_JSON(user_data, USERS)


if __name__ == "__main__":
    print("Press CTRL^C to kill the bot")
    main()
