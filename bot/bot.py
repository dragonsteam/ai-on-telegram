import requests
from telebot import TeleBot
from telebot.types import (
    WebAppInfo,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from django.conf import settings

from .models import Record

# from .text import get_text as _
# from .helpers.auth import register_user
# from .keyboards import get_main_keyboard
# from .handlers import register_handlers


# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

WEB_APP_URL = "https://alpaca-better-husky.ngrok-free.app"


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    # Create inline keyboard with a Web App button
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        "Open Mini App",
        web_app=WebAppInfo(url=WEB_APP_URL)  # Use WebAppInfo for inline Web Apps
    )
    markup.add(button)
    
    # Send a message with the Web App button
    bot.send_message(
        chat_id=message.chat.id,
        text="Hello! Click the button below to open the mini app:",
        reply_markup=markup
    )


@bot.message_handler(commands=['history'])
def history(message: Message):
    records = Record.objects.filter(user_id=message.chat.id)

    print("records:")
    print(len(records))

    if not records:
        bot.send_message(chat_id=message.chat.id, text='No records found.')
        return

    for record in records:
        bot.send_message(chat_id=message.chat.id, text=f'Question: {record.question} \n\nAnswer: {record.answer}')


@bot.message_handler(commands=['clear'])
def history(message: Message):
    Record.objects.filter(user_id=message.chat.id).delete()

    bot.send_message(chat_id=message.chat.id, text="All records have been deleted.")


@bot.message_handler()
def handle_text(message: Message):
    

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={settings.GEMINI_API}"

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": message.text}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data).json()

    if response.get('error', None):
        bot.send_message(chat_id=message.chat.id, text="An error occured while proccessing your request.")
        return

    print(response)

    answer = response['candidates'][0]['content']['parts'][0]['text']

    bot.send_message(
        chat_id=message.chat.id,
        text=answer[:1000]
    )

    Record.objects.create(
        user_id=message.chat.id,
        question=message.text,
        answer=answer[:1000]
    )



def authorize_step(message: Message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = KeyboardButton(text="share ", request_contact=True)
    markup.add(button)
    msg = bot.reply_to(message, "share your phone", reply_markup=markup)
    bot.register_next_step_handler(msg, process_phone_step)


def process_phone_step(message: Message):
    # check if user actually share a contact number
    if not message.contact:
        bot.reply_to(message, "you didnt share a contanct, fuck off ")
        return
    
    # check if that contact belongs to user (not other)
    if message.contact.user_id != message.from_user.id:
        bot.reply_to(message, "this contanct is not yours moron")
        return
    
    # register_user(message.contact.phone_number, message.from_user.id)
    bot.reply_to(message, "registery success")


# register_handlers(bot)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()



"""
{"candidates": [{"content": {"parts": [{"text": "Salom!  (Hello!) How can I help you today?\n"}], "role": "model"}, "finishReason": "STOP", "avgLogprobs": -0.15449368158976237}], "usageMetadata": {"promptTokenCount": 2, "candidatesTokenCount": 15, "totalTokenCount": 17}, "modelVersion": "gemini-1.5-flash-latest"}
"""