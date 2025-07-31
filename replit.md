# Telegram Translation Bot

## Overview

This is a Telegram bot that automatically translates messages between Portuguese and English. The bot detects the language of incoming text messages and translates them to the opposite language (Portuguese to English or English to Portuguese). It uses Google Translate API through the `deep-translator` library and language detection via `langdetect`.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (July 31, 2025)

- ✅ Implemented personalized translation messages using user's first name
- ✅ Fixed language detection issues with improved keyword matching
- ✅ Added robust error handling for message processing
- ✅ Customized response format: "[Name] disse:" for PT→EN, "[Name] said:" for EN→PT
- ✅ Enhanced Portuguese and English word detection for better accuracy

## System Architecture

The application follows a simple modular architecture with clear separation of concerns:

- **main.py**: Entry point and application lifecycle management
- **translator_bot.py**: Core bot logic and Telegram integration
- **utils.py**: Translation and language detection utilities
- **config.py**: Centralized configuration management

The architecture is designed for simplicity and maintainability, with each module having a specific responsibility.

## Key Components

### Bot Engine (translator_bot.py)
- **Purpose**: Handles Telegram bot interactions and message processing
- **Technology**: Python Telegram Bot library
- **Key Features**: Message handling, bot lifecycle management
- **Design Decision**: Uses class-based approach for better state management and extensibility

### Translation Engine (utils.py)
- **Purpose**: Provides language detection and translation capabilities
- **Technology**: `langdetect` for detection, `deep-translator` with Google Translate
- **Key Features**: Automatic language detection, bidirectional translation
- **Design Decision**: Separated from bot logic to allow for easy testing and potential replacement of translation services

### Configuration Management (config.py)
- **Purpose**: Centralized configuration and constants
- **Key Features**: Environment variable handling, language codes, error messages
- **Design Decision**: Externalized configuration for easy deployment and localization

### Application Bootstrap (main.py)
- **Purpose**: Application entry point and process management
- **Key Features**: Signal handling, graceful shutdown, error handling
- **Design Decision**: Separated bootstrap logic for clean application lifecycle management

## Data Flow

1. **Message Reception**: Bot receives text messages from Telegram users
2. **Language Detection**: System detects the language of the incoming message using `langdetect`
3. **Language Validation**: Checks if the detected language is supported (Portuguese or English)
4. **Translation**: Uses Google Translate via `deep-translator` to translate to the target language
5. **Response Formatting**: Formats the response with appropriate flag emojis and headers
6. **Message Delivery**: Sends the translated message back to the user

## External Dependencies

### Core Dependencies
- **python-telegram-bot**: Telegram Bot API integration
- **deep-translator**: Google Translate API wrapper
- **langdetect**: Language detection library

### Translation Service
- **Google Translate**: Primary translation service
- **Rationale**: Chosen for reliability, language support, and ease of integration
- **Alternative**: Could be replaced with other services through the translator interface

### Messaging Platform
- **Telegram Bot API**: Message delivery platform
- **Authentication**: Bot token-based authentication
- **Webhook vs Polling**: Currently uses polling (default behavior)

## Deployment Strategy

### Environment Configuration
- **Bot Token**: Configured via `BOT_TOKEN` environment variable
- **Default Fallback**: Includes hardcoded token for development (should be removed for production)
- **Logging**: Structured logging with configurable levels

### Process Management
- **Signal Handling**: Graceful shutdown on SIGINT/SIGTERM
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Monitoring**: Structured logging for operational visibility

### Scalability Considerations
- **Stateless Design**: Bot doesn't maintain user state, allowing for horizontal scaling
- **API Limits**: Relies on Google Translate rate limits and Telegram Bot API limits
- **Memory Usage**: Minimal memory footprint due to stateless operation

### Security Considerations
- **Token Management**: Bot token should be secured via environment variables
- **Input Validation**: Basic text validation and error handling
- **API Security**: Relies on HTTPS for API communications