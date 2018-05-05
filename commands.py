import discord
import json
import re

import utils
import pat_manager

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
    'orange': 0xEA803F,
    'white': 0xDEDEDE
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

static_commands = read_static_commands() 
skill_commands = read_skill_commands()     

class CommandHandler:
    """
    This class is designed to provide an easier to use interface for processing
        commands.
    """

    def __init__(self, bot, message):
        """
        Constructor creating a new instance of a command handler. Only one
            instance is needed per bot object.

        :param bot: Discord bot object using this CommandHandler.
        :param message: Discord message being handled.
        """
        # Instance variables.
        self.bot = bot
        self.content = message.content
        self.channel = message.channel
        self.author = message.author

    async def handle_commands(self):
        """
        Handles responding to any commands present in a given message.

        :param message: Discord message object to search and respond to commands
            for. 
        """
        await self._handle_prefixed_commands()
        await self._handle_skill_commands()
        # TODO: You'll probably add different functions for handling different
        # types of commands. I'm just using this as a small example.

    async def _handle_prefixed_commands(self):
        if not self.content.startswith(COMMAND_PREFIX):
            return

        msg_split = self.content.split(' ')
        command = msg_split[0][1:]
        args = msg_split[1:]

        await self._handle_static_commands(command)
        await self._handle_pat_commands(command)

    async def _handle_static_commands(self, command):
        if command not in static_commands:
            return # Abandon ship if the command does not exist.
        command = static_commands[command]
        await self._send_response(command['message'])

    async def _handle_pat_commands(self, command):
        if command in ['checkpats', 'checkpets']:
            count = pat_manager.get_pats(self.author.id)
            if count == 0:
                await self._send_reply("You haven't pet Feh yet :(")
            else: 
                time_str = 'time!'
                if count > 1:
                    time_str = 'times!'
                reply = "You've pet Feh " + pat_manager.format_pat_count(count)
                reply += " " + time_str
                await self._send_reply(reply)

        if command in ['pat', 'pet', 'headpat']:
            pat_manager.add_pats(self.author.id, 1)
            await self._send_response('Thanks! ^_^')

        if command in ['halfpat', 'halfpet']:
            pat_manager.add_pats(self.author.id, 0.5)
            await self._send_response('Thanks!')

    async def _handle_skill_commands(self):
        if '{{' in self.content and '}}' in self.content:

            # regex the skill
            query = re.search(
                    '%s(.*)%s' % ('{{', '}}'), self.content).group(1).lower()

            query = utils.spellcheck(query, skill_commands)

            # just in case it errors
            if query not in skill_commands:
                await self._handle_error()
                return

            skill = skill_commands[query]
            emb = discord.Embed(title=skill['aka'],
                                description=skill['content'],
                                color=int(COLOR_TYPES[skill['color']]))
            emb.set_author(name=skill['skill'], icon_url=EMBED_ICON_URL)
            await self.bot.send_message(self.channel, embed=emb)

    async def _send_reply(self, response):
        await self._send_response(
                utils.mention(self.author) + ' ' + response)

    async def _send_response(self, response):
        await self.bot.send_message(self.channel, response)

    async def _handle_error(self):
        """
        Tells a user they messed up.
        """
        if self.author.id == "188123523691053060": #Yellow
            await self._send_response("<@188123523691053060> I don't think you typed that correctly! Classic yellow.")
        elif self.author.id == "126197907392167937": #Me
            await self._send_response("lol alpha doesn't know how to use his own bot")
        else: #@everyone else
            await self._send_response("<@" + self.author.id + "> I don't know what you mean! If you think I should, use !report to tell Alpha to fix it")
