import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Берем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv('8229212850:AAHZ_dpFeCSCSVJMlZxWGD1rJjxiHOV4Rgs', 'ВАШ_ТОКЕН')

# Простая имитация тарифов
def get_fake_taxi_prices(lat, lon):
    return [
        ('Эконом', '250 ₽'),
        ('Комфорт', '400 ₽'),
        ('Бизнес', '700 ₽')
    ]

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    prices = get_fake_taxi_prices(lat, lon)

    msg = ''
    icons = {'Эконом':'🚗','Комфорт':'🚙','Бизнес':'💼'}
    for name, price in prices:
        msg += f"{icons.get(name,'🚘')} {name}: {price}\n"

    await update.message.reply_text(msg)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    print('Бот запущен в группе...')
    app.run_polling()
