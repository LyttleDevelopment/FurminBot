import asyncio
import os
import subprocess
from discord.ext import commands
from utils.logger import main_log


async def update(bot: commands.Bot):
    print("Updating bot..")
    output = await execute(
        "ssh-agent bash -c 'ssh-add $HOME/.ssh/id_ed25519; git fetch; git pull'"
    )
    print(output)
    await main_log(bot, f"> **<@{bot.user.id}> MAIN:** ```{output}```")
    await clean_exit(bot)


async def get_head() -> str:
    output = await execute("git --no-pager log --decorate=short --pretty=oneline -n1")
    return output[1]


async def clean_exit(bot: commands.Bot):
    print("Shutting down...")
    await main_log(bot, f"> **<@{bot.user.id}> MAIN:** Shutting down...")
    await bot.close()


async def execute(command):
    p = subprocess.Popen(
        command,
        cwd=os.getcwd(),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    while p.poll() is None:
        await asyncio.sleep(1)

    out, error = p.communicate()
    return p.returncode, out.decode("utf-8").strip(), error.decode("utf-8").strip()
