from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

# Função que mostrará o cardápio verdadeiro junto a um botão
# Quando pressionado, o cardápio mudará para o falso
def menu(update, context):
    keyboard = [[InlineKeyboardButton(text="Clique aqui para esconder o cardápio!", callback_data='menu')]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    prompt = "Este é o nosso cardápio:"
    photo = "../static/help_menu.png"
    context.bot.send_message(chat_id=update.effective_chat.id, text=prompt)
    text_id = context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(photo, 'rb'), reply_markup=markup)
    context.bot_data['text_id'] = text_id.message_id # Guardando para exclusão posterior da imagem

def query_handler(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'menu':
        text_id = context.bot_data['text_id']
        context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id) # Deletando o botão
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=text_id) # Deletando o cardápio verdadeiro
        media = "../static/fake_menu.png"
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(media, 'rb')) # Enviando o cardápio falso
        answer = "Agradecemos pela preferência!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

swap_menu = CallbackQueryHandler(query_handler, pattern='^menu$')
display_real_menu = CommandHandler("menu", menu) 