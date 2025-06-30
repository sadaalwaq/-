#!/usr/bin/env python3
"""
Main entry point for the Telegram bot application.
This file initializes and starts the bot.
"""

import asyncio
import logging
import sys
from bot import TelegramBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the Telegram bot."""
    try:
        # Initialize and start the bot
        bot = TelegramBot()
        await bot.start()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
