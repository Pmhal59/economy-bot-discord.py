from base import EconomyBot, Auth

import discord

intents = discord.Intents.all()
client = EconomyBot(command_prefix=Auth.COMMAND_PREFIX, intents=intents, help_command=None)

if __name__ == "__main__":
    # Make sure to add Bot Token in '.env' file
    client.load_extension("cogs.help")
    client.run(Auth.TOKEN)
