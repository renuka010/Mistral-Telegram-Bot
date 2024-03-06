from dotenv import load_dotenv
import os
import telebot
import requests

import speech_recognition as sr
from pydub import AudioSegment

from haystack.components.generators.chat import HuggingFaceTGIChatGenerator
from haystack.dataclasses import ChatMessage

# Last 10 chat conversations
msg = []

# Load environment variables from .env file
load_dotenv()

# Set Hugging Face API token
os.environ["HF_API_TOKEN"] = os.getenv("HF_API_TOKEN")

# Initialize Hugging Face Chat Generator
generator = HuggingFaceTGIChatGenerator(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    generation_kwargs={"max_new_tokens": 350},
)

generator.warm_up()

# Initialize Telegram Bot
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


# Start command
@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.reply_to(message, "Welcome to Mistral ChatBOT! What do you need help with?")


# Help command
@bot.message_handler(commands=["help"])
def bot_help(message):
    bot.reply_to(
        message,
        "Start typing to chat with Mistral bot 🤖. \n\n You can also send voice messages to chat with Mistral bot.",
    )


# Handle text messages
@bot.message_handler(func=lambda message: message.text)
def handle_text(message):
    msg.append(ChatMessage.from_user(message.text))
    response = generator.run(messages=msg)
    msg.append(response["replies"][0])
    bot.reply_to(message, response["replies"][0].content)
    if len(msg) > 20:
        msg.pop(0)
        msg.pop(0)


# Handle voice messages
@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    # Download voice message
    voice_file = bot.get_file(message.voice.file_id)
    file = requests.get(
        "https://api.telegram.org/file/bot{0}/{1}".format(TOKEN, voice_file.file_path)
    )
    with open("audio.ogg", "wb") as f:
        f.write(file.content)

    # Convert voice message to .wav format
    sound = AudioSegment.from_file("audio.ogg", format="ogg")
    sound.export("audio.wav", format="wav")

    # Convert voice meassage to text message
    recognizer = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio_file = recognizer.record(source)
        query = recognizer.recognize_google(audio_file)

    # Get response from Mistral bot
    msg.append(ChatMessage.from_user(query))
    response = generator.run(messages=msg)
    msg.append(response["replies"][0])
    bot.reply_to(message, response["replies"][0].content)

    os.remove("audio.ogg")
    os.remove("audio.wav")
    if len(msg) > 20:
        msg.pop(0)
        msg.pop(0)


if __name__ == "__main__":
    print("Bot is running...")
    print("Press Ctrl + C to stop bot")
    bot.polling()