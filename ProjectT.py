import telebot
import fitz
import requests
from bs4 import BeautifulSoup as BS
from config import settings  # токен хранится в отдельнов файле в целях безопасности

bot = telebot.TeleBot(settings['token'])

commands = {
    "/help": "Привет, чтобы увидеть список доступных комманд напиши /commands",
    "/info": "Я бот, написанный Иваном Петрухиным из БИБ225 в качестве его первого проекта",
    "Привет": "Привет, чем я могу тебе помочь?",
    "/search": '''Отправьте свой снилс в формате: "Мой снилс: 123-456-789 01"'''
}


def last_news(link):
    site = requests.get(link)
    html = BS(site.content, 'html.parser')
    post = html.find('div', class_="post")
    title = post.find('a', {"class": "link link_dark2 no-visited"}).text
    news = title
    if news != []:
        return news
    else:
        return "что-то пошло не так"


def search_name(snils):
    pdf = fitz.open(settings['file'])
    flag = True
    for current_page in range(len(pdf)):
        page = pdf.load_page(current_page)
        if page.search_for(snils):
            flag = False
            message = ('%s найден на %i странице в файле ' % (snils, current_page + 1)) + settings['file_name']
            return message
    if flag:
        return 'Я не смог найти вас в приказах о зачисление'


bot.delete_my_commands(scope=None, language_code=None)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("/help", "помощь"),
        telebot.types.BotCommand("/info", "информация о боте"),
        telebot.types.BotCommand("/commands", "Вывести список доступных команд"),
        telebot.types.BotCommand("/search", "Искать себя в списке зачисленных"),
        telebot.types.BotCommand("/contacts", "Контакты НИУ ВШЭ"),
        telebot.types.BotCommand("/news", "Последняя новость для поступающих")
    ],
)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in commands:
        bot.send_message(message.from_user.id, commands[message.text])
    elif "Мой снилс: " in message.text:
        bot.send_message(message.from_user.id, search_name(message.text[11:]))
    elif message.text == "/commands":
        bot.send_message(message.from_user.id, """На данный момент сущестуют команды:
        /help - помощь
        /info - информация о боте
        /commands - выводит список доступных команд
        /search - поиск себя в приказе на зачисление
        /contacts - контакты НИУ ВШЭ
        /news - показывает последнюю новость для поступающих""")
    elif message.text == "/contacts":
        bot.send_message(message.from_user.id, """Контакты:
        Тел.: +7 (495) 771-32-32
        Факс.: +7 (495) 628-79-31
        Приёмная комиссия:
        +7 (495) 771-32-42
        +7 (495) 916-88-44""")
    elif message.text == "/news":
        bot.send_message(message.from_user.id, last_news(settings['link']))
        bot.send_message(message.from_user.id, settings['link'])
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help или /commands")


bot.polling(none_stop=True, interval=0)
