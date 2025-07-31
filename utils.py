"""
Utility functions for the Telegram Translation Bot
"""
import logging
from typing import Optional
from langdetect import detect
from deep_translator import GoogleTranslator
from config import PORTUGUESE, ENGLISH, PORTUGUESE_VERSION_MSG, ENGLISH_VERSION_MSG

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of the given text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        Optional[str]: Language code or None if detection fails
    """
    try:
        detected_lang = detect(text)
        logger.info(f"Detected language: {detected_lang}")
        return detected_lang
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return None

def translate_text(text: str, source_lang: str, target_lang: str) -> Optional[str]:
    """
    Translate text from source language to target language.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
        
    Returns:
        Optional[str]: Translated text or None if translation fails
    """
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text)
        logger.info(f"Translation successful: {source_lang} -> {target_lang}")
        return translated_text
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return None

def format_translation_response(translated_text: str, target_lang: str) -> str:
    """
    Format the translation response with appropriate flag and message.
    
    Args:
        translated_text (str): The translated text
        target_lang (str): Target language code
        
    Returns:
        str: Formatted response message
    """
    if target_lang == ENGLISH:
        return f"{ENGLISH_VERSION_MSG}\n{translated_text}"
    elif target_lang == PORTUGUESE:
        return f"{PORTUGUESE_VERSION_MSG}\n{translated_text}"
    else:
        return translated_text

def is_supported_language(lang: str) -> bool:
    """
    Check if the detected language is supported by the bot.
    
    Args:
        lang (str): Language code to check
        
    Returns:
        bool: True if language is supported, False otherwise
    """
    return lang in [PORTUGUESE, ENGLISH]

def get_target_language(source_lang: str) -> str:
    """
    Get the target language for translation based on source language.
    
    Args:
        source_lang (str): Source language code
        
    Returns:
        str: Target language code
    """
    if source_lang == PORTUGUESE:
        return ENGLISH
    elif source_lang == ENGLISH:
        return PORTUGUESE
    else:
        return ENGLISH  # Default fallback
