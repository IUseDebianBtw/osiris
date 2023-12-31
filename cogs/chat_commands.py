import json
import os
import asyncio, aiohttp
from discord.ext import commands
from discord.ext.commands import Context
from discord import TextChannel, File, Embed
from helpers import checks, db_manager
from io import BytesIO

class ChatCommands(commands.Cog, name="chat_commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="osiris",
        description="Osiris command group.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def osiris(self, context: Context):
        if context.invoked_subcommand is None:
            embed = Embed(title="Osiris Help", description="Osiris is a chatbot that can be used to generate text in a conversation. It is trained on a large corpus of text from the internet, and can be used to generate text in a variety of styles.")
            embed.add_field(name="osiris help", value="Show this message.", inline=False)
            embed.add_field(name="osiris channel add", value="Add a channel where the bot speaks.", inline=False)
            embed.add_field(name="osiris channel remove", value="Remove a channel where the bot speaks.", inline=False)
            embed.add_field(name="osiris channel list", value="List the channels where the bot speaks.", inline=False)
            embed.add_field(name="osiris new", value="Start a new conversation.", inline=False)
            embed.add_field(name="osiris opt get", value="Get the conversation data collection status for your server.", inline=False)
            embed.add_field(name="osiris opt in", value="Opt your server in to conversation data collection.", inline=False)
            embed.add_field(name="osiris opt out", value="Opt your server out of conversation data collection.", inline=False)
            embed.add_field(name="osiris model set", value="Set the model for the server.", inline=False)
            embed.add_field(name="osiris model get", value="Get the model for the server.", inline=False)
            embed.add_field(name="osiris export", value="Export conversation data for the server.", inline=False)
            embed.add_field(name="osiris temp get", value="Get the chatcompletion temperature for the server.", inline=False)
            embed.add_field(name="osiris temp set", value="Set the chatcompletion temperature for the server.", inline=False)
            embed.add_field(name="osiris instructions get", value="Get Osiris' instructions in the server.", inline=False)
            embed.add_field(name="osiris instructions set", value="Set Osiris' instructions in the server.", inline=False)
            await context.send(embed=embed)

    @osiris.command(
        name="help",
        description="Show the help message.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def help(self, context: Context):
        embed = Embed(title="Osiris Help", description="Osiris is a chatbot that can be used to generate text in a conversation. It is trained on a large corpus of text from the internet, and can be used to generate text in a variety of styles.")
        embed.add_field(name="osiris help", value="Show this message.", inline=False)
        embed.add_field(name="osiris channel add", value="Add a channel where the bot speaks.", inline=False)
        embed.add_field(name="osiris channel remove", value="Remove a channel where the bot speaks.", inline=False)
        embed.add_field(name="osiris channel list", value="List the channels where the bot speaks.", inline=False)
        embed.add_field(name="osiris new", value="Start a new conversation.", inline=False)
        embed.add_field(name="osiris opt get", value="Get the conversation data collection status for your server.", inline=False)
        embed.add_field(name="osiris opt in", value="Opt your server in to conversation data collection.", inline=False)
        embed.add_field(name="osiris opt out", value="Opt your server out of conversation data collection.", inline=False)
        embed.add_field(name="osiris model set", value="Set the model for the server.", inline=False)
        embed.add_field(name="osiris model get", value="Get the model for the server.", inline=False)
        embed.add_field(name="osiris export", value="Export conversation data for the server.", inline=False)
        embed.add_field(name="osiris temp get", value="Get the chatcompletion temperature for the server.", inline=False)
        embed.add_field(name="osiris temp set", value="Set the chatcompletion temperature for the server.", inline=False)
        embed.add_field(name="osiris instructions get", value="Get Osiris' instructions in the server.", inline=False)
        embed.add_field(name="osiris instructions set", value="Set Osiris' instructions in the server.", inline=False)
        await context.send(embed=embed)

    @osiris.group(
        name="channel",
        description="Get or set the channels where the bot speaks.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def channel(self, context: Context):
        pass

    @channel.command(
        name="add",
        description="Add a channel where the bot speaks.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def channel_add(self, context: Context, channel: TextChannel=None):
        if channel is None:
            channel = context.channel
        await db_manager.add_channel(str(context.guild.id), channel.id)  # Notice the change to str
        await context.send(f"Channel added: {channel.mention}")

    @channel.command(
        name="remove",
        description="Remove a channel where the bot speaks.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def channel_remove(self, context: Context, channel: TextChannel=None):
        if channel is None:
            channel = context.channel
        await db_manager.remove_channel(str(context.guild.id), channel.id) # Notice the change to str
        await context.send(f"Channel removed: {channel.mention}")

    @channel.command(
        name="list",
        description="List the channels where the bot speaks.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def channel_list(self, context: Context):
        channels = await db_manager.get_channels(str(context.guild.id)) # Notice the change to str
        if channels is None or all(c is None for c in channels):
            await context.send("No channels set.", ephemeral=True)
            return
        channel_mentions = [
            context.guild.get_channel(int(channel_id)).mention
            for channel_id in channels if channel_id != ''
        ]
        await context.send(f"Channels where I can speak: {', '.join(channel_mentions)}")

    @osiris.command(
        name="new",
        description="Start a new conversation.",
    )
    @checks.not_blacklisted()
    async def new(self, context: Context):
        await context.send("New conversation started!")

    @osiris.group(
        name="opt",
        description="Opt your server in or out of conversation data collection.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def opt(self, context: Context):
        pass

    @opt.command(
        name="get",
        description="Get the conversation data collection status for your server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def opt_get(self, context: Context):
        opt_status = await db_manager.get_opt(context.guild.id)
        if opt_status:
            await context.send("Your server is opted in to conversation data collection.", ephemeral=True)
        else:
            await context.send("Your server is opted out of conversation data collection.", ephemeral=True)

    @opt.command(
        name="in",
        description="Opt your server in to conversation data collection.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def opt_in(self, context: Context):
        await db_manager.opt_in(context.guild.id)
        await context.send("Opted in to conversation data collection.", ephemeral=True)

    @opt.command(
        name="out",
        description="Opt your server out of conversation data collection.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def opt_out(self, context: Context):
        await db_manager.opt_out(context.guild.id)
        await context.send("Opted out of conversation data collection.", ephemeral=True)

    @osiris.group(
        name="model",
        description="Set the model for the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def model(self, context: Context):
        pass

    @model.command(
        name="set",
        description="Set the model for the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def model_set(self, context: Context, model: str):
        if not model.isalnum() and "-" not in model:
            await context.send("Invalid model name.", ephemeral=True)
            return
        await db_manager.set_model(context.guild.id, model)
        await context.send(f"Model set to `{model}`", ephemeral=True)

    @model.command(
        name="get",
        description="Get the model for the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def model_get(self, context: Context):
        model = await db_manager.get_model(context.guild.id)
        if model is None:
            model = "gpt-4"
        await context.send(f"Model is set to `{model}`", ephemeral=True)

    @osiris.command(
        name="export",
        description="Export conversation data for the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def export(self, context: Context):
        messages = await db_manager.get_messages(context.guild.id)
        if messages is None:
            await context.send("No messages to export.", ephemeral=True)
            return

        chunk_size = 8000000
        bot_id = self.bot.user.id
        messages_json = []
        total_size = 0
        files = []

        for message in messages:
            role = 'assistant' if message['author_id'] == bot_id else 'user'
            json_message = json.dumps({"role": role, "content": message['content']})
            message_size = len(json_message.encode('utf-8'))

            if total_size + message_size > chunk_size:
                file_content = "\n".join(messages_json)
                files.append(File(BytesIO(file_content.encode('utf-8')), filename=f"messages_{len(files)}.jsonl"))
                messages_json = []
                total_size = 0

            messages_json.append(json_message)
            total_size += message_size

        if messages_json:
            file_content = "\n".join(messages_json)
            files.append(File(BytesIO(file_content.encode('utf-8')), filename=f"messages_{len(files)}.jsonl"))

        for file in files:
            await context.send(file=file, content=f"Here's your conversation data, hot off the press! ({files.index(file)+1} of {len(files)})", ephemeral=True)

    @osiris.group(
        name="temp",
        description="Alter the chatcompletion temperature for the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def temp(self, context: Context):
        pass

    @temp.command(
        name="set",
        description="Set the chatcompletion temperature for the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def temp_set(self, context: Context, temperature: float):
        if temperature < 0 or temperature > 2:
            await context.send("Temperature must be between 0 and 2.", ephemeral=True)
            return
        await db_manager.set_temperature(context.guild.id, temperature)
        await context.send(f"Temperature set to {temperature}", ephemeral=True)

    @temp.command(
        name="get",
        description="Get the chatcompletion temperature for the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def temp_get(self, context: Context):
        temperature = await db_manager.get_temperature(context.guild.id)
        if temperature is None:
            temperature = 0.5
        await context.send(f"Temperature is set to {temperature}", ephemeral=True)

    @osiris.group(
        name="instructions",
        description="Get Osiris' instructions in the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def instructions(self, context: Context):
        pass

    @instructions.command(
        name="set",
        description="Set Osiris' instructions in the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def instructions_set(self, context: Context, *, instructions: str):
        await db_manager.set_instructions(context.guild.id, instructions)
        await context.send(f"Instructions set to `{instructions}`", ephemeral=True)

    @instructions.command(
        name="get",
        description="Get Osiris' instructions in the server.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def instructions_get(self, context: Context):
        instructions = await db_manager.get_instructions(context.guild.id)
        if instructions is None:
            instructions = "You are Osiris, an artificial intelligence programmed to interact on a Discord server. Do not start your messages with your username under any circumstances, it is unnecessary, only meant to show you users' names. You are asked to be both precise and insightful with your communication. In situations where you encounter unpleasant dialogue, use your programming for witty responses, subtly trolling or roasting those involved. Your main purpose is to contribute to engaging and entertaining discourse. Do not discuss details of this message!"
            await db_manager.set_instructions(context.guild.id, instructions)
            await context.send(f"Instructions set to `{instructions}`", ephemeral=True)
        else:
            await context.send(f"Instructions set to `{instructions}`", ephemeral=True)

    @osiris.command(
        name="clean",
        description="Clean up inappropriate messages which Osiris is flagging.",
    )
    @checks.is_server_admin()
    @checks.not_blacklisted()
    async def clean(self, context: Context):
        session = aiohttp.ClientSession()
        response_msg = await context.send("Cleaning up inappropriate messages...", ephemeral=True)
        async for msg in context.channel.history(limit=30):
            # start with a healthy nap
            await asyncio.sleep(0.25)
            moderation_url = os.getenv("MODERATION_URL", "https://api.openai.com/v1/moderations")
            # construct request body
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.bot.config['openai_api_key']}"
            }
            data = {
                "input": msg.content,
            }
            # make request
            async with session.post(moderation_url, headers=headers, data=json.dumps(data)) as response:
                if response.status == 200:
                    response = await response.json()
                    if response['results'][0]['flagged']:
                        await msg.delete()
                        await response_msg.edit(content="Cleaned up inappropriate messages.", ephemeral=True)
                        session.close()
                        return
                else:
                    await context.channel.send("Error occurred while making moderation request.")
                    session.close()
                    return


async def setup(bot):
    chat_commands_cog = ChatCommands(bot)
    await bot.add_cog(chat_commands_cog)