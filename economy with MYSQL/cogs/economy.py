from base import EconomyBot

from numpy import random

import discord
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, client: EconomyBot):
        self.client = client
        self.bank = self.client.db.bank

    @commands.cooldown(1, 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def daily(self, ctx):
        user = ctx.author
        await self.bank.open_acc(user)

        rand_amt = random.randint(3000, 5000)
        await self.bank.update_acc(user, +rand_amt)

        embed = discord.Embed(
            title="**Daily Reward**",
            description=f"Congratulations {user.mention} 🎊, you have received `{rand_amt:,}` coins.",
            color=discord.Color.green()
        ).set_thumbnail(url=user.display_avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 7 * 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def weekly(self, ctx):
        user = ctx.author
        await self.bank.open_acc(user)

        rand_amt = random.randint(7000, 10000)
        await self.bank.update_acc(user, +rand_amt)

        embed = discord.Embed(
            title="**Weekly Reward**",
            description=f"Congratulations {user.mention} 🎊, you have received `{rand_amt:,}` coins.",
            color=discord.Color.green()
        ).set_thumbnail(url=user.display_avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 30 * 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def monthly(self, ctx):
        user = ctx.author
        await self.bank.open_acc(user)

        rand_amt = random.randint(30000, 50000)
        await self.bank.update_acc(user, +rand_amt)

        embed = discord.Embed(
            title="**Monthly Reward**",
            description=f"Congratulations {user.mention} 🎊, you have received `{rand_amt:,}` coins.",
            color=discord.Color.green()
        ).set_thumbnail(url=user.display_avatar.url)
        await ctx.reply(embed=embed, mention_author=False)


# if you are using 'discord.py >=v2.0' comment(remove) below code
def setup(client):
    client.add_cog(Economy(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Economy(client))
