from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw, ImageFont

# === ВАЖНО ===
# Перед загрузкой на Render или запуском локально замените строку ниже на ваш токен от BotFather:
TELEGRAM_TOKEN = "8229212850:AAHZ_dpFeCSCSVJMlZxWGD1rJjxiHOV4Rgs"

ICON_PATHS = {
    "Эконом": "icons/econ.png",
    "Комфорт": "icons/comfort.png",
    "Бизнес": "icons/business.png"
}

def get_taxi_prices_with_real_icons(lat, lon):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1200,1200")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://taxi.yandex.ru/?pickup-lat={lat}&pickup-lon={lon}"
    driver.get(url)

    try:
        block = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-tid='OfferList']"))
        )
    except Exception as e:
        print("Error waiting for OfferList:", e)
        driver.quit()
        return None

    try:
        offers = block.find_elements(By.CSS_SELECTOR, "[data-tid='OfferCard']")
    except:
        offers = []
    offer_data = []
    for offer in offers:
        try:
            price_elem = offer.find_element(By.CSS_SELECTOR, "[data-tid='Price']")
            name_elem = offer.find_element(By.CSS_SELECTOR, "[data-tid='Name']")
            price = price_elem.text
            name = name_elem.text
            offer_data.append((name, price))
        except:
            continue

    driver.save_screenshot("full_screenshot.png")
    location = block.location
    size = block.size
    driver.quit()

    x, y = int(location['x']), int(location['y'])
    width, height = int(size['width']), int(size['height'])
    im = Image.open("full_screenshot.png").convert("RGBA")
    im_cropped = im.crop((x, y, x + width, y + height))

    draw = ImageDraw.Draw(im_cropped)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()

    for i, (name, price) in enumerate(offer_data):
        cy = 10 + i*50
        icon_path = ICON_PATHS.get(name)
        if icon_path and os.path.exists(icon_path):
            icon = Image.open(icon_path).convert("RGBA").resize((36,36))
            im_cropped.paste(icon, (8, cy), icon)
        draw.text((56, cy+8), f"{name}: {price}", fill="black", font=font)

    screenshot_path = "taxi_prices_real_icons.png"
    im_cropped.save(screenshot_path)
    return screenshot_path

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    await update.message.reply_text("Формирую тарифы с иконками авто...")
    screenshot_path = get_taxi_prices_with_real_icons(lat, lon)
    if screenshot_path:
        with open(screenshot_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось получить цены.")

if __name__ == "__main__":
    import os
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    print("Бот запущен в группе...")
    app.run_polling()
