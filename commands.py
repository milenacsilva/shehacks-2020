from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, Handler, CallbackQueryHandler

from register_user import User

FETCH_LOCATION, HELP_ME = range(2)
def get_current_location(update, context):
    text = "Clique aqui para confirmar endereço de entrega"
    keyboard = [[KeyboardButton(text=text, request_location=True)]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Informe o endereço de entrega", reply_markup=reply_markup)

    return FETCH_LOCATION

def fetch_location(update, context):
    location = update.message.location
    user_id = update.effective_user.id
    # TODO: Arrumar exceção 
    # if user_id not in context.user_data.keys() 
    context.user_data[user_id].current_location = location 


    keyboard = [[InlineKeyboardButton("Pizza aiuto", callback_data='1')],
                [InlineKeyboardButton("Pizza pericollo", callback_data='2')],
                [InlineKeyboardButton("Pizza minaccia", callback_data='3')]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Endereço de entrega salvo", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("Escolha seu pedido", reply_markup=reply_markup)
    return HELP_ME

def get_help_option(update, context):
    query = update.callback_query
    user_id = update.effective_user.id

    query.answer()

    context.user_data[user_id].set_help_option(query.data)
    query.edit_message_text("Pedido realizado")

    return help_me(update, context)

def __send_help_message_to_registered_contacts(update, context, help_option):
    ''' Base function for all others help commands '''
    user_id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.username
    location = context.user_data[user_id].current_location
    help_contacts = context.user_data[user_id].help_contacts 
    print(location)

    text = [f"<a href='https://t.me/{username}'> {name.title()} </a> está em situaçãode risco e precisa de sua ajuda", help_option]
    for contact in help_contacts:   
        print(contact)
        try:
            context.bot.send_message(
                chat_id = contact.user_id,
                text = "\n".join(text),
                parse_mode="HTML"
            )
            context.bot.send_location(
                chat_id = contact.user_id,
                latitude = location.latitude,
                longitude = location.longitude
            )
        except:
            print("Num mandei")

def help_me(update, context):
    user_id = update.effective_user.id
    help_option = context.user_data[user_id].help_option

    if help_option == '1':
        text = "Por favor, vá a localização atual"
    elif help_option == '2':
        text = "Por favor, chame a as autoridades"
    elif help_option == '3':
        text = "Ligue para o Disque Direitos Humanos"
    
    __send_help_message_to_registered_contacts(update, context, text)

    return ConversationHandler.END
    
def menu(update, context):
    help_menu = "./static/help_menu.png"

    bot_message = context.bot.send_photo(
        chat_id = update.message.chat_id,
        photo = open(file=help_menu, mode="rb")
    )
    #TODO: fazer com q o bot edite a foto do help menu para o fake menu

get_help = ConversationHandler(
    entry_points = [CommandHandler("teste", get_current_location)],
    states = {
        FETCH_LOCATION: [MessageHandler(Filters.location, fetch_location)],
        HELP_ME: [CallbackQueryHandler(get_help_option)]
    },
    fallbacks=[])

display_menu = CommandHandler("menu", menu)