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

import json
import requests
from base64 import b64encode
from typing import Dict, Any, Optional
from kudubot.db.Address import Address
from sqlalchemy.orm import Session
from bundesliga_tippspiel_reminder.db.ApiKey import ApiKey


def api_request(
        endpoint: str,
        method: str,
        params: Dict[Any, Any],
        api_key: Optional[str] = None
) -> Dict[Any, Any]:
    """
    Sends a request to the API
    :param endpoint: The endpoint to send the request to
    :param method: The HTTP method to use
    :param params: The parameters to use
    :param api_key: The API key to use
    :return: The response
    """
    url = "https://hk-tippspiel.com/api/v2/" + endpoint

    headers = {}
    if api_key is not None:
        encoded = b64encode(api_key.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": "Basic {}".format(encoded)
        }

    return json.loads(requests.request(
        method,
        url,
        headers=headers,
        json=params,
    ).text)


def is_authorized(address: Address, db_session: Session) -> bool:
    """
    Checks whether or not the address is authorized
    :param address: The address to check
    :param db_session: The database session to use
    :return: True if authorized, False otherwise
    """
    api_key = get_api_key(address, db_session)
    if api_key is None:
        return False
    else:
        resp = api_request("authorize", "get", {}, api_key)
        return resp["status"] == "ok"


def get_api_key(address: Address, db_session: Session) -> Optional[str]:
    """
    Retrieves the API key for an address
    :param address: The address for which to get the API key
    :param db_session: The database session to use
    :return: The API key, or None if no API key exists
    """
    api_key = db_session.query(ApiKey).filter_by(kudubot_user=address).first()
    return None if api_key is None else api_key.key
