"""
Main bot class that handles the Telegram bot initialization and management.
"""

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
from handlers import BotHandlers
from utils import Utils

logger = logging.getLogger(__name__)

class TelegramBot:
    """Main Telegram bot class."""
    
    def __init__(self):
        """Initialize the bot with configuration."""
        self.config = Config()
        self.handlers = BotHandlers()
        self.utils = Utils()
        self.application = None
        
    async def start(self):
        """Start the Telegram bot."""
        try:
            # Create application
            self.application = Application.builder().token(self.config.bot_token).build()
            
            # Add command handlers
            self.application.add_handler(CommandHandler("start", self.handlers.start_command))
            self.application.add_handler(CommandHandler("help", self.handlers.help_command))
            
            # Add message handler for text messages
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message)
            )
            
            # Add error handler
            self.application.add_error_handler(self.handlers.error_handler)
            
            logger.info("Bot is starting...")
            
            # Start the bot
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            logger.info("Bot is running! Press Ctrl+C to stop.")
            
            # Keep the bot running
            await self.application.updater.idle()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
        finally:
            if self.application:
                await self.application.stop()
                await self.application.shutdown()
