import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

def _safe_int(value: str | None) -> int | None:
    """Return int(value) if possible, else None."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

# Get values from .env (robust parsing)
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = _safe_int(os.getenv('GUILD_ID'))
MEMBER_ROLE_ID = _safe_int(os.getenv('MEMBER_ROLE_ID'))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

# Enable member intent
intents = discord.Intents.default()
intents.members = True  # Required for on_member_join
intents.message_content = True  # Enable to avoid message content warning
bot = commands.Bot(command_prefix="!", intents=intents)

# Set presence when bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="for new members 👀",
        ),
    )
    logging.info(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info("👀 Presence set to: Watching for new members")
    
    # Start keep-alive task
    asyncio.create_task(keep_alive())

# Auto-assign role and send DM on member join
@bot.event
async def on_member_join(member: discord.Member):
    # Prefer the guild from the member object
    guild = member.guild

    if GUILD_ID is not None and guild.id != GUILD_ID:
        # Ignore joins from other guilds if GUILD_ID is specified
        return

    # Resolve role safely
    role = None
    if MEMBER_ROLE_ID is not None:
        role = guild.get_role(MEMBER_ROLE_ID)
        if role is None:
            logging.warning(f"⚠️ Role with ID {MEMBER_ROLE_ID} not found in guild {guild.name}")

    # Try assigning the role
    if role is not None:
        try:
            await member.add_roles(role, reason="Auto-assign on join")
            logging.info(f"✅ Assigned role '{role.name}' to {member} in {guild.name}")
        except discord.Forbidden:
            logging.warning(f"⚠️ Missing permissions to assign role '{role.name}' to {member}")
        except discord.HTTPException as http_exc:
            logging.error(f"❌ Failed to assign role due to HTTP error: {http_exc}")

    # Build a clean embed for the welcome DM
    embed = discord.Embed(
        title="Welcome to AstraBoost! 🎉",
        description=(
            "We're excited to have you here.\n\n"
            "- Need help? Create a support ticket anytime.\n"
            "- Have questions? Our team is here for you.\n"
            "- Make yourself at home and enjoy your stay!"
        ),
        color=discord.Color.blurple(),
    )
    embed.set_footer(text="AstraBoost • We're here to help ✨")

    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        logging.warning(f"⚠️ Could not DM {member} (DMs closed)")
    except discord.HTTPException as http_exc:
        logging.error(f"❌ Failed to send DM due to HTTP error: {http_exc}")

    logging.info(f"👋 New member joined: {member} in {guild.name}")

# Keep-alive function to prevent Render from sleeping
async def keep_alive():
    """Send periodic logs to keep the service active"""
    while True:
        await asyncio.sleep(300)  # Every 5 minutes
        logging.info("🔄 Bot is alive and running...")

# Run the bot
if __name__ == "__main__":
    if BOT_TOKEN:
        try:
            logging.info("🚀 Starting AstraBoost bot...")
            bot.run(BOT_TOKEN)
        except Exception as e:
            logging.error(f"❌ Bot crashed: {e}")
            raise
    else:
        logging.error("❌ BOT_TOKEN is not set! Please check your environment variables.")
        exit(1)
