"""
Note
-----
If your bot is not intended for public use and is only meant to be used on one or two servers that you own,
you can add these commands.

However, if your bot is publicly available for anyone to add to their server,
it is not recommended to include these commands.
"""

from base import EconomyBot

import discord

from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client: EconomyBot):
        self.client = client
        self.bank = self.client.db.bank
        self.inv = self.client.db.inv

    @commands.command(aliases=["addmoney"], usage="<member*: @member> <amount*: integer> <mode: wallet or bank>")
    @commands.is_owner()
    @commands.cooldown(3, 2 * 60, commands.BucketType.user)
    async def add_money(self, ctx, member: discord.Member, amount: str, mode: str = "wallet"):
        mode = mode.lower()
        if member.bot:
            embed = discord.Embed(
                title="Error ❌",
                description="You can't add money to a bot.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        if not amount.isdigit() or int(amount) <= 0:
            embed = discord.Embed(
                title="Error ❌",
                description="Please enter a valid amount.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        if mode not in ["wallet", "bank"]:
            embed = discord.Embed(
                title="Error ❌",
                description="Please enter either wallet or bank only.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        limit = 100_000
        amount = int(amount)
        if amount > limit:
            embed = discord.Embed(
                title="Error ❌",
                description=f"You cannot add money more than {limit:,}.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        await self.bank.open_acc(member)
        await self.bank.update_acc(member, +amount, mode)

        embed = discord.Embed(
            title="Success ✅",
            description=f"You added `{amount:,}` in {member.mention}'s {mode}.",
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["remoney"], usage="<member*: @member> <amount*: integer> <mode: wallet or bank>")
    @commands.is_owner()
    @commands.cooldown(3, 2 * 60, commands.BucketType.user)
    async def remove_money(self, ctx, member: discord.Member, amount: str, mode: str = "wallet"):
        mode = mode.lower()
        if member.bot:
            embed = discord.Embed(
                title="Error ❌",
                description="You can't remove money from a bot.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        if not amount.isdigit() or int(amount) <= 0:
            embed = discord.Embed(
                title="Error ❌",
                description="Please enter a valid amount.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        if mode not in ["wallet", "bank"]:
            embed = discord.Embed(
                title="Error ❌",
                description="Please enter either wallet or bank only.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        amount = int(amount)
        await self.bank.open_acc(member)

        users = await self.bank.get_acc(member)
        user_amt = users[2 if mode == "bank" else 1]
        if user_amt < amount:
            embed = discord.Embed(
                title="Error ❌",
                description=f"You can only remove `{user_amt:,}` from {member.mention}'s {mode}.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        await self.bank.update_acc(member, -amount, mode)

        embed = discord.Embed(
            title="Success ✅",
            description=f"You removed `{amount:,}` from {member.mention}'s {mode}.",
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage="<member*: @member>")
    @commands.is_owner()
    @commands.cooldown(2, 3 * 60, commands.BucketType.user)
    async def reset_user(self, ctx, member: discord.Member):
        if member.bot:
            embed = discord.Embed(
                title="Error ❌",
                description="Bots don't have an account.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        users = await self.bank.get_acc(member)
        if users is None:
            await self.bank.open_acc(member)
        else:
            await self.bank.reset_acc(member)

        embed = discord.Embed(
            title="Success ✅",
            description=f"{member.mention}'s account has been reset.",
            color=discord.Color.green()
        )
        return await ctx.reply(embed=embed, mention_author=False)


# if you are using 'discord.py >=v2.0' comment(remove) below code
def setup(client):
    client.add_cog(Admin(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Admin(client))
