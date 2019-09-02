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
from bundesliga_tippspiel_reminder.db.ApiKey import ApiKey
from bundesliga_tippspiel_reminder.BundesligaTippspielReminderParser import \
    BundesligaTippspielReminderParser
from bundesliga_tippspiel_reminder.api import api_request, is_authorized, \
    get_api_key


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
            sender: Address,
            db_session: Session
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
        if command == "login":
            self._handle_login(sender, args, db_session)
        elif command == "is_authorized":
            self._handle_is_authorized(sender, db_session)
        elif command == "leaderboard":
            self._handle_leaderboard(sender, db_session)

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

    @classmethod
    def extra_config_args(cls) -> List[str]:
        """
        :return: A list of additional settings parameters required for
                 this bot. Will be stored in a separate extras.json file
        """
        return []

    def _handle_login(
            self,
            sender: Address,
            args: Dict[str, Any],
            db_session: Session
    ):
        """
        Handles a login command
        :param sender: The sender of the message
        :param args: The command arguments
        :param db_session: The database session
        :return: None
        """

        data = {"username": args["username"], "password": args["password"]}
        response = api_request("api_key", "post", data)
        print(response)

        if response["status"] == "ok":
            key = ApiKey(
                kudubot_user=sender,
                tippspiel_user=args["username"],
                key=response["data"]["api_key"]
            )
            db_session.add(key)
            db_session.commit()
            reply = "Logged in successfully"
        else:
            reply = "Login unsuccessful"

        reply = TextMessage(self.connection.address, sender, reply, "Login")
        self.connection.send(reply)

    def _handle_is_authorized(self, sender: Address, db_session: Session):
        """
        Handles an is_authorized command
        :param sender: The sender of the message
        :param db_session: The database session to use
        :return: None
        """
        reply = "yes" if is_authorized(sender, db_session) else "no"
        self.connection.send(TextMessage(
            self.connection.address, sender, reply, "Authorized"
        ))

    def _authorization_check(self, sender: Address, db_session: Session) \
            -> bool:
        """
        Checks whether or not the sender is authorized.
        If the user is not authorized, a message is sent detailing this
        :param sender: The sender to check
        :param db_session: The database session to use
        :return: True if authorized, False if not
        """
        authorized = is_authorized(sender, db_session)
        if not authorized:
            self.connection.send(TextMessage(
                self.connection.address,
                sender,
                "Not authorized, use /login <username> <password> first",
                "Not authorized"
            ))
        return authorized

    def _handle_leaderboard(self, sender: Address, db_session: Session):
        """
        Handles a leaderboard command
        :param sender: The sender of the message
        :param db_session: The database session to use
        :return: None
        """
        if not self._authorization_check(sender, db_session):
            return

        api_key = get_api_key(sender, db_session)
        response = api_request("leaderboard", "get", {}, api_key)
        print(response)
        if response["status"] == "ok":
            leaderboard = response["data"]["leaderboard"]
            formatted = []
            for i, (user, points) in enumerate(leaderboard):
                formatted.append("{}: {} ({})".format(
                    i + 1,
                    user["username"],
                    points
                ))

            reply = "\n".join(formatted)
            self.connection.send(TextMessage(
                self.connection.address, sender, reply, "Leaderboard"
            ))
