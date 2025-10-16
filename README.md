Готовый проект TaxiBot — бот для Telegram, который по отправленной геолокации присылает блок тарифов Яндекс.Такси.
Файлы в архиве:
- bot.py
- requirements.txt
- icons/econ.png, icons/comfort.png, icons/business.png

Инструкция кратко:
1. Замените TELEGRAM_TOKEN в bot.py на ваш токен от BotFather.
2. Загрузите репозиторий на GitHub или прямо на Render.
3. В Render создайте Web Service, подключив репозиторий:
   - Build Command: pip install -r requirements.txt
   - Start Command: python bot.py
4. Добавьте бота в группу и дайте права отправлять сообщения и фото.
5. Участники присылают локацию — бот отвечает скриншотом тарифов.

Примечания:
- Иконки в папке icons — простые заглушки. Можете заменить на свои.
- Render требует опции --no-sandbox и --disable-dev-shm-usage в хроме; они добавлены в код.
- Если возникнут ошибки с Selenium на Render, возможно потребуется добавить buildpack или использовать готовый контейнер с Chrome. Пиши — помогу.
