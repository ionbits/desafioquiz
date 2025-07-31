"""
Telegram Translation Bot
Automatically translates messages between Portuguese and English
"""
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from utils import (
    detect_language, 
    translate_text, 
    format_translation_response, 
    is_supported_language,
    get_target_language
)
from config import (
    BOT_TOKEN,
    PORTUGUESE,
    ENGLISH,
    TRANSLATION_ERROR_MSG,
    DETECTION_ERROR_MSG,
    UNSUPPORTED_LANGUAGE_MSG
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TranslatorBot:
    """Telegram bot for automatic translation between Portuguese and English"""
    
    def __init__(self, token: str):
        """
        Initialize the translator bot.
        
        Args:
            token (str): Telegram bot token
        """
        self.token = token
        self.app = ApplicationBuilder().token(token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup message handlers for the bot"""
        # Handle all text messages that are not commands
        text_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), 
            self.translate_message
        )
        self.app.add_handler(text_handler)
        
        logger.info("Message handlers configured successfully")
    
    async def translate_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle incoming text messages and translate them.
        
        Args:
            update (Update): Telegram update object
            context (ContextTypes.DEFAULT_TYPE): Bot context
        """
        try:
            # Get the message text and user info
            text = update.message.text
            user_id = update.effective_user.id
            user_name = update.effective_user.first_name or "Usuário"
            
            if not text:
                logger.warning(f"Empty message received from user {user_id}")
                return
            
            logger.info(f"Processing message from user {user_id}: {text[:50]}...")
            
            # Detect language
            detected_lang = detect_language(text)
            
            if detected_lang is None:
                await update.message.reply_text(DETECTION_ERROR_MSG)
                return
            
            # Check if language is supported - if not, respond with "?"
            if not is_supported_language(detected_lang):
                logger.info(f"Unsupported language detected: {detected_lang}, responding with '?'")
                await update.message.reply_text("?")
                return
            
            # Get target language
            target_lang = get_target_language(detected_lang)
            
            # Translate the text
            translated_text = translate_text(text, detected_lang, target_lang)
            
            if translated_text is None:
                await update.message.reply_text(TRANSLATION_ERROR_MSG)
                return
            
            # Format and send the response with user's name
            response = format_translation_response(translated_text, target_lang, user_name)
            await update.message.reply_text(response)
            
            logger.info(f"Translation completed for user {user_id}")
            
        except Exception as e:
            logger.error(f"Unexpected error in translate_message: {e}")
            await update.message.reply_text(TRANSLATION_ERROR_MSG)
    
    def run(self):
        """Start the bot with polling"""
        try:
            logger.info("Starting Telegram Translation Bot...")
            logger.info("Bot is now running and waiting for messages...")
            self.app.run_polling()
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
    
    def stop(self):
        """Stop the bot gracefully"""
        logger.info("Stopping bot...")
        self.app.stop()
