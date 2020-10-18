from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

CPF, EMAIL, ADDRESS, HELP_CONTACTS = range(4)
GET_NEW_INFO, UPDATE_INFO = range(2)

class User():
    ''' Represents a user of the app '''
    def __init__(self, username):
        self.username = username
        self.cpf = None
        self.email = None
        self.address = None
        self.help_contacts = list()
        self.current_location = None
        self.help_option = None

    def set_current_location(self, location):
        self.current_location = location

    def set_help_option(self, help_option):
        self.help_option = help_option
    
    def set_cpf(self, cpf):
        self.cpf = cpf
    
    def set_email(self, email):
        self.email = email
    
    def set_address(self, address):
        self.address = address
    
    def add_help_contact(self, new_contact):
        self.help_contacts.append(new_contact)

def __register_user(update, context):
    ''' Private function to help register a new user '''
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if user_id not in context.user_data.keys():
        context.user_data[user_id] = User(username)
        return True

    return False

def register(update, context):
    ''' First command to be executed when a new user tries to register '''
    text = list()

    if not __register_user(update, context):
        text.append("Não se preocupe! Suas informções já estão cadastradas.🍕")
         
        text.append("Deseja mudar alguma informação? Digite /editar") 
        "\n".join(text)
        text.append("--->Endereço 🏡? Digite /endereco")
        update.message.reply_text("\n".join(text))
        text.append("--->Contatos favoritos 👩‍🦱👨‍🦱? Digite /contatos")
        "\n".join(text)
        text.append("--->CPF 1️⃣2️⃣3️⃣? Digite /cpf")
        "\n".join(text)
        text.append("--->E-mail 🗨? Digite /email")

        return ConversationHandler.END
    
    text.append(f"Olá {update.effective_user.username}, sabemos que está em uma situação difícil e por isso vamos te ajudar. Nos informe os seguintes dados, por favor:") #TODO
    text.append("CPF:") #TODO
    update.message.reply_text("\n".join(text))
    
    return CPF

def get_cpf(update, context):
    ''' Follow-up command, gets the cpf of the user '''
    user_id = update.effective_user.id
    context.user_data[user_id].cpf = update.message.text

    update.message.reply_text("E-mail usual:") #TODO    

    return EMAIL

def get_email(update, context):
    ''' Gets the user email '''
    user_id = update.effective_user.id
    context.user_data[user_id].email = update.message.text

    update.message.reply_text("Endereço onde geralmente ocorrem os delitos:") #TODO

    return ADDRESS

def get_address(update, context):
    ''' Gets the user address '''
    user_id = update.effective_user.id
    context.user_data[user_id].address = update.message.text

    update.message.reply_text("Nos envie os seus contatos que você mais confia, pois eles irão te socorrer quando preciso. Assim que terminar, digite /concluir")

    return HELP_CONTACTS

def get_help_contacts(update, context):
    ''' Get all the help contacts from the user '''
    user_id = update.effective_user.id 
    new_contact = update.message.contact
    if new_contact:
        context.user_data[user_id].help_contacts.append(new_contact)
    else:
        update.message.reply_text("Por favor, nos informe um contato que está salvo em seu celular.") #TODO
    
    return HELP_CONTACTS

def conclude_registration(update, context):
    ''' Finishs the registration conversation '''
    update.message.reply_text("Agora estamos com você. Use os seguintes comandos quando precisar ser socorrida:")
    
    # BOTAR A LISTA DE COMANDO AQ TODO
    
    return ConversationHandler.END

def edit(update, context):
    user_id = update.effective_user.id
    user_data = context.user_data

    if user_id not in user_data.keys():
        update.message.reply_text("Você ainda não está cadastrada. Vamos lá?")
        #ai mnada printar toda a mensagem de cadastro da def register
        return ConversationHandler.END

    keyboard = [[InlineKeyboardButton("Cpf<- esses nomes aqui", callback_data='1'), # ANA TODO
                 InlineKeyboardButton("Email", callback_data='2'),
                 InlineKeyboardButton("Endereço", callback_data='3')],
                [InlineKeyboardButton("Lista de Contatos", callback_data='4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("O quê você deseja editar", reply_markup=reply_markup)

    return GET_NEW_INFO 

def get_new_info(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(f"Me mando o novo f{query.data}")
    context.bot_data['query_data'] = [query.data,]    
   
    return UPDATE_INFO

def update_info(update, context):
    user_id = update.effective_user.id
    user_data = context.user_data
    info_to_update = context.bot_data['query_data'].pop(0)

    if info_to_update == '1':
        new_info = update.message.text
        user_data[user_id].set_cpf(new_info)
    elif info_to_update == '2':
        new_info = update.message.text
        user_data[user_id].set_email(new_info)
    elif info_to_update == '3':
        new_info = update.message.text
        user_data[user_id].set_address(new_info)
    elif info_to_update == '4':
        new_info = update.message.contact
        if not new_info:
            update.message.reply_text("Mande um novo contato válido")
            return UPDATE_INFO
    
        user_data[user_id].add_help_contact(new_info)

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