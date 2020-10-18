from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from utils import read_JSON, USERS
CPF, EMAIL, ADDRESS, HELP_CONTACTS = range(4)
GET_NEW_INFO, UPDATE_INFO = range(2)


EDIT_CPF, EDIT_EMAIL, EDIT_ADDRESS, EDIT_HELP_CONTACT_LIST = range(4)

user_data = read_JSON(USERS)
def __register_user(update, context):
    ''' Private function to help register a new user '''
    user_id = str(str(update.effective_user.id))
    username = update.message.from_user.username

    if user_id not in user_data.keys():
        user_data[user_id] = dict()
        user_data[user_id]['username'] = username
        user_data[user_id]['help_contact_list'] = list()
        return True

    return False

def register(update, context):
    ''' First command to be executed when a new user tries to register '''
    text = list()

    if not __register_user(update, context):
        text.append("Não se preocupe! Suas informações já estão cadastradas.🍕")
        text.append("Deseja mudar alguma informação? Digite /edit") 
        for t in text:
            update.message.reply_text(t)

        return ConversationHandler.END
    
    text.append(f"Olá, {update.effective_user.username}, sabemos que está em uma situação difícil e por isso iremos te ajudar. Informe-nos os seguintes dados, por favor") 
    text.append("Qual é seu CPF?") 
    for t in text:
        update.message.reply_text(t)
    
    return CPF

def get_cpf(update, context):
    ''' Follow-up command, gets the cpf of the user '''
    user_id = str(update.effective_user.id)
    user_data[user_id]['cpf'] = update.message.text

    update.message.reply_text("E-mail usual?")     

    return EMAIL

def get_email(update, context):
    ''' Gets the user email '''
    user_id = str(update.effective_user.id)
    user_data[user_id]['email'] = update.message.text

    update.message.reply_text("Endereço de entrega?") 

    return ADDRESS

def get_address(update, context):
    ''' Gets the user address '''
    user_id = str(update.effective_user.id)
    user_data[user_id]['address'] = update.message.text
    

    keyboard = [[InlineKeyboardButton("Concluir registro", callback_data='finish')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Envie-nos contatos para saber das promoções! Assim que terminar, clique no botão a seguir", reply_markup=reply_markup)

    return HELP_CONTACTS

def get_help_contacts(update, context):
    ''' Get all the help contacts from the user '''
    user_id = str(update.effective_user.id) 
    new_contact = update.message.contact
    try:
        print(new_contact.user_id)
        user_data[user_id]['help_contact_list'].append({str(new_contact.user_id): new_contact.phone_number})
        update.message.reply_text("Contato adicionado")
    except:
        update.message.reply_text("Por favor, informe-nos um contato válido.") 


    return HELP_CONTACTS

def finish_registration(update, context):
    ''' Finishs the registration conversation '''
    query = update.callback_query
    query.answer()
    print("im here")
    query.message.reply_text("Agora estamos com você 🌺. Digite /menu para escolher o seu pedido.")
    
    return ConversationHandler.END

def edit(update, context):
    user_id = str(update.effective_user.id)

    if user_id not in user_data.keys():
        update.message.reply_text("Você ainda não está cadastrada. Vamos lá?")
        return ConversationHandler.END

    keyboard = [[InlineKeyboardButton("CPF 1️⃣2️⃣3️⃣", callback_data='edit_cpf'), 
                 InlineKeyboardButton("Email 📨", callback_data='edit_email'),
                 InlineKeyboardButton("Endereço 🏡", callback_data='edit_address')],
                [InlineKeyboardButton("Lista de Contatos 👨‍🦱👩‍🦱", callback_data='edit_help_contact_list')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("O que você deseja editar?", reply_markup=reply_markup)

    return GET_NEW_INFO 

def edit_cpf(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text("🆗, me informe o novo valor do seu CPF")
    context.bot_data['query_data'] = [query.data,]    
   
    return UPDATE_INFO

def edit_email(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text("🆗, me informe o novo valor do seu email")
    context.bot_data['query_data'] = [query.data,]    
   
    return UPDATE_INFO

def edit_address(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text("🆗, me informe seu novo endereço")
    context.bot_data['query_data'] = [query.data,]    
   
    return UPDATE_INFO

def edit_help_contact_list(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text("🆗, me informe o novo contato")
    context.bot_data['query_data'] = [query.data,]    
    
    return UPDATE_INFO

def update_info(update, context):
    user_id = str(update.effective_user.id)
    info_to_update = context.bot_data['query_data'].pop(0)

    if info_to_update == 'edit_cpf':
        new_info = update.message.text
        user_data[user_id]['cpf'] = new_info
    elif info_to_update == 'edit_email':
        new_info = update.message.text
        user_data[user_id]['email'] = new_info
    elif info_to_update == 'edit_address':
        new_info = update.message.text
        user_data[user_id]['address'] = new_info
    elif info_to_update == 'edit_help_contact_list':
        new_info = update.message.contact
        if not new_info:
            update.message.reply_text("Envie um novo contato válido que esteja em seu celular.")
            return UPDATE_INFO
    
        user_data[user_id]['help_contact_list'].append(new_info)

    update.message.reply_text("Informação atualizada com sucesso. 🌺")
    return ConversationHandler.END

registration = ConversationHandler(
    entry_points = [CommandHandler("register", register)],
    states = {
        CPF: [MessageHandler(~Filters.regex('^/'), get_cpf)],
        EMAIL: [MessageHandler(~Filters.regex('^/'), get_email)],
        ADDRESS: [MessageHandler(~Filters.regex('^/'), get_address)],
        HELP_CONTACTS: [MessageHandler(~Filters.regex('^/'), get_help_contacts)],
    },
    fallbacks = [CallbackQueryHandler(finish_registration, pattern="^finish$")])

edit_info = ConversationHandler(
    entry_points= [CommandHandler("edit", edit)],
    states = {
        GET_NEW_INFO: [CallbackQueryHandler(edit_cpf, pattern='^edit_cpf$'), CallbackQueryHandler(edit_email, pattern='^edit_email$'), CallbackQueryHandler(edit_address, pattern='^edit_address$'),CallbackQueryHandler(edit_help_contact_list, pattern='^edit_help_contact_list$')],
        UPDATE_INFO: [MessageHandler(Filters.all, update_info)]

    
    },
    fallbacks=[])