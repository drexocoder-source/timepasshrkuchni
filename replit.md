# DazaiRobot - Telegram Bot

## Overview
DazaiRobot is a feature-rich Telegram group management bot built with Python. It uses python-telegram-bot, Pyrogram, and Telethon libraries to provide moderation, fun commands, anime lookups, and more.

## Project Architecture
- **Language**: Python 3.10
- **Entry Point**: `python -m DazaiRobot`
- **Main Package**: `DazaiRobot/`
  - `__init__.py` - Bot initialization, config loading, client setup
  - `__main__.py` - Main bot loop, command handlers
  - `config.py` - Development config class
  - `modules/` - Bot command modules (admin, bans, fun, etc.)
  - `modules/sql/` - SQLAlchemy database models
  - `modules/mongo/` - MongoDB models
  - `modules/helper_funcs/` - Utility functions
- **Database**: PostgreSQL (via DATABASE_URL env var) + MongoDB (optional, via MONGO_DB_URI)
- **Dependencies**: Listed in `requirements.txt`

## Required Environment Variables (Secrets)
- `TOKEN` - Telegram Bot Token from @BotFather
- `API_ID` - Telegram API ID from my.telegram.org
- `API_HASH` - Telegram API Hash from my.telegram.org
- `OWNER_ID` - Telegram user ID of the bot owner
- `DATABASE_URL` - PostgreSQL connection string (auto-provided by Replit)
- `ENV` - Set to "True" (already configured)

## Optional Environment Variables
- `MONGO_DB_URI` - MongoDB connection string
- `SUPPORT_CHAT` - Support chat username
- `EVENT_LOGS` - Event log channel ID
- `CASH_API_KEY` - Currency API key
- `TIME_API_KEY` - Time API key

## Workflow
- **DazaiRobot**: Runs `python -m DazaiRobot` (console output)

## Recent Changes
- 2026-02-14: Initial Replit setup - installed Python 3.10, dependencies, PostgreSQL database, configured workflow
