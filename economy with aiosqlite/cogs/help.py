import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, category: str = None):
        if category is None:
            embed = discord.Embed(
                title="Help",
                description="Here are the available command categories. Use `!help <category>` to see the commands in that category.",
                color=discord.Color.blue()
            )
            for cog_name, cog in self.client.cogs.items():
                if cog_name not in ["Events", "Help"]:
                    embed.add_field(name=cog_name, value=cog.description or "No description", inline=False)
            await ctx.send(embed=embed)
        else:
            cog = self.client.get_cog(category.capitalize())
            if cog is None:
                await ctx.send(f"No category named `{category}` found.")
                return

            embed = discord.Embed(
                title=f"{cog.qualified_name} Commands",
                description=cog.description or "No description",
                color=discord.Color.blue()
            )
            for command in cog.get_commands():
                embed.add_field(name=f"`!{command.name}`", value=command.help or "No description", inline=False)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
