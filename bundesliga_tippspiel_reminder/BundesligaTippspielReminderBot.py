"""LICENSE
Copyright 2019 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel-reminder (btr).

btr is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

btr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with btr.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from bokkichat.entities.message.TextMessage import TextMessage
from kudubot.Bot import Bot
from kudubot.db.Address import Address as Address
from kudubot.parsing.CommandParser import CommandParser
from bundesliga_tippspiel_reminder.BundesligaTippspielReminderParser import \
    BundesligaTippspielReminderParser


class BundesligaTippspielReminderBot(Bot):
    """
    The bundesliga tippspiel reminder bot
    """

    def on_command(
            self,
            message: TextMessage,
            parser: CommandParser,
            command: str,
            args: Dict[str, Any],
            sender: Address, db_session: Session
    ):
        """
        Defines the behaviour of the bot when receiving a message
        :param message: The received message
        :param parser: The parser that matched the message
        :param command: The command that matched the message
        :param args: The arguments of the command
        :param sender: The sender of the message
        :param db_session: The database session to use
        :return: None
        """
        pass

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the bot
        """
        return "bundesliga-tippspiel-reminder"

    @classmethod
    def parsers(cls) -> List[CommandParser]:
        """
        :return: The parsers for the bot
        """
        return [BundesligaTippspielReminderParser()]
