import discord
from discord.ext import commands


class Authentication(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.is_protection_on: bool = False

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        new_member_role: discord.Role = self.bot.get_channel(465158208978157588).guild.get_role(663581221967757313)
        await member.add_roles(new_member_role)

    @commands.command()
    @commands.dm_only()
    async def rule_acknowledged(self, ctx: commands.Context) -> None:
        if self.is_protection_on:
            await ctx.send(
                "Unfortunately, the moderators of 22/7 server have turned on the server protection protocol, "
                "new members may not join at this time. Please wait until the restriction is lifted. ")
        else:
            user_id: int = ctx.author.id

            nananijiguild: discord.Guild = self.bot.get_guild(336277820684763148)
            if nananijiguild.get_member(user_id) is None:
                await ctx.send("Unsupported operation.")
                return

            new_member_role: discord.Role = nananijiguild.get_role(663581221967757313)
            if new_member_role not in nananijiguild.get_member(user_id).roles:
                await ctx.send("You are already a member!")
                return

            await nananijiguild.get_member(user_id).remove_roles(new_member_role,
                                                                 reason="User acknowledged rule. ")
            await ctx.send(
                "You should have access to the rest of the server now. If not, please DM one of the Moderators. ")

    @commands.command()
    @commands.has_any_role('Moderators')
    async def protect(self, ctx: commands.Context) -> None:
        """
        Do mysterious things.
        Note: this is an on/off switch command.
        """
        self.is_protection_on = not self.is_protection_on
        await ctx.send("Protection is {}".format(self.is_protection_on))
