from base import EconomyBot

import discord

from datetime import datetime
from discord.ext import commands


class MainBank(commands.Cog):
    def __init__(self, client: EconomyBot):
        self.client = client
        self.bank = self.client.db.bank

    @commands.command(aliases=["bal"], usage=f"<member: @member>")
    @commands.guild_only()
    async def balance(self, ctx, member: discord.Member = None):
        user = member or ctx.author
        user_av = user.display_avatar or user.default_avatar
        if user.bot:
            embed = discord.Embed(
                title="Error ❌",
                description="Bots don't have an account.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        await self.bank.open_acc(user)

        users = await self.bank.get_acc(user)
        wallet_amt = users[1]
        bank_amt = users[2]
        net_amt = int(wallet_amt + bank_amt)

        em = discord.Embed(
            description=f"**Wallet:** `{wallet_amt:,}`\n"
                        f"**Bank:** `{bank_amt:,}`\n"
                        f"**Net:** `{net_amt:,}`",
            color=discord.Color.green()
        )
        em.set_author(name=f"{user.name}'s Balance", icon_url=user_av.url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["with"], usage="<amount*: integer or all>")
    @commands.guild_only()
    async def withdraw(self, ctx, amount: str):
        user = ctx.author
        await self.bank.open_acc(user)

        users = await self.bank.get_acc(user)
        bank_amt = users[2]

        if amount.lower() == "all" or amount.lower() == "max":
            await self.bank.update_acc(user, +1 * bank_amt)
            await self.bank.update_acc(user, -1 * bank_amt, "bank")
            embed = discord.Embed(
                title="Success ✅",
                description=f"You withdrew `{bank_amt:,}` in your wallet.",
                color=discord.Color.green()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        amount = int(amount)
        if amount > bank_amt:
            embed = discord.Embed(
                title="Error ❌",
                description="You don't have that much money!",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        if amount < 0:
            embed = discord.Embed(
                title="Error ❌",
                description="Enter a valid amount!",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        await self.bank.update_acc(user, +amount)
        await self.bank.update_acc(user, -amount, "bank")
        embed = discord.Embed(
            title="Success ✅",
            description=f"You withdrew `{amount:,}` from your bank.",
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["dep"], usage="<amount*: integer or all>")
    @commands.guild_only()
    async def deposit(self, ctx, amount: str):
        user = ctx.author
        await self.bank.open_acc(user)

        users = await self.bank.get_acc(user)
        wallet_amt = users[1]
        if amount.lower() == "all" or amount.lower() == "max":
            await self.bank.update_acc(user, -wallet_amt)
            await self.bank.update_acc(user, +wallet_amt, "bank")
            embed = discord.Embed(
                title="Success ✅",
                description=f"You deposited `{wallet_amt:,}` in your bank.",
                color=discord.Color.green()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        amount = int(amount)
        if amount > wallet_amt:
            embed = discord.Embed(
                title="Error ❌",
                description="You don't have that much money!",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        if amount < 0:
            embed = discord.Embed(
                title="Error ❌",
                description="Enter a valid amount!",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        await self.bank.update_acc(user, -amount)
        await self.bank.update_acc(user, +amount, "bank")
        embed = discord.Embed(
            title="Success ✅",
            description=f"You deposited `{amount:,}` in your bank.",
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage="<member*: @member> <amount*: integer>")
    @commands.guild_only()
    async def send(self, ctx, member: discord.Member, amount: int):
        user = ctx.author
        if member.bot:
            embed = discord.Embed(
                title="Error ❌",
                description="Bots don't have an account.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        await self.bank.open_acc(user)
        await self.bank.open_acc(member)

        users = await self.bank.get_acc(user)
        wallet_amt = users[1]
        if amount <= 0:
            embed = discord.Embed(
                title="Error ❌",
                description="Enter a valid amount!",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)
        if amount > wallet_amt:
            embed = discord.Embed(
                title="Error ❌",
                description="You don't have enough amount.",
                color=discord.Color.red()
            )
            return await ctx.reply(embed=embed, mention_author=False)

        await self.bank.update_acc(user, -amount)
        await self.bank.update_acc(member, +amount)
        embed = discord.Embed(
            title="Success ✅",
            description=f"You sent `{amount:,}` to {member.mention}.",
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["lb"])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        users = await self.bank.get_networth_lb()

        data = []
        index = 1
        for member in users:
            if index > 10:
                break

            member_name = self.client.get_user(member[0])
            member_amt = member[1]

            if index == 1:
                msg1 = f"**🥇 `{member_name}` -- {member_amt}**"
                data.append(msg1)
            if index == 2:
                msg2 = f"**🥈 `{member_name}` -- {member_amt}**"
                data.append(msg2)
            if index == 3:
                msg3 = f"**🥉 `{member_name}` -- {member_amt}**\n"
                data.append(msg3)
            if index >= 4:
                members = f"**{index} `{member_name}` -- {member_amt}**"
                data.append(members)
            index += 1

        msg = "\n".join(data)

        em = discord.Embed(
            title=f"Top {index - 1} Richest Users - Leaderboard",
            description=f"It's Based on Net Worth (wallet + bank) of Global Users\n\n{msg}",
            color=discord.Color(0x00ff00),
            timestamp=datetime.utcnow()
        )
        em.set_footer(text=f"GLOBAL - {ctx.guild.name}")
        await ctx.reply(embed=em, mention_author=False)


# if you are using 'discord.py >=v2.0' comment(remove) below code
def setup(client):
    client.add_cog(MainBank(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(MainBank(client))
