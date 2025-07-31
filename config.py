"""
Configuration file for the Telegram Translation Bot
"""
import os

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8349056540:AAHZTPt7X9X5bJLuOrD6ZYx6EyXAwpOPgs8")

# Language codes
PORTUGUESE = 'pt'
ENGLISH = 'en'

# Emoji flags
BRAZIL_FLAG = "🇧🇷"
USA_FLAG = "🇺🇸"

# Messages
PORTUGUESE_VERSION_MSG = f"{BRAZIL_FLAG} Versão em português:"
ENGLISH_VERSION_MSG = f"{USA_FLAG} Versão em inglês:"

# Error messages
TRANSLATION_ERROR_MSG = "❌ Desculpe, não foi possível traduzir esta mensagem."
DETECTION_ERROR_MSG = "❌ Não foi possível detectar o idioma da mensagem."
UNSUPPORTED_LANGUAGE_MSG = "❌ Este bot só traduz entre português e inglês."

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
