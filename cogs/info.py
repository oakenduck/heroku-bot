import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

from main import random_color
from snowflake import to_datetime as to_dt

from datetime import datetime

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """ Get bot latency. """
        embed = discord.Embed(
            title = 'Pong!',
            description = f"Latency is {round(self.client.latency * 1000, 3)}ms.",
            colour = random_color()
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def whois(self, ctx, mention_or_id=None):
        is_in_server = True
        if mention_or_id:
            member = await self.get_user(ctx, mention_or_id)
            if not member:
                return await ctx.send(f"❌ User `{mention_or_id}` not found.")

            is_in_server = member.id in [user.id for user in ctx.guild.members]

        else:
            member = ctx.author

        creation = to_dt(member.id)
        date = datetime.now() - creation

        embed = discord.Embed(
            title = str(member),
            description = f"Information on {member.name}.",
            colour = random_color()
        )

        embed.add_field(name="Account created", value=creation.strftime("%d/%m/%Y, at %H:%M:%S"), inline=False)
        embed.add_field(name="Account age", value=f"approximately {date.days} days old.", inline=False)
        embed.add_field(name="In server", value=is_in_server)
        embed.add_field(name="Bot", value=member.bot)

        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"UID : {member.id}")

        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, mention_or_id=None):
        if mention_or_id:
            member = await self.get_user(ctx, mention_or_id)
            if not member:
                return await ctx.send(f"❌ User `{mention_or_id}` not found.")
        else:
            member = ctx.author

        embed = discord.Embed(
            title = f"Avatar for {member}",
            colour = random_color()
        )

        embed.set_image(url=member.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def info(self, ctx):
        """ See bot info. """
        with open('description.txt', 'r') as file:
            description = file.read()
        replacements = {
            "{bot_name}" : self.client.user.name,
            "{bot_guilds_count}" : str(len(self.client.guilds))
        }
        for item in replacements.items():
            description = description.replace(item[0], item[1])

        embed = discord.Embed(
            title = f"{self.client.user.name} info.",
            description = description,
            colour = random_color()
        )

        embed.set_footer(text=f"Prefix{'es' * (len(self.client.command_prefix) - 1)}: {', '.join([p.strip() for p in self.client.command_prefix])}")
        await ctx.send(embed=embed)

    async def get_user(self, ctx, mention_or_id):
        if mention_or_id.isdigit():
            member = self.client.get_user(int(mention_or_id))
        else:
            converter = MemberConverter()
            member = await converter.convert(ctx, mention_or_id)

        return member


def setup(client):
    client.add_cog(Info(client))