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
    Detect the language of the given text with enhanced keyword matching.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        Optional[str]: Language code or None if detection fails
    """
    try:
        # First try automatic detection
        detected_lang = detect(text)
        logger.info(f"Initial language detection: {detected_lang}")
        
        # Enhanced keyword matching for better accuracy
        text_lower = text.lower().strip()
        
        # Portuguese keywords and common words
        portuguese_words = [
            'olá', 'oi', 'tchau', 'obrigado', 'obrigada', 'por favor', 'desculpa',
            'meu', 'minha', 'nome', 'sou', 'está', 'como', 'que', 'para', 'com',
            'não', 'sim', 'tudo', 'bem', 'muito', 'bom', 'dia', 'noite', 'tarde',
            'você', 'eu', 'ele', 'ela', 'nós', 'vocês', 'eles', 'elas',
            'casa', 'trabalho', 'escola', 'água', 'comida', 'tempo', 'hoje',
            'ontem', 'amanhã', 'agora', 'depois', 'antes', 'aqui', 'ali', 'lá'
        ]
        
        # English keywords and common words
        english_words = [
            'hello', 'hi', 'bye', 'thank you', 'thanks', 'please', 'sorry',
            'my', 'name', 'is', 'how', 'are', 'you', 'what', 'where', 'when',
            'good', 'morning', 'evening', 'night', 'yes', 'no', 'very', 'nice',
            'alright', 'okay', 'ok', 'the', 'and', 'but', 'with', 'from',
            'this', 'that', 'here', 'there', 'now', 'then', 'today', 'tomorrow',
            'work', 'home', 'school', 'water', 'food', 'time'
        ]
        
        # Check for exact word matches or word boundaries
        words_in_text = text_lower.split()
        has_portuguese = any(word in portuguese_words for word in words_in_text) or any(pt_word in text_lower for pt_word in portuguese_words)
        has_english = any(word in english_words for word in words_in_text) or any(en_word in text_lower for en_word in english_words)
        
        # Override detection for very short texts or when keywords are found
        if has_portuguese and not has_english:
            logger.info(f"Override: Portuguese keywords detected in text")
            return PORTUGUESE
        elif has_english and not has_portuguese:
            logger.info(f"Override: English keywords detected in text")
            return ENGLISH
        elif detected_lang in ['pt', 'pt-br', 'pt-pt']:
            logger.info(f"Confirmed Portuguese detection")
            return PORTUGUESE
        elif detected_lang in ['en', 'en-us', 'en-gb', 'en-ca', 'en-au']:
            logger.info(f"Confirmed English detection")
            return ENGLISH
        else:
            logger.info(f"Using automatic detection result: {detected_lang}")
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

def format_translation_response(translated_text: str, target_lang: str, user_name: str = "Usuário") -> str:
    """
    Format the translation response with appropriate flag and personalized message.
    
    Args:
        translated_text (str): The translated text
        target_lang (str): Target language code
        user_name (str): The name of the user who sent the message
        
    Returns:
        str: Formatted response message
    """
    if target_lang == ENGLISH:
        # Portuguese to English: "[Name] said:"
        return f"{user_name} said:\n{translated_text}"
    elif target_lang == PORTUGUESE:
        # English to Portuguese: "[Name] disse:"
        return f"{user_name} disse:\n{translated_text}"
    else:
        return translated_text

def is_supported_language(lang: str) -> bool:
    """
    Check if the detected language is supported by the bot.
    Includes enhanced language detection for Portuguese and English variations.
    
    Args:
        lang (str): Language code to check
        
    Returns:
        bool: True if language is supported, False otherwise
    """
    # Support Portuguese and English, plus common variants
    supported_languages = [
        PORTUGUESE, ENGLISH,
        'pt-br', 'pt-pt',  # Brazilian and European Portuguese
        'en-us', 'en-gb', 'en-ca', 'en-au',  # English variants
        'es', 'it', 'ca', 'gl', 'fr'  # Romance languages often misdetected as Portuguese
    ]
    return lang in supported_languages

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
