from base import EconomyBot

import discord

from discord.ext import commands


class Shop(commands.Cog):
    def __init__(self, client: EconomyBot):
        self.client = client
        self.inv = self.client.db.inv

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def shop(self, ctx):
        user = ctx.author
        await self.inv.open_acc(user)

        em = discord.Embed(
            title="Shop",
            color=discord.Color.green()
        )
        x = 1
        for item in self.inv.shop_items:
            name = item["name"]
            cost = item["cost"]
            item_id = item["id"]
            item_info = item["info"]

            x += 1
            if x > 1:
                em.add_field(name=f"{name.upper()} -- {cost:,}",
                             value=f"{item_info}\nID: `{item_id}`", inline=False)

        await ctx.reply(embed=em, mention_author=False)

    @shop.command(usage="<item_name*: string>")
    @commands.guild_only()
    async def info(self, ctx, *, item_name: str):
        user = ctx.author
        for item in self.inv.shop_items:
            name = item["name"]
            cost = item["cost"]
            item_info = item["info"]

            if name.lower() == item_name.lower():
                em = discord.Embed(
                    description=item_info,
                    title=f"{name.upper()}",
                    color=discord.Color.blue()
                )

                sell_amt = int(cost / 4)

                em.add_field(name="Buying price", value=f"`{cost:,}`", inline=False)
                em.add_field(name="Selling price",
                             value=f"`{sell_amt:,}`", inline=False)

                return await ctx.reply(embed=em, mention_author=False)

        embed = discord.Embed(
            title="Error ❌",
            description=f"There's no item named `{item_name}`.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed, mention_author=False)


# if you are using 'discord.py >=v2.0' comment(remove) below code
def setup(client):
    client.add_cog(Shop(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Shop(client))
