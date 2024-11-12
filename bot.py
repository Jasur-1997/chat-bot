import telebot

# Замените 'YOUR_TOKEN' на токен вашего бота от BotFather
bot = telebot.TeleBot('YOUR_TOKEN')

# ID администратора — замените на реальный ID администратора
admin_id = 123456789  # Здесь укажите id вашего администратора

# Словарь для хранения сопоставлений ID пользователя и администратора
user_admin_map = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Вы можете отправить мне сообщение, и я перешлю его администратору.")

# Обработчик всех входящих сообщений от пользователей
@bot.message_handler(func=lambda message: message.chat.id != admin_id)
def handle_user_message(message):
    user_id = message.chat.id
    user_admin_map[user_id] = admin_id
    bot.send_message(admin_id, f"Сообщение от {message.from_user.first_name} (ID: {message.from_user.id}): {message.text}")
    bot.reply_to(message, "Ваше сообщение отправлено администратору.")

# Обработчик всех сообщений от администратора
@bot.message_handler(func=lambda message: message.chat.id == admin_id)
def handle_admin_message(message):
    # Для успешной маршрутизации ответа администратора введите ID пользователя в начале сообщения
    try:
        user_id, user_message = message.text.split(' ', 1)
        user_id = int(user_id)
        if user_id in user_admin_map:
            bot.send_message(user_id, f"Администратор ответил: {user_message}")
        else:
            bot.reply_to(message, "Неизвестный ID пользователя.")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, начните сообщение с ID пользователя и текста.")

# Запуск бота
bot.polling()
