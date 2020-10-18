from telegram.ext import MessageHandler, ConversationHandler, Filters, CommandHandler
import speech_recognition as sr
import subprocess


def convert_ogg_to_wav(audio):
    dot_ogg = './static/audio.ogg'
    dot_wav = './static/audio.wav'
    audio.download(dot_ogg)
    subprocess.run(['ffmpeg', '-i', dot_ogg, dot_wav, '-y'])

    return dot_wav

def audio_interpreter(update, context):
    try:
        voice = context.bot.getFile(update.message.reply_to_message.voice)
    except:
        update.message.reply_text("Opa, acho q não entendi seu pedido")
        return ConversationHandler.END

    wav = convert_ogg_to_wav(voice)
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(wav) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language= 'pt-BR')
        except:
            text = "Opa, acho q não entendi seu pedido"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

voice_recognition = CommandHandler("audio", audio_interpreter)