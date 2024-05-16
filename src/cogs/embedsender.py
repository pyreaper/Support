import disnake
from disnake import TextInputStyle
from disnake.ext import commands


class EmbedSettingsModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Титул",
                placeholder="Новости",
                custom_id="title",
                style=TextInputStyle.short,
                required=True,
            ),
            disnake.ui.TextInput(
                label="Описание",
                placeholder="У нас вышло что то новое",
                custom_id="description",
                style=TextInputStyle.paragraph,
                required=True,
            ),
            disnake.ui.TextInput(
                label="Футер",
                placeholder="©️ CMT 2024. All rights reserved.",
                custom_id="footer",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Ссылка на картинку",
                placeholder="...",
                custom_id="image",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Контент сообщения",
                placeholder="@everyone",
                custom_id="content",
                style=TextInputStyle.short,
                required=False,
            ),
        ]
        super().__init__(title="Настройки", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        embed_to_send = disnake.Embed(
            title=inter.text_values["title"],
            description=inter.text_values["description"]
        )

        if inter.text_values["footer"] != "":
            embed_to_send.set_footer(text=inter.text_values["footer"])

        if inter.text_values["image"] != "":
            embed_to_send.set_image(url=inter.text_values["image"])

        if inter.text_values["content"] != "":
            await inter.channel.send(content=inter.text_values["content"], embeds=[embed_to_send])
        else:
            await inter.channel.send(embeds=[embed_to_send])

        await inter.response.send_message("Эмбед успешно отправлен.", ephemeral=True)


class EmbedSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="send_embed", description="Отправить эмбед (в канал в котором используется комманда)",
                            dm_permission=False, aliases=['embed', 'эмбед'])
    @commands.default_member_permissions(administrator=True)
    async def suembed(self, inter):
        await inter.response.send_modal(modal=EmbedSettingsModal())


def setup(bot: commands.Bot):
    bot.add_cog(EmbedSender(bot))
