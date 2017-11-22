import discord
import json
import re #only

import utils

# TODO: Create an instance - cmd_handler = CommandHandler(client)
#       Call the member function - cmd_handler.handle_commands(message)

"""
This module provides stuff that helps with processing commands.
"""

STATIC_COMMANDS_FILE = 'static_commands.json'
SKILL_COMMANDS_FILE = 'skills.json'
COMMAND_PREFIX = "!"
COLOR_TYPES = {
    'red': 0xD92242, 
    'green': 0x0CA428, 
    'blue': 0x2763D6, 
    'grey': 0x63737B, 
    'cyan': 0x28EFEF, 
    'purple': 0xA012ED, 
    'yellow': 0xDEC027, 
    'orange': 0xEA803F
}
EMBED_ICON_URL = 'https://i.imgur.com/CyaOfZE.png'

def read_static_commands() -> dict:
    """
    Reads all static commands from their source file.

    :return: Dictionary mapping command names to their output values.
    """
    with open(STATIC_COMMANDS_FILE) as f:
        return json.load(f)


def read_skill_commands() -> dict:
    """
    Reads all skill commands from their source file.abs

    :return: Dictionary mapping command names to their outputs.
    """
    with open(SKILL_COMMANDS_FILE) as f:
        old_skills = json.load(f)
        new_skills = {}
        for old_skill in old_skills:
            new_skill = {
                'name': old_skill['name'],
                'content': old_skill['content'],
                'color': old_skill['color'],
                'aka': old_skill['aka'],
                'skill': old_skill['skill']
            }
            new_skills[old_skill['name']] = new_skill
            for a in old_skill['aliases']:
                new_skills[a] = new_skill
        return new_skills

        

class CommandHandler:
    """
    This class is designed to provide an easier to use interface for processing
        commands.
    """

    def __init__(self, bot):
        """
        Constructor creating a new instance of a command handler. Only one
            instance is needed per bot object.

        :param bot: Discord bot object using this CommandHandler.
        """
        # Instance variables.
        self.bot = bot
        self.static_commands = read_static_commands()
        self.skill_commands = read_skill_commands()

    async def handle_commands(self, message):
        """
        Handles responding to any commands present in a given message.

        :param message: Discord message object to search and respond to commands
            for. 
        """
        await self._handle_static_commands(message)
        await self._handle_skill_commands(message)
        # TODO: You'll probably add different functions for handling different
        # types of commands. I'm just using this as a small example.

    async def _handle_static_commands(self, message):
        msg_split = message.content.split(' ')
        command_str = msg_split[0]

        if command_str.startswith(COMMAND_PREFIX):
            command_str = command_str[1:] # Get rid of that nasty prefix.

            if command_str not in self.static_commands:
                return # Abandon ship if the command does not exist.

            command = self.static_commands[command_str]
            await self.bot.send_message(message.channel, command['message'])

    async def _handle_skill_commands(self, message):
        if '{{' in message.content and '}}' in message.content:
            start = '{{'
            end = '}}'
            query = re.search(
                    '%s(.*)%s' % (start, end), message.content).group(1).lower()
            
            if query not in self.skill_commands:
                await self._handle_error(message)
                return

            skill = self.skill_commands[query]
            emb = discord.Embed(title=skill['aka'],
                                description=skill['content'],
                                color=int(COLOR_TYPES[skill['color']]))
            emb.set_author(name=skill['skill'], icon_url=EMBED_ICON_URL)
            await self.bot.send_message(message.channel, embed=emb)

    async def _handle_error(self, message):
        """
        Tells a user they messed up.
        """
        if message.author.id == "188123523691053060": #Yellow
            await self.bot.send_message(message.channel, "<@188123523691053060> I don't think you typed that correctly! Classic yellow.")
        elif message.author.id == "126197907392167937": #Me
            await self.bot.send_message(message.channel, "lol alpha doesn't know how to use his own bot")
        else: #@everyone else
             await self.bot.send_message(message.channel, "<@" + message.author.id + "> I don't know what you mean! If you think I should, use !report to tell Alpha to fix it")
