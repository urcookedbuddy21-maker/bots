# AstraBoost Discord Bot

A Discord bot that automatically assigns roles and sends welcome messages to new members.

## Features

- Auto-assigns roles when members join
- Sends beautiful embed welcome messages
- Configurable via environment variables
- Ready for deployment on Render

## Setup

1. Create a Discord application at https://discord.com/developers/applications
2. Create a bot and copy the token
3. Enable "Server Members Intent" in the Bot settings
4. Invite the bot to your server with appropriate permissions

## Environment Variables

- `BOT_TOKEN`: Your Discord bot token
- `GUILD_ID`: Your Discord server ID (optional, for single-server mode)
- `MEMBER_ROLE_ID`: Role ID to auto-assign to new members

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file:
   ```
   BOT_TOKEN=your_bot_token_here
   GUILD_ID=123456789012345678
   MEMBER_ROLE_ID=123456789012345678
   ```

3. Run the bot:
   ```bash
   python main.py
   ```

## Deploy on Render

1. Push this code to a GitHub repository
2. Connect your GitHub repo to Render
3. Create a new "Background Worker" service
4. Set the environment variables in Render dashboard
5. Deploy!

The bot will automatically start and stay running on Render's free tier.
