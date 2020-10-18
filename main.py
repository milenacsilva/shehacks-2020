from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from env import TOKEN
import logging
from delete import test
from register_user import registration, helpme
from commands import display_menu, get_help


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

CPF, EMAIL, ADDRESS, HELP_CONTACTS = range(4)

# def start(update, context):
#     text = "Informar Localização"
#     keyboard = [
#         [KeyboardButton(text=text, request_location=True)]
#         ]

#     reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
#     update.message.reply_text("aopa", reply_markup=reply_markup)


# def fetch_location(update, context):
#     location = update.message.location
#     print(location)

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
    # dp.add_handler(helpme)

    updater.start_polling()
    print("++++++ STARTING BOT ++++++")
    updater.idle()
    print("+++++++ KILLING BOT ++++++")



if __name__ == "__main__":
    print("Press CTRL^C to kill the bot")
    main()