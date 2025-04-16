import discord
import aiosqlite
from discord.ext import commands
from discord import app_commands, ui
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# Database initialization
async def init_db():
    async with aiosqlite.connect("tickets.db") as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            channel_id INTEGER,
            category TEXT,
            status TEXT DEFAULT 'open',
            created_at DATETIME
        )''')
        await db.commit()



TICKET_CATEGORIES = {
    "Help & Support": {
        "description": "General help and support requests"
    },
    "Team Joining Application": {
        "description": "Applications to join our team"
    },
    "Staff Application": {
        "description": "Applications for staff positions"
    },
    "Custom": {
        "description": "Custom requests"
    }
}


class TicketDropdown(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=category,
                description=config["description"],
                emoji="🎫"
            ) for category, config in TICKET_CATEGORIES.items()
        ]
        super().__init__(
            placeholder="Select ticket category...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        config = TICKET_CATEGORIES[category]


        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            discord.utils.get(interaction.guild.roles, name="Support Team"):
                discord.PermissionOverwrite(read_messages=True)
        }

        category_channel = discord.utils.get(interaction.guild.categories, name="Tickets")
        ticket_channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category_channel,
            overwrites=overwrites
        )


        embed = discord.Embed(
            title=f"{category} Ticket",
            description=f"**User:** {interaction.user.mention}\n"
                        f"**Category:** {category}\n"
                        f"**Created At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            color=0x00ff00
        )
        embed.set_image(url=config["image"])
        embed.add_field(
            name="Guidelines",
            value="1. Be respectful\n2. Provide all necessary information\n3. Wait for support response",
            inline=False
        )

        view = TicketManagementView()

        await ticket_channel.send(
            f"{interaction.user.mention} | <@&SUPPORT_ROLE_ID>",
            embed=embed,
            view=view
        )

        async with aiosqlite.connect("tickets.db") as db:
            await db.execute('''INSERT INTO tickets 
                              (user_id, channel_id, category, created_at)
                              VALUES (?, ?, ?, ?)''',
                             (interaction.user.id, ticket_channel.id,
                              category, datetime.now()))
            await db.commit()

        await interaction.response.send_message(
            f"Ticket created: {ticket_channel.mention}",
            ephemeral=True
        )


class TicketManagementView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: ui.Button):
        if "Support Team" not in [role.name for role in interaction.user.roles]:
            return await interaction.response.send_message(
                "Only support team can close tickets!",
                ephemeral=True
            )

        async with aiosqlite.connect("tickets.db") as db:
            await db.execute("UPDATE tickets SET status='closed' WHERE channel_id=?",
                             (interaction.channel.id,))
            await db.commit()

        await interaction.channel.delete()


class TicketSetupView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())


@bot.tree.command(name="setup_tickets")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tickets(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎫Ticket",
        description="""
**Welcome to the official support system!** If you need help, feel free to create a ticket. 
            Our team is here to assist you.\n\n
            **📌 __You can create a ticket for:__**\n
            ✅ **Help & support from staff**\n
            ✅ **Team Joining** _(When Application is open)_\n
            ✅ **Team Media role request**\n
            ✅ **Any other important plans related to teams**\n\n
            **📜 __Ticket Rules:__**\n
            🚫 __Do not spam or create unnecessary tickets__\n
            🚫 __Begging for roles or permissions is not allowed__\n
            🚫 __Stay respectful & follow staff instructions__

        """,
        color=0x7289da
    )
    embed.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWZ5c2l0NnNlY2phMzYzOXlrMng3c3Ftbmh3bjdtZ29heGE0NmJmdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PfhDVTbCOsBxOMzemc/giphy.gif")


    if not discord.utils.get(interaction.guild.categories, name="Tickets"):
        await interaction.guild.create_category("Tickets")


    if not discord.utils.get(interaction.guild.roles, name="Support Team"):
        await interaction.guild.create_role(name="Support Team", color=discord.Color.green())

    await interaction.channel.send(embed=embed, view=TicketSetupView())
    await interaction.response.send_message("Ticket system setup complete!", ephemeral=True)


@bot.event
async def on_ready():
    await init_db()
    await bot.tree.sync()
    print(f"Bot ready as {bot.user}")


bot.run("discord bot token")