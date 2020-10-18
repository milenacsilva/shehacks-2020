from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, Handler, CallbackQueryHandler
from register_user import user_data


FETCH_LOCATION, HELP_ME = range(2)
AUITO, PERICOLO, MINACCIA = range(3)

def get_current_location(update, context):
    text = "Clique aqui para confirmar endereço de entrega"
    keyboard = [[KeyboardButton(text=text, request_location=True)]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Informe o endereço de entrega:", reply_markup=reply_markup)

    return FETCH_LOCATION

def fetch_location(update, context):
    location = update.message.location
    user_id = str(update.effective_user.id) 

    if user_id not in user_data.keys():
        update.message.send_message("Você ainda não está cadastrado(a)")
        return ConversationHandler.END 
   
    user_data[user_id]['current_location'] = location 
    keyboard = [
                [InlineKeyboardButton("Pizza aiuto", callback_data=AUITO)],
                [InlineKeyboardButton("Pizza pericollo", callback_data=PERICOLO)],
                [InlineKeyboardButton("Pizza minaccia", callback_data=MINACCIA)]
                ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Endereço de entrega salvo", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("Escolha seu pedido:", reply_markup=reply_markup)
    return HELP_ME

def get_help_option(update, context):
    query = update.callback_query
    user_id = str(update.effective_user.id)

    query.answer()

    user_data[user_id]['help_option'] = query.data
    query.edit_message_text("Pedido realizado")

    return help_me(update, context)

def _send_help_message_to_registered_contacts(update, context, help_text):
    ''' Base function for all others help commands '''
    user_data = context.user_data
    name = update.effective_user.first_name
    user_id = str(update.effective_user.id)
    username = update.effective_user.username 
    
    text = [f"<a href='https://t.me/{username}'> {name.title()} </a> está em situação de risco e precisa de sua ajuda", help_text]
    for contact in user_data[user_id]['help_contacts']:   
        try:
            context.bot.send_message(
                chat_id = contact.user_id,
                text = "\n".join(text),
                parse_mode="HTML"
            )
            context.bot.send_location(
                chat_id = contact.user_id,
                latitude = user_data[user_id]['current_location'].latitude,
                longitude = user_data[user_id]['current_location'].longitude
            )
        except:
            pass

def help_me(update, context):
    user_data = context.user_data
    user_id = str(update.effective_user.id)
    help_option = user_data[user_id]['help_option']

    if help_option == AUITO:
        help_text = "Por favor, vá à localização atual"
    elif help_option == PERICOLO:
        help_text = "Por favor, chame as autoridades"
    elif help_option == MINACCIA:
        help_text = "Ligue para o Disque Direitos Humanos"
    
    _send_help_message_to_registered_contacts(update, context, help_text)

    return ConversationHandler.END

get_help = ConversationHandler(
    entry_points = [CommandHandler("teste", get_current_location)],
    states = {
        FETCH_LOCATION: [MessageHandler(Filters.location, fetch_location)],
        HELP_ME: [CallbackQueryHandler(get_help_option)]
    },
    fallbacks=[])
