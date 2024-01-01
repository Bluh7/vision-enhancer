import discord
from discord.ext import commands
import os
from helpers.users_running import UsersRunning
from helpers.image_enhancement import ImageEnhancement
from helpers.get_image import GetImage


class Sharpen(commands.Cog):
    def __init__(self, client) -> None:
        self.CLIENT = client
        self.UR = UsersRunning()
        self.GI = GetImage()

    @discord.slash_command(name="sharpen", description="Sharpen an image to get a better quality (not recommended for low resolution images)")
    @commands.guild_only()
    async def sharpen(self, ctx) -> None:
        if ctx.author.id in self.UR.users_running_list:
            already_running_embed = discord.Embed(
                title="You are already running this command!",
                description="Please end the previous command before running this one or wait for it to finish",
                color=discord.Color.red()
            )
            already_running_embed.set_footer(text=self.CLIENT.user.name,
                                             icon_url=self.CLIENT.user.avatar)
            await ctx.respond(embed=already_running_embed, ephemeral=True)
            return

        self.UR.add_new_user_running(ctx.author.id)

        waiting_for_image_embed = discord.Embed(
            title="Waiting for you to upload an image!",
            description=f"Please upload an image to sharpen it",
            color=discord.Color.blue()
        )
        waiting_for_image_embed.set_footer(text=self.CLIENT.user.name,
                                           icon_url=self.CLIENT.user.avatar)

        client_msg = await ctx.respond(embed=waiting_for_image_embed, ephemeral=True)

        # waits for the user to upload an image for 60 seconds
        try:
            user_msg = await self.CLIENT.wait_for(
                "message",
                check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.attachments,
                timeout=60,
            )
        except TimeoutError:
            too_long_embed = discord.Embed(
                title="You took too long to upload an image!",
                description="Please try again",
                color=discord.Color.yellow()
            )
            too_long_embed.set_footer(text=self.CLIENT.user.name,
                                      icon_url=self.CLIENT.user.avatar)
            await client_msg.edit_original_response(embed=too_long_embed)
            self.UR.remove_user_running(ctx.author.id)
            return

        IMAGE_URL = user_msg.attachments[0]
        image = self.GI.get_image(IMAGE_URL)

        sharpening_embed = discord.Embed(
            title="I'm sharpening your image!",
            description=f"Please wait while I sharpen your image (this may take a while)",
            color=discord.Color.blue()
        )
        sharpening_embed.set_footer(text=self.CLIENT.user.name,
                                    icon_url=self.CLIENT.user.avatar)

        await user_msg.delete()
        await client_msg.edit_original_response(embed=sharpening_embed)
        await ctx.channel.trigger_typing()

        IE = ImageEnhancement(image, ctx.author.id)
        await IE.sharpen_enhance()

        sharpened_image_embed = discord.Embed(
            title=f"{ctx.author.name} here is your sharpened image!",
            description=f"This image was sharpened",
            color=discord.Color.blue()
        )
        sharpened_image_embed.set_footer(text=self.CLIENT.user.name,
                                         icon_url=self.CLIENT.user.avatar)
        sharpened_image_embed.set_image(
            url=f"attachment://{ctx.author.id}.png")

        # sends the embed with the upscaled image in the embed
        await ctx.channel.send(
            embed=sharpened_image_embed,
            file=discord.File(
                f"../results/{ctx.author.id}.png",
                filename=f"{ctx.author.id}.png"
            )
        )
        await client_msg.delete_original_response()
        os.remove(f"../results/{ctx.author.id}.png")
        self.UR.remove_user_running(ctx.author.id)


def setup(client) -> None:
    client.add_cog(Sharpen(client))
