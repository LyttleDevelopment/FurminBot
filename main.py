import os
from typing import List

import discord
from discord.ext import commands
from utils.config import config
from utils.environments import is_production

print("MAIN: Bot starting, please wait!")

intents = discord.Intents().default()
intents.members = True

client: commands.Bot = commands.Bot(command_prefix='.fb', intents=intents)
client.remove_command('help')


def try_cog_action(function):
    try:
        function()
        return True, None
    except Exception as e:
        return False, e


# Actions when bot loaded
@client.event
async def on_ready():
    logs_channel = client.get_channel(856832351245828116)
    await logs_channel.send(f"\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_"
                            f"\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_")
    await logs_channel.send(f"> **<@{client.user.id}> MAIN:** Bot starting, please wait!")
    await logs_channel.send(f"> **<@{client.user.id}> MAIN:** Production: {str(prod)}")
    # Process loading.
    print("MAIN: Loading cogs...")
    await logs_channel.send(f"> **<@{client.user.id}> MAIN:** Loading cogs...")
    # Set values for loading cogs.
    total_successful_loads = 0
    total_cumulative_files = 0
    # Load cogs.
    for cog_folder in cog_folders:
        successful_loads, total_files = cog_loader(cog_folder)
        # Prints:
        print(
            f"COGS: cogs.{cog_folder} - {successful_loads}/{total_files} succeeded."
        )
        await logs_channel.send(f"> **<@{client.user.id}> COGS:** cogs.{cog_folder} - {successful_loads}/{total_files} succeeded.")
        total_successful_loads += successful_loads
        total_cumulative_files += total_files
    # Final messages.
    print(f"COGS: Successfully loaded {total_successful_loads}/{total_cumulative_files} cogs.")
    print("MAIN: Cogs loaded, bot is active!")
    await logs_channel.send(f"> **<@{client.user.id}> COGS:** Successfully loaded {total_successful_loads}/{total_cumulative_files} cogs.")
    await logs_channel.send(f"> **<@{client.user.id}> MAIN:** Cogs loaded, bot is active <@132487290835435521>!")


# Cog folders currently active.
cog_folders: List[str] = ["core", "development", "presence", "actions", "commands"]


def cog_loader(folder: str):
    files: List[str] = os.listdir(f'cogs/{folder}')
    files = list(filter(lambda f: f.endswith('.py'), files))
    successful_loads = 0

    for filename in files:
        cog_name = f"cog.{folder}.{filename[:-3]}"

        try:
            client.load_extension(f'cogs.{folder}.{filename[:-3]}')
            print(f"COGS: Loaded \"{cog_name}\"")
            successful_loads += 1
        except Exception as e:
            print(f"ERROR loading extension {cog_name}:\n{e}")

    return successful_loads, len(files)


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
