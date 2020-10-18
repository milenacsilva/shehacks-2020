from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from getdata import read_JSON, USERS
CPF, EMAIL, ADDRESS, HELP_CONTACTS = range(4)
GET_NEW_INFO, UPDATE_INFO = range(2)


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
        text.append("Não se preocupe! Suas informções já estão cadastradas.🍕")
         
        text.append("Deseja mudar alguma informação? Digite /edit") 
        "\n".join(text)
        text.append("--->Endereço 🏡? Digite /endereco")
        update.message.reply_text("\n".join(text))
        text.append("--->Contatos favoritos 👩‍🦱👨‍🦱? Digite /contatos")
        "\n".join(text)
        text.append("--->CPF 1️⃣2️⃣3️⃣? Digite /cpf")
        "\n".join(text)
        text.append("--->E-mail 🗨? Digite /email")

        return ConversationHandler.END
    
    text.append(f"Olá, {update.effective_user.username}, sabemos que está em uma situação difícil e por isso iremos te ajudar. Informe-nos os seguintes dados, por favor:") #TODO
    text.append("CPF:") #TODO
    update.message.reply_text("\n".join(text))
    
    return CPF

def get_cpf(update, context):
    ''' Follow-up command, gets the cpf of the user '''
    user_id = str(update.effective_user.id)
    user_data[user_id]['cpf'] = update.message.text

    update.message.reply_text("E-mail usual:") #TODO    

    return EMAIL

def get_email(update, context):
    ''' Gets the user email '''
    user_id = str(update.effective_user.id)
    user_data[user_id]['email'] = update.message.text

    update.message.reply_text("Endereço onde geralmente ocorrem os delitos:") #TODO

    return ADDRESS

def get_address(update, context):
    ''' Gets the user address '''
    user_id = str(update.effective_user.id)
    user_data[user_id]['address'] = update.message.text

    update.message.reply_text("Envie-nos os contatos nos quais mais confia, pois eles irão te socorrer quando preciso. Assim que terminar, digite /concluir")

    return HELP_CONTACTS

def get_help_contacts(update, context):
    ''' Get all the help contacts from the user '''
    user_id = str(update.effective_user.id) 
    new_contact = update.message.contact
    if new_contact:
        user_data[user_id]['help_contact_list'].append(new_contact)
    else:
        update.message.reply_text("Por favor, informe-nos um contato que está salvo em seu celular.") #TODO
    
    return HELP_CONTACTS

def conclude_registration(update, context):
    ''' Finishs the registration conversation '''
    update.message.reply_text("Agora estamos com você. Use os seguintes comandos quando precisar ser socorrida:")
    
    # BOTAR A LISTA DE COMANDO AQ TODO
    
    return ConversationHandler.END

def edit(update, context):
    user_id = str(update.effective_user.id)

    if user_id not in user_data.keys():
        update.message.reply_text("Você ainda não está cadastrada. Vamos lá?")
        #ai mnada printar toda a mensagem de cadastro da def register
        return ConversationHandler.END

    keyboard = [[InlineKeyboardButton("Cpf<- esses nomes aqui", callback_data='1'), # ANA TODO
                 InlineKeyboardButton("Email", callback_data='2'),
                 InlineKeyboardButton("Endereço", callback_data='3')],
                [InlineKeyboardButton("Lista de Contatos", callback_data='4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("O que você deseja editar?", reply_markup=reply_markup)

    return GET_NEW_INFO 

def get_new_info(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(f"Mande o novo f{query.data}")
    context.bot_data['query_data'] = [query.data,]    
   
    return UPDATE_INFO

def update_info(update, context):
    user_id = str(update.effective_user.id)
    info_to_update = context.bot_data['query_data'].pop(0)

    if info_to_update == '1':
        new_info = update.message.text
        user_data[user_id]['cpf'] = new_info
    elif info_to_update == '2':
        new_info = update.message.text
        user_data[user_id]['email'] = new_info
    elif info_to_update == '3':
        new_info = update.message.text
        user_data[user_id]['address'] = new_info
    elif info_to_update == '4':
        new_info = update.message.contact
        if not new_info:
            update.message.reply_text("Mande um novo contato válido")
            return UPDATE_INFO
    
        user_data[user_id]['help_contact_list'].append(new_info)

    update.message.reply_text("Informação atualizada com sucesso")
    return ConversationHandler.END

registration = ConversationHandler(
    entry_points = [CommandHandler("register", register)],
    states = {
        CPF: [MessageHandler(~Filters.regex('^/'), get_cpf)],
        EMAIL: [MessageHandler(~Filters.regex('^/'), get_email)],
        ADDRESS: [MessageHandler(~Filters.regex('^/'), get_address)],
        HELP_CONTACTS: [MessageHandler(~Filters.regex('^/'), get_help_contacts)],
    },
    fallbacks = [CommandHandler("concluir", conclude_registration)])

edit_info = ConversationHandler(
    entry_points= [CommandHandler("edit", edit)],
    states = {
        GET_NEW_INFO: [CallbackQueryHandler(get_new_info)],
        UPDATE_INFO: [MessageHandler(Filters.all, update_info)]
    },
    fallbacks=[])