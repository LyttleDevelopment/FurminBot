import os
from typing import List

import discord
from discord.ext import commands
from utils.config import config
from utils.environments import is_production
from utils.shortcuts import line
from utils.logger import main_log

print("MAIN: Bot starting, please wait!")

intents = discord.Intents.all()

client: commands.Bot = commands.Bot(command_prefix="!f ", intents=intents)
client.remove_command("help")



def try_cog_action(function):
    try:
        function()
        return True, None
    except Exception as e:
        return False, e


# Actions when bot loaded
@client.event
async def on_ready():
    # Set status to booting.
    await client.change_presence(
        status=discord.Status.dnd, activity=discord.Activity(name="booting...", type=5)
    )

    # Reset log grouping messages.
    log_print = [
        f"{line}",
        f"> **<@{client.user.id}> MAIN:** Bot starting, please wait!",
        f"> **<@{client.user.id}> MAIN:** Production: {str(prod)}",
    ]

    # Start loading cogs.
    print("MAIN: Loading cogs...")
    log_print.append(f"> **<@{client.user.id}> MAIN:** Loading cogs...")

    # Merge messages and send to log channel.
    log_message = "\n".join(map(str, log_print))
    await main_log(client, log_message)

    # Reset log grouping messages.
    log_print = []

    # Set values for loading cogs.
    total_successful_loads = 0
    total_cumulative_files = 0

    # Load cogs.
    for cog_folder in cog_folders:
        successful_loads, total_files, status = cog_loader(cog_folder)
        # Prints:
        print(f"COGS: cogs.{cog_folder} - {successful_loads}/{total_files} succeeded.")
        log_print.append(
            f"> **<@{client.user.id}> COGS:** ***cogs.{cog_folder} - {successful_loads}/{total_files} succeeded.***"
        )
        status = "\n".join(map(str, status))
        log_print.append(f"{status}")
        total_successful_loads += successful_loads
        total_cumulative_files += total_files

    # Merge messages and send to log channel.
    log_message = "\n".join(map(str, log_print))
    await main_log(client, log_message)

    # Print ready state.
    print(
        f"COGS: Successfully loaded {total_successful_loads}/{total_cumulative_files} cogs."
    )
    print("MAIN: Cogs loaded, bot is active!")

    # Reset log grouping messages.
    log_print = [
        f"> **<@{client.user.id}> COGS:** Successfully loaded {total_successful_loads}/{total_cumulative_files} cogs.",
        f"> **<@{client.user.id}> MAIN:** Cogs loaded, bot is active!",
    ]

    # Merge messages and send to log channel.
    log_message = "\n".join(map(str, log_print))
    await main_log(client, log_message)


# Cog folders currently active.
cog_folders: List[str] = ["core", "development", "presence", "actions", "commands"]


def cog_loader(folder: str):
    files: List[str] = os.listdir(f"./cogs/{folder}")
    files = list(filter(lambda f: f.endswith(".py"), files))
    successful_loads = 0
    status = []

    for filename in files:
        cog_name = f"cog.{folder}.{filename[:-3]}"

        try:
            client.load_extension(f"cogs.{folder}.{filename[:-3]}")
            print(f'COGS: Loaded "{cog_name}"')
            status.append(f'> **<@{client.user.id}> COGS:** Loaded "{cog_name}"')
            successful_loads += 1
        except Exception as e:
            print(f"ERHR: ERROR loading extension {cog_name}:\n{e}")
            status.append(
                f"> **<@{client.user.id}> ERHR:** ERROR loading extension {cog_name}:\n```{e}```"
            )

    return successful_loads, len(files), status


@client.command()
async def load(ctx, extension):
    if extension is None:
        await ctx.send("You have to specify an extension to load")
        return
    success, error = try_cog_action(lambda: client.load_extension(f'cogs.{extension}'))
    if success:
        print(f'COGS: Loaded "cogs.{extension}"')
        await ctx.send(
            f'Success! <a:green_circle:832697262118535199> **Loaded "cogs.{extension}"** *(took: {round(client.latency * 1000)}ms)*')
    else:
        text = f"There was an error loading \"cogs.{extension}\".\nException: ```\n{error}\n```"
        print(text)
        await ctx.send(text)


@client.command()
async def unload(ctx, extension):
    if extension is None:
        await ctx.send("You have to specify an extension to unload")
        return
    success, error = try_cog_action(lambda: client.unload_extension(f'cogs.{extension}'))
    if success:
        print(f'COGS: Unloaded "cogs.{extension}"')
        await ctx.send(
            f'Success! <a:red_circle:833343241617276969> **Unloaded "cogs.{extension}"** *(took: {round(client.latency * 1000)}ms)*')
    else:
        text = f"There was an error unloading \"cogs.{extension}\".\nException: ```\n{error}\n```"
        print(text)
        await ctx.send(text)


@client.command()
async def reload(ctx, extension):
    if extension is None:
        await ctx.send("You have to specify an extension to load")
        return
    success, error = try_cog_action(lambda: client.unload_extension(f'cogs.{extension}')), (
        lambda: client.load_extension(f'cogs.{extension}'))
    if success:
        print(f'COGS: Loaded "cogs.{extension}"')
        await ctx.send(
            f'Success! <a:orange_circle:833401546112237598> **Reloaded "cogs.{extension}"** *(took: {round(client.latency * 1000)}ms)*')
    else:
        text = f"There was an error reloading \"cogs.{extension}\".\nException: ```\n{error}\n```"
        print(text)
        await ctx.send(text)

if __name__ == "__main__":
    prod: bool = is_production()
    print("MAIN: Production: " + str(prod))

    if prod:
        client.run(config.prod_token)
    else:
        client.run(config.dev_token)
