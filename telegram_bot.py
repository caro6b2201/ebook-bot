"""Telegram bot for the 'Beyond the Diagnosis' ebook."""

import os
import sys

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from chat import get_response, handle_greeting

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print(
        "Error: TELEGRAM_BOT_TOKEN environment variable not set.\n"
        "Run: TELEGRAM_BOT_TOKEN=your_token python3 telegram_bot.py"
    )
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)


def _detect_user_lang(message: telebot.types.Message) -> str:
    """Detect language from Telegram user's language_code, default to English."""
    code = getattr(message.from_user, "language_code", None) or ""
    return "es" if code.startswith("es") else "en"


def _build_reply(response: dict):
    """Convert a chat.py response dict to (text, markup) for Telegram."""
    text = response["text"]

    buttons = response.get("buttons", [])
    markup = None
    if buttons:
        markup = InlineKeyboardMarkup()
        for btn in buttons:
            label = btn["label"]
            action = btn["action"]
            if action.startswith("http"):
                markup.add(InlineKeyboardButton(label, url=action))
            else:
                markup.add(InlineKeyboardButton(label, callback_data=action))

    return text, markup


@bot.message_handler(commands=["start"])
def cmd_start(message):
    lang = _detect_user_lang(message)
    response = handle_greeting(lang)
    text, markup = _build_reply(response)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=["help"])
def cmd_help(message):
    lang = _detect_user_lang(message)
    if lang == "es":
        text = (
            "Puedes preguntarme sobre:\n\n"
            "- El contenido del libro\n"
            "- El precio\n"
            "- Los beneficios\n"
            "- La autora\n"
            "- Preguntas frecuentes\n"
            "- O simplemente escribir /start para comenzar"
        )
    else:
        text = (
            "You can ask me about:\n\n"
            "- The book's content\n"
            "- The price\n"
            "- The benefits\n"
            "- The author\n"
            "- Frequently asked questions\n"
            "- Or just type /start to begin"
        )
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    response = get_response(message.text)
    text, markup = _build_reply(response)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    response = get_response(call.data)
    text, markup = _build_reply(response)
    bot.send_message(call.message.chat.id, text, reply_markup=markup)
    bot.answer_callback_query(call.id)


if __name__ == "__main__":
    print("Bot is running... Press Ctrl+C to stop.")
    bot.infinity_polling()
