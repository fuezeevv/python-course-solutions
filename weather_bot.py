"""Telegram weather bot for Moscow, Saint Petersburg and Kazan.

Set TELEGRAM_BOT_TOKEN and WEATHER_API_KEY before running this file.
"""

import os

import requests
import telebot
from telebot import types


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "000")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "000")
bot = telebot.TeleBot(TOKEN)

CITIES = ("Moscow", "Saint Petersburg", "Kazan")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(city) for city in CITIES]
    keyboard.add(*buttons)
    bot.reply_to(
        message,
        "Привет! Я могу рассказать тебе погоду в Москве, Санкт-Петербурге и Казани",
        reply_markup=keyboard,
    )


@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip()
    if city not in CITIES:
        bot.reply_to(message, "Выберите город с помощью кнопок: Moscow, Saint Petersburg или Kazan")
        return
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": f"{city},ru", "appid": WEATHER_API_KEY, "units": "metric", "lang": "ru"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        bot.reply_to(message, f"Погода в {city}: {temperature}°C, {description}")
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        bot.reply_to(message, "Произошла ошибка при получении данных о погоде")


if __name__ == "__main__":
    if TOKEN == "000" or WEATHER_API_KEY == "000":
        raise SystemExit("Укажите TELEGRAM_BOT_TOKEN и WEATHER_API_KEY для запуска бота")
    bot.infinity_polling()
