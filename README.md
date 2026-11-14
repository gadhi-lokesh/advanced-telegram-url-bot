
# Advanced Telegram URL Shortener Bot

A Python-based Telegram bot that converts long URLs into
short, shareable links using multiple public URL-shortening
APIs with automatic fallback.

## Features

- Shorten URLs directly through Telegram
- Multiple public URL-shortening APIs
- Automatic fallback when an API fails
- URL validation and error handling
- SQLite database for URL history
- Personal URL statistics
- Asynchronous Telegram bot handlers
- Secure token management with environment variables

## Tech Stack

- Python 3
- python-telegram-bot
- Requests
- SQLite
- REST APIs
- python-dotenv

## Project Structure

advanced-telegram-url-bot/
├── bot.py
├── config.py
├── database.py
├── url_shortener.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## How It Works

1. A user sends a long URL to the Telegram bot.
2. The bot validates the URL.
3. The API manager contacts a URL-shortening service.
4. If a provider fails, the next provider is tried.
5. A successful short URL is saved in SQLite.
6. The bot returns the shortened URL to the user.

## Installation

### 1. Clone the repository

git clone https://github.com/gadhi-lokesh/advanced-telegram-url-bot.git

cd advanced-telegram-url-bot

### 2. Create a virtual environment

python3 -m venv venv

source venv/bin/activate

### 3. Install dependencies

python -m pip install -r requirements.txt

### 4. Configure the bot token

Copy .env.example to .env:

cp .env.example .env

Get your token from @BotFather on Telegram and
replace the placeholder in .env.

### 5. Run the bot

python bot.py

## Telegram Commands

| Command | Description |
|---------|-------------|
| /start | Start the bot |
| /help | Display instructions |
| /shorten URL | Shorten a URL |
| /history | Show recent shortened URLs |
| /stats | Show URL statistics |

## API Integration

The bot supports multiple URL-shortening providers:

- is.gd
- v.gd
- CleanURI

If a service fails, the bot automatically tries another.

External API availability and usage limits may change.

## Security

- Bot tokens are stored in environment variables.
- .env files are excluded from Git.
- SQLite database files are not uploaded.
- URLs are validated before shortening.

Do not shorten sensitive or private URLs because
external providers receive the submitted destinations.

## Future Improvements

- QR code generation
- Interactive Telegram buttons
- Analytics dashboard
- Admin panel
- Cloud deployment

## License

See the LICENSE file for license terms.
