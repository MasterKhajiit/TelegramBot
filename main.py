import feedparser
import telebot
import configparser


# Считываем настройки
config = configparser.ConfigParser()
config.read('settings.ini')
FEED = config.get('RSS', 'feed')
DATETIME = config.get('RSS', 'DATETIME')
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
CHANNEL = config.get('Telegram', 'CHANNEL')

# Получаем RSS ленту
rss = feedparser.parse(FEED)

# Инициализируем телеграмм бота
bot = telebot.TeleBot(BOT_TOKEN)

for post in reversed(rss.entries):
    data = post.published
    data_old = config.get('RSS', 'DATETIME')

# Пропускаем уже опубликованные посты
    if data <= data_old:
        continue
    else:
        # Записываем время и дату нового поста в файл
        config.set('RSS', 'DATETIME', str(data))
        with open('settings.ini', "w") as config_file:
            config.write(config_file)

    print('---------------------------------')
    print(data)

    # Получаем заголовок поста
    text = post.title
    print(text)

    # Получаем ссылку на пост
    link = post.links[0].href
    print(link)

    # Отправляем картинку и текстовое описание в Telegram
    bot.send_message(CHANNEL, '<a href="' + link + '">' + text + '</a>', parse_mode='HTML')

    with open('log.txt', "a") as log:
        log.write(data+"\n"+text+"\n"+link)