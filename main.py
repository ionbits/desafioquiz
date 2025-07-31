#!/usr/bin/env python3
"""
Main entry point for the Telegram Translation Bot
"""
import logging
import signal
import sys
from translator_bot import TranslatorBot
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global bot instance
bot_instance = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down...")
    if bot_instance:
        bot_instance.stop()
    sys.exit(0)

def main():
    """Main function to run the translation bot"""
    global bot_instance
    
    try:
        # Validate bot token
        if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("Bot token not configured. Please set BOT_TOKEN environment variable.")
            sys.exit(1)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Create and start the bot
        logger.info("Initializing Telegram Translation Bot...")
        bot_instance = TranslatorBot(BOT_TOKEN)
        
        logger.info("Bot initialized successfully!")
        logger.info("The bot will automatically translate messages between Portuguese and English.")
        logger.info("Send any text message to the bot to see it in action!")
        logger.info("Press Ctrl+C to stop the bot.")
        
        # Start the bot
        bot_instance.run()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        if bot_instance:
            bot_instance.stop()
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    main()
