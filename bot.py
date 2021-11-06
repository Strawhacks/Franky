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
import sys
import argparse
import logging
from pprint import pprint  # , pformat

## Third Party libraries
import discord
from discord_slash import SlashCommand

## Modules
try:
    from .classes import RequestHandler
    from .classes import ThreadedServer
except ImportError:
    # If we can't import modules, probably running from VSCODE
    # attempt to hack in modules
    import importlib
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    RequestHandler = importlib.import_module(__package_name__+'.classes.RequestHandler')
    ThreadedServer = importlib.import_module(__package_name__+'.classes.ThreadedServer')


def begin_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(style="{", fmt="[{name}:{filename}] {levelname} - {message}")
    )
    log = logging.getLogger(__package_name__)
    log.setLevel(logging.INFO)
    log.addHandler(handler)


def collect_args():
    parser = argparse.ArgumentParser(
        description=__code_desc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-V", "--version", action="version", version=__code_version__)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()
    return parser, args


def handle_args():
    # collect parser if needed to conditionally call usage: parser.print_help()
    parser, args = collect_args()
    return args


def main():
    begin_logging()
    args = handle_args()

    BIND = '0.0.0.0'
    PORT = 8000
    server = ThreadedServer.ThreadedServer((BIND, PORT), RequestHandler)
    while True:
        try:
            DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
            if DISCORD_TOKEN is None:
                raise SystemExit("DISCORD_TOKEN missing from environment.")

            # Expects a comma-seperated list of guild ids
            DISCORD_GUILDS = os.getenv("DISCORD_GUILDS")
            if DISCORD_GUILDS is None:
                raise SystemExit("DISCORD_GUILDS missing from environment.")

            client = discord.Client(intents=discord.Intents.default())
            slash = SlashCommand(
                client, sync_commands=True
            )  # Declares slash commands through the client.

            @client.event
            async def on_ready():
                print("Ready!")

            # Register commands to these servers
            guild_ids = DISCORD_GUILDS.split(",")

            # Defines a new "context" (ctx) command called "ping."
            @slash.slash(name="ping", guild_ids=guild_ids)
            async def _ping(ctx):
                await ctx.send(f"Pong! ({client.latency*1000}ms)")

            # Run client and spawn http server
            client.run(DISCORD_TOKEN)
            try:
                server.handle_request()
            except KeyboardInterrupt:
                break

        except Exception as e:
            pprint(e)
            raise e
        finally:
            pass


if __name__ == "__main__":
    main()
