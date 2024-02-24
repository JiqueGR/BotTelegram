import telebot
from deep_translator import GoogleTranslator

token = "YOUR_TOKEN_HERE"
idReceberMensagem = "YOUR_GROUP_HERE"
idEnviarMensagem = "YOUR_GROUP_HERE"
bot = telebot.TeleBot(token)
simboloRegistro = "\u00AE"

def analisar_mensagem(mensagem):
    if "t.me" in mensagem:
        return False
    elif simboloRegistro in mensagem:
        indiceRegistro = mensagem.find('\u00AE')
        mensagem_modificada = mensagem[:indiceRegistro]
        for indice, caractere in enumerate(mensagem):
            if caractere == '\n':
                indiceQuebra = indice
        try:
            mensagem_modificada = mensagem_modificada[:indiceQuebra]
        except:
            pass
        return mensagem_modificada
    else:
        return mensagem
def traduzir_texto(texto):
    tradutor = GoogleTranslator(source="auto", target="pt")
    traducao = tradutor.translate(texto)
    traducao = analisar_mensagem(traducao)
    if traducao:
        return traducao

@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    if str(idReceberMensagem) == str(message.chat.id):
        photo = message.photo[-1]
        if message.caption is not None:
            texto = traduzir_texto(message.caption)
            if texto:
                if len(texto) > 1024:
                    texto = texto[:1021] + "..."
                bot.send_photo(idEnviarMensagem, photo.file_id, caption=texto)
        else:
            bot.send_photo(idEnviarMensagem, photo.file_id, caption="")

@bot.message_handler(content_types=['text'])
def handle_messages(message):
    if str(idReceberMensagem) == str(message.chat.id):
        texto = traduzir_texto(message.text)
        if texto:
            bot.send_message(idEnviarMensagem, texto)


while True:
    try:
        bot.remove_webhook()
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Erro durante o polling: {e}")

