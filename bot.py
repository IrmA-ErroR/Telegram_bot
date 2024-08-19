##### Эхо-бот
import config
import telebot

bot = telebot.TeleBot(config.TOKEN) # Присваивание токена


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Функция повтора сообщений (название не важно)
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True) # Цикл
