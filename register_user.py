from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

CPF, EMAIL, ADDRESS, HELP_CONTACTS = range(4)

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
        text.append("Não se preocupe! Suas informções já estão cadastradas.🍕") #TODO 
        text.append("Deseja mudar alguma informação? Digite /edit") #TODO
        update.message.reply_text("\n".join(text))
        return ConversationHandler.END
    
    text.append(f"Olá {update.effective_user.username}, não se preocupe, iremos te registrar rapidamente") #TODO
    text.append("Qual é seu cpf?") #TODO
    update.message.reply_text("\n".join(text))
    
    return CPF

def get_cpf(update, context):
    ''' Follow-up command, gets the cpf of the user '''
    user_id = update.effective_user.id
    context.user_data[user_id].cpf = update.message.text

    update.message.reply_text("Email para contato?") #TODO    

    return EMAIL

def get_email(update, context):
    ''' Gets the user email '''
    user_id = update.effective_user.id
    context.user_data[user_id].email = update.message.text

    update.message.reply_text("Endereço atual?") #TODO

    return ADDRESS

def get_address(update, context):
    ''' Gets the user address '''
    user_id = update.effective_user.id
    context.user_data[user_id].address = update.message.text

    update.message.reply_text("Me mande os contatos que vc mais confia, quando terminar de enviar todos os contatos, digite /concluir")

    return HELP_CONTACTS

def get_help_contacts(update, context):
    ''' Get all the help contacts from the user '''
    user_id = update.effective_user.id 
    new_contact = update.message.contact
    if new_contact:
        context.user_data[user_id].help_contacts.append(new_contact)
    else:
        update.message.reply_text("Por favor, me mande um contato válido") #TODO
    
    return HELP_CONTACTS

def conclude_registration(update, context):
    ''' Finishs the registration conversation '''
    update.message.reply_text("Você foi registrade com sucesso") #TODO
    
    return ConversationHandler.END

def helpme(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.username
    help_contacts = context.user_data[user_id].help_contacts 

    text = f"{username} precisa da sua ajuda"
    for contact in help_contacts:
        try:
            context.bot.send_message(
                chat_id = contact.user_id,
                text = text
            )
        except:
            pass

registration = ConversationHandler(
    entry_points = [CommandHandler("register", register)],
    states = {
        CPF: [MessageHandler(~Filters.regex('^/'), get_cpf)],
        EMAIL: [MessageHandler(~Filters.regex('^/'), get_email)],
        ADDRESS: [MessageHandler(~Filters.regex('^/'), get_address)],
        HELP_CONTACTS: [MessageHandler(~Filters.regex('^/'), get_help_contacts)],
    },
    fallbacks = [CommandHandler("concluir", conclude_registration)]
)

helpme = CommandHandler("helpme", helpme)