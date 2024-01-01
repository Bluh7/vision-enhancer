import discord
from discord.ext import commands
import os
from helpers.users_running import UsersRunning
from helpers.image_enhancement import ImageEnhancement
from helpers.get_image import GetImage


class Denoise(commands.Cog):
    def __init__(self, client) -> None:
        self.CLIENT = client
        self.UR = UsersRunning()
        self.GI = GetImage()

    @discord.slash_command(name="denoise", description="Denoises an image to get a better quality (not recommended for low res images)")
    @commands.guild_only()
    async def denoise(self, ctx) -> None:
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
            description=f"Please upload an image to denoise",
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

        denoising_embed = discord.Embed(
            title="I'm denoising your image!",
            description=f"Please wait while I denoise your image (this may take a while)",
            color=discord.Color.blue()
        )
        denoising_embed.set_footer(text=self.CLIENT.user.name,
                                   icon_url=self.CLIENT.user.avatar)

        await user_msg.delete()
        await client_msg.edit_original_response(embed=denoising_embed)
        await ctx.channel.trigger_typing()

        IE = ImageEnhancement(image, ctx.author.id)
        await IE.denoise_enhance()

        denoised_image_embed = discord.Embed(
            title=f"{ctx.author.name} here is your denoised image!",
            description=f"This image was denoised removing the jpg artifacts from the image",
            color=discord.Color.blue()
        )
        denoised_image_embed.set_footer(text=self.CLIENT.user.name,
                                        icon_url=self.CLIENT.user.avatar)
        denoised_image_embed.set_image(
            url=f"attachment://{ctx.author.id}.png")

        # sends the embed with the upscaled image in the embed
        await ctx.channel.send(
            embed=denoised_image_embed,
            file=discord.File(
                f"../results/{ctx.author.id}.png",
                filename=f"{ctx.author.id}.png"
            )
        )
        await client_msg.delete_original_response()
        os.remove(f"../results/{ctx.author.id}.png")
        self.UR.remove_user_running(ctx.author.id)


def setup(client) -> None:
    client.add_cog(Denoise(client))
