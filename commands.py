import json

import utils

# TODO: Create an instance - cmd_handler = CommandHandler(client)
#       Call the member function - cmd_handler.handle_commands(message)

"""
This module provides stuff that helps with processing commands.
"""

STATIC_COMMANDS_FILE = 'static_commands.json'
COMMAND_PREFIX = "!"

def read_static_commands() -> dict:
    """
    Reads all static commands from their souce file.abs

    :return: Dictionary mapping command names to their output values.
    """
    with open(STATIC_COMMANDS_FILE) as f:
        return json.load(f)

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

    async def handle_commands(self, message):
        """
        Handles responding to any commands present in a given message.abs

        :param message: Discord message object to search and respond to commands
            for. 
        """
        self._handle_static_commands(message)
        # TODO: You'll probably add different functions for handling different
        # types of commands. I'm just using this as a small example.

    async def _handle_static_commands(self, message):
        msg_split = message.content.split[' ']
        command_str = msg_split[0]

        if command_str.startswith(COMMAND_PREFIX):
            command_str = command_str[1:] # Get rid of that nasty prefix.

            if command_str not in self.static_commands:
                return # Abandon ship if the command does not exist.

            command = self.static_commands[command_str]

            await self.bot.send_message(message.channel, command['message'])
            print(utils.mention(message.author) + ' ' + command['log_message'])
