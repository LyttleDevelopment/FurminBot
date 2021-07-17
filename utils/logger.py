from discord.ext import commands
from utils.config import config

# logger Version:
version = "1.0"


async def log_helper(client: commands.Bot, target: int, log_message: str):
    guild = client.get_guild(config.admin_guild)
    logs_channel = guild.get_channel(target)
    await logs_channel.send(log_message)


async def log(client: commands.Bot, log_message):
    await log_helper(client, config.log_channel, log_message)
    await log_helper(client, config.advanced_logs, log_message)


async def advanced_log(client: commands.Bot, log_message):
    await log_helper(client, config.advanced_logs, log_message)


async def error_log(client: commands.Bot, log_message):
    await log_helper(client, config.error_channel, log_message)


async def main_log(client: commands.Bot, log_message):
    await log_helper(client, config.main_logs, log_message)
    await log_helper(client, config.log_channel, log_message)
    await log_helper(client, config.advanced_logs, log_message)
