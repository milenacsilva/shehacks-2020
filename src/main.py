from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from env import TOKEN
import logging
from delete import test
from register_user import registration, edit_info, user_data
from commands import display_menu, get_help
from getdata import write_JSON, USERS

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

CPF, EMAIL, ADDRESS, HELP_CONTACTS = range(4)

def start(update, context):
    update.message.reply_text("Bem vindo a pizzaria")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(MessageHandler(Filters.location, fetch_location))
    # dp.add_handler(CommandHandler("test", test))
    dp.add_handler(registration)
    dp.add_handler(display_menu)
    dp.add_handler(get_help)
    # dp.add_handler(voice_recognition)
    dp.add_handler(edit_info)

    updater.start_polling()
    print("++++++ STARTING BOT ++++++")
    updater.idle()
    print("+++++++ KILLING BOT ++++++")
    write_JSON(user_data, USERS)


if __name__ == "__main__":
    print("Press CTRL^C to kill the bot")
    main()