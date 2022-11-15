import telebot
from config import settings #токен хранится в отдельнов файле в целях безопасности

bot = telebot.TeleBot(settings['token'])

commands = {
    "/help": "Привет, чтобы увидеть список доступных комманд напиши /commands",
    "/info": "Я бот, написанный Иваном Петрухиным из БИБ225 в качестве его первого проекта",
    "Привет": "Привет, чем я могу тебе помочь?"
}

bot.delete_my_commands(scope=None, language_code=None)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("/help", "помощь"),
        telebot.types.BotCommand("/info", "информация о боте"),
        telebot.types.BotCommand("/commands", "Вывести список доступных команд")
    ],
)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in commands:
        bot.send_message(message.from_user.id, commands[message.text])
    elif message.text == "/commands":
        bot.send_message(message.from_user.id, """На данный момент сущестуют команды: 
        /help - помощь 
        /info - информация о боте 
        /commands - выводит список доступных команд""")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help или /commands")


bot.polling(none_stop=True, interval=0)
