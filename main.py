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

    # Получаем заголовок поста и ссылку
    text = post.title
    link = post.links[0].href

    #лог для консоли
    print(data)
    print(text)
    print(link)
    print('---------------------------------')

    # Отправляем сообщение в канал
    bot.send_message(CHANNEL, '<a href="' + link + '">' + text + '</a>', parse_mode='HTML')

    #запись лога в файл
    with open('log.txt', "a") as log:
        log.write(data+"\n"+text+"\n"+link+"\n")