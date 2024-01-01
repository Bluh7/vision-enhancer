import discord
from discord.ext import commands
import os
from helpers.users_running import UsersRunning
from helpers.image_enhancement import ImageEnhancement
from helpers.get_image import GetImage


class Full(commands.Cog):
    def __init__(self, client) -> None:
        self.CLIENT = client
        self.UR = UsersRunning()
        self.GI = GetImage()

    @discord.slash_command(name="full", description="Upscales, sharpens and denoises an image to get a better quality (recommended using 4x factor)")
    @commands.guild_only()
    @discord.option(
        "factor",
        required=False,
        default="4",  # must be a string
        description="Times to upscale the image (higher is better quality), minimum is 2 and maximum is 4"
    )
    async def full(self, ctx, factor: str) -> None:
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

        if factor and not factor.isdigit() or int(factor) > 4 or int(factor) < 2:
            invalid_factor_embed = discord.Embed(
                title="Invalid factor!",
                description="Factor must be a number between 2 and 4",
                color=discord.Color.yellow()
            )
            invalid_factor_embed.set_footer(text=self.CLIENT.user.name,
                                            icon_url=self.CLIENT.user.avatar)
            await ctx.respond(embed=invalid_factor_embed, ephemeral=True)
            return

        self.UR.add_new_user_running(ctx.author.id)

        waiting_for_image_embed = discord.Embed(
            title="Waiting for you to upload an image!",
            description=f"Please upload an image (upscaling, sharpening and denoising will be applied to it) factor is **{factor}x**",
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

        full_enhancementing_embed = discord.Embed(
            title="I'm upscaling, sharpening and denoising your image!",
            description=f"Please wait while I upscale, sharpen and denoise your image (this may take a while)",
            color=discord.Color.blue()
        )
        full_enhancementing_embed.set_footer(text=self.CLIENT.user.name,
                                             icon_url=self.CLIENT.user.avatar)

        await user_msg.delete()
        await client_msg.edit_original_response(embed=full_enhancementing_embed)
        await ctx.channel.trigger_typing()

        IE = ImageEnhancement(image, ctx.author.id)
        await IE.full_enhance(int(factor))

        full_enhancement_image_embed = discord.Embed(
            title=f"{ctx.author.name} here is your upscaled, sharpened and denoised image!",
            description=f"This image was upscaled by **{factor}x** and it's new resolution went from **{image.width}x{image.height}** to approximately **{image.width * int(factor)}x{image.height * int(factor)}**",
            color=discord.Color.blue()
        )
        full_enhancement_image_embed.set_footer(text=self.CLIENT.user.name,
                                                icon_url=self.CLIENT.user.avatar)
        full_enhancement_image_embed.set_image(
            url=f"attachment://{ctx.author.id}.png")

        # sends the embed with the upscaled image in the embed
        await ctx.channel.send(
            embed=full_enhancement_image_embed,
            file=discord.File(
                f"../results/{ctx.author.id}.png",
                filename=f"{ctx.author.id}.png"
            )
        )
        await client_msg.delete_original_response()
        os.remove(f"../results/{ctx.author.id}.png")
        self.UR.remove_user_running(ctx.author.id)


def setup(client) -> None:
    client.add_cog(Full(client))
