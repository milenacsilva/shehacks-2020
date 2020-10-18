from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

# Função que mostrará o cardápio verdadeiro junto a um botão
# Quando pressionado, o cardápio mudará para o falso
def cardapio(update, context):
    keyboard = [[InlineKeyboardButton(text="Clique aqui quando estiver pronto(a) para pedir!", callback_data='help')]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    prompt = "Este é o nosso cardápio:"
    photo = open("comandos.png", 'rb')
    context.bot.send_message(chat_id=update.effective_chat.id, text=prompt)
    global text_id # Guardando a mensagem com a foto para exclusão
    text_id = context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=photo, reply_markup=markup)

def query_handler(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'help':
        context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id) # Deletando o botão
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=text_id.message_id) # Deletando o cardápio verdadeiro
        media = open("falso.png", 'rb')
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=media) # Enviando o cardápio falso
        answer = "Agradecemos pela preferência!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
