#!/usr/bin/env python3
"""
Main entry point for the Telegram Translation Bot
"""
import logging
import signal
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

try:
    from flask import Flask
    from threading import Thread

    app = Flask('')

    @app.route('/')
    def home():
        return "Bot está online!"

    def run():
        print("Servidor Flask iniciado na porta 8080")
        app.run(host='0.0.0.0', port=8080)

    t = Thread(target=run)
    t.start()

    logger.info("Keep-alive service started successfully")
except ImportError:
    logger.info("Keep-alive service disabled (Flask not available - this is optional for bot functionality)")
except Exception as e:
    logger.info(f"Keep-alive service disabled ({e})")

from translator_bot import TranslatorBot
from config import BOT_TOKEN

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
