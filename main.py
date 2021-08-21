import discord
from discord_components import DiscordComponents
from discord.ext import commands
import os


class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualifed_name}: {[command.name for command in mapping[cog]]}')

    async def send_cog_help(self, cog):
        await self.get_destination().send(f'{cog.qualifed_name}: {[command.name for command in cog.get_commands()]}')

    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

    async def send_command_help(self, command):
        await self.get_destination().send(command.name)


with open('Texts/Secrets.txt', 'r') as filestream:
    data = filestream.readlines()
    TOKEN = data[0]
filestream.close()

client = commands.Bot(command_prefix='?', help_command=commands.MinimalHelpCommand())
DiscordComponents(client)


@client.event
async def on_message(message):  # When Someone Types Something
    await client.process_commands(message)
    if message.author == client.user:  # So it doesn't respond to itself potentially
        return


@client.event
async def on_command_error(ctx, error):  # If User uses Command that doesn't exist
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command')


@client.command(pass_context=True)
async def embeded(ctx):
    embed = discord.Embed(
        title='Title',
        description='Snolid Ice',
        colour=discord.Colour.blue(),
    )

    embed.set_footer(text='Total Plays:')
    embed.set_image(url='https://www.speedrun.com/gameasset/9dowwk1p/cover?v=26a8ad0')  # LEGO
    embed.set_thumbnail(url='https://www.speedrun.com/gameasset/46w33l1r/cover?v=19285e8')  # TCS
    embed.set_author(name='Author', icon_url='https://www.speedrun.com/gameasset/yd4wqg6e/cover?v=6a04a5f')  # LB3
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)

    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def test(ctx, *, message):
    await ctx.send(message)


@test.error
async def test_error(ctx, error):  # Error Checking for test command
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please fill all arguments')


@client.command()
async def reload(ctx, extension):  # Reloads Cog Files
    if ctx.author.id == 227499228413427712:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
    else:
        await ctx.send("You don't have permission to use that")


for filename in os.listdir('./cogs'):  # Loading Cogs
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
