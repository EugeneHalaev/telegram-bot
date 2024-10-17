import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime  # Импортируем модуль для работы с датами

API_TOKEN = '7617166979:AAH22S6YiW6jsYkTBttWGLc4bmuV2VGzIhw'  # Замените на ваш токен Telegram бота
CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'  # URL для получения курсов валют

async def get_exchange_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(CURRENCY_API_URL)
    data = response.json()

    # Проверяем, есть ли ошибка в ответе
    if response.status_code != 200 or 'rates' not in data:
        await update.message.reply_text("Не удалось получить курс валют. Попробуйте позже.")
        return

    # Получаем курс USD/PLN и EUR/PLN
    usd_to_pln = data['rates'].get('PLN')
    
    # Запрос на другой API для получения курсов валют (если API не поддерживает несколько валют)
    eur_response = requests.get('https://api.exchangerate-api.com/v4/latest/EUR')
    eur_data = eur_response.json()
    
    if eur_response.status_code != 200 or 'rates' not in eur_data:
        await update.message.reply_text("Не удалось получить курс EUR/PLN. Попробуйте позже.")
        return

    eur_to_pln = eur_data['rates'].get('PLN')

    # Получаем сегодняшнюю дату
    today = datetime.now().strftime("%d.%m.%Y")  # Форматируем дату

    if usd_to_pln and eur_to_pln:
        await update.message.reply_text(
            f'Курс на {today}\n'  # Изменено сообщение
            f'USD/PLN: {usd_to_pln}\n'
            f'EUR/PLN: {eur_to_pln}'
        )
    else:
        await update.message.reply_text('Не удалось получить курсы валют.')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Используйте команду /rate для получения курсов USD/PLN и EUR/PLN.')

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('rate', get_exchange_rate))
    application.run_polling()