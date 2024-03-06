# Mistral Telegram Chatbot 🤖

## Overview

This is a chatbot created using Python, Haystack, pydub, and the Hugging Face model `mistralai/Mistral-7B-Instruct-v0.2`. It supports text and voice messages, allowing users to interact with the chatbot in their preferred format.

## Features

- Text Conversations with `Mistral-7B-Instruct-v0.2` model
- Voice message Processing using Google Speech Recognition
- Chat Conversation tracking

## Prerequisites

- Hugging Face Token
- Telegram bot token

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/renuka010/Mistral-Telegram-Bot.git
    ```
2. Change into the project directory:
    ```bash
    cd Mistral-Telegram-Bot
    ```
3. Create and Activate the virtual environment:
    ```bash
    python3 -m venv venv  # Create
    venv\Scripts\activate    # Activate
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Create a `.env` file with your Huggingface token and Telegram token:
    ```
    HF_API_TOKEN=your_hf_token
    TELEGRAM_BOT_TOKEN=your_telegram_token
    ```
6. Run the server:
    ```bash
    python chatbot.py
    ```

## Future Scope

Creating vector-based memory for storing conversation history. (Currently, the project supports only inbuilt memory which can remember only the last 10 conversations from history.)

## Contributing

Contributions are welcome! If you'd like to contribute, please submit a pull request or open an issue with your proposed changes or bug reports.