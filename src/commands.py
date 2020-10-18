from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, Handler, CallbackQueryHandler


FETCH_LOCATION, HELP_ME = range(2)
def get_current_location(update, context):
    text = "Clique aqui para confirmar endereço de entrega"
    keyboard = [[KeyboardButton(text=text, request_location=True)]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Informe o endereço de entrega", reply_markup=reply_markup)

    return FETCH_LOCATION

def fetch_location(update, context):
    location = update.message.location
    user_data = context.user_data

    if not user_data:
        update.message.send_message("Você ainda não está cadastrada")
        return ConversationHandler.END 
   
    user_data['current_location'] = location 


    keyboard = [
                [InlineKeyboardButton("Pizza aiuto", callback_data='1')],
                [InlineKeyboardButton("Pizza pericollo", callback_data='2')],
                [InlineKeyboardButton("Pizza minaccia", callback_data='3')]
                ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Endereço de entrega salvo", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("Escolha seu pedido", reply_markup=reply_markup)
    return HELP_ME

def get_help_option(update, context):
    query = update.callback_query
    user_data = context.user_data

    query.answer()

    user_data['help_option'] = query.data
    query.edit_message_text("Pedido realizado")

    return help_me(update, context)

def _send_help_message_to_registered_contacts(update, context, help_option):
    ''' Base function for all others help commands '''
    user_data = context.user_data
    name = update.effective_user.first_name
    username = update.effective_user.username 
    
    text = [f"<a href='https://t.me/{username}'> {name.title()} </a> está em situaçãode risco e precisa de sua ajuda", help_option]
    for contact in user_data['help_contacts']:   
        try:
            context.bot.send_message(
                chat_id = contact.user_id,
                text = "\n".join(text),
                parse_mode="HTML"
            )
            context.bot.send_location(
                chat_id = contact.user_id,
                latitude = user_data['current_location'].latitude,
                longitude = user_data['current_location'].longitude
            )
        except:
            print("Num mandei")

def help_me(update, context):
    user_data = context.user_data
    help_option = user_data['help_option']

    if help_option == '1':
        text = "Por favor, vá a localização atual"
    elif help_option == '2':
        text = "Por favor, chame a as autoridades"
    elif help_option == '3':
        text = "Ligue para o Disque Direitos Humanos"
    
    _send_help_message_to_registered_contacts(update, context, text)

    return ConversationHandler.END

get_help = ConversationHandler(
    entry_points = [CommandHandler("teste", get_current_location)],
    states = {
        FETCH_LOCATION: [MessageHandler(Filters.location, fetch_location)],
        HELP_ME: [CallbackQueryHandler(get_help_option)]
    },
    fallbacks=[])
