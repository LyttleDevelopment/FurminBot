import asyncio
import os
import subprocess
from typing import List

from discord.ext import commands


async def execute(commands_to_execute: List[str]):
    p = subprocess.Popen(
        commands_to_execute,
        cwd=os.getcwd(),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    while p.poll() is None:
        await asyncio.sleep(1)

    out, error = p.communicate()
    return p.returncode, out.decode("utf-8").strip(), error.decode("utf-8").strip()


async def clean_exit(bot: commands.Bot):
    print("Shutting down...")
    await bot.logout()


def get_class_path(c) -> str:
    return c.__class__.__module__
