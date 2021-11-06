from __future__ import print_function, unicode_literals, division, absolute_import

__metaclass__ = type
__package_name__ = "franky"
__code_name__ = __package_name__
__code_desc__ = """ program description to be displayed by argparse \n    ex: python {name}
    """.format(
    name=str(__code_name__) + ".py"
)
__code_version__ = "v0.0.1"
__code_debug__ = False

## Standard Libraries
import os
import logging

## Third Party libraries
import discord
from discord.ext import commands
from discord_slash import SlashCommand


def begin_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(style="{", fmt="[{name}:{filename}] {levelname} - {message}")
    )
    log = logging.getLogger(__package_name__)
    log.setLevel(logging.INFO)
    log.addHandler(handler)

    return log


def main():
    logger = begin_logging()

    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if DISCORD_TOKEN is None:
        raise SystemExit("DISCORD_TOKEN missing from environment.")

    # Expects a comma-seperated list of guild ids
    DISCORD_GUILDS = os.getenv("DISCORD_GUILDS")
    if DISCORD_GUILDS is None:
        raise SystemExit("DISCORD_GUILDS missing from environment.")

    bot = commands.Bot(command_prefix="!")
    slash = SlashCommand(
        bot, sync_commands=True
    )  # Declares slash commands through the client.

    @bot.event
    async def on_ready():
        logger.info("ready")

    # Register commands to these servers
    guild_ids = list(map(int, DISCORD_GUILDS.split(",")))

    # Defines a new "context" (ctx) command called "ping."
    @slash.slash(name="ping", guild_ids=guild_ids)
    async def _ping(ctx):
        await ctx.send(f"Pong!!!!! ({bot.latency*1000}ms)")

    # Run client and spawn http server
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
