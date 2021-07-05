from discord.ext import commands

from utils.utils import execute, clean_exit


async def update(bot: commands.Bot):
    print("Updating...")
    output = await execute([
        "git pull origin main"
    ])
    print("output:" + "\n".join(output[1].split("\\n")))
    await clean_exit(bot)


async def get_head() -> str:
    output = await execute(["git --no-pager log --decorate=short --pretty=oneline -n1"])
    return output[1]
