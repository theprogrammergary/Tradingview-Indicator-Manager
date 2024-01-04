"""
Tradingview Manage Private Script Access API
"""

# standard imports
import json
import tkinter as tk
from typing import Any

import requests
from requests import Response

# custom imports
from shared.config import (
    ADD_ACCESS_URL,
    REMOVE_ACCESS_URL,
    USER_ACCESS_LIST_URL,
    logger,
)
from shared.login import TradingviewLogin
from urllib3 import encode_multipart_formdata


class Tradingview(tk.Frame):
    """
    API for Managing Private Indicators on Tradingview
    """

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(master=parent)
        self.parent: tk.Tk = parent
        self.login()

    def login(self) -> None:
        """
        Ensures current session ID is valid or prompts user to re-login to capture
        a new session ID cookie
        """
        self.tradingview_login = TradingviewLogin(parent=self.parent)
        self.session_id: str | None = self.tradingview_login.read_saved_session_id()

    def add(self, username: str, pine_id: str) -> str:
        """
        Adds user to indicator access

        Args:
            username (str):
            pine_id (str): PUB ID for the indicator

        Returns:
            str: status
        """

        try:
            payload: dict[str, Any] = {
                "pine_id": pine_id,
                "username_recip": username,
                "noExpiration": True,
            }

            _, content_type = encode_multipart_formdata(fields=payload)

            headers: dict[str, str] = {
                "origin": "https://www.tradingview.com",
                "Content-Type": content_type,
                "cookie": (f"sessionid={self.session_id}"),
            }

            add_request: Response = requests.post(
                url=ADD_ACCESS_URL, headers=headers, timeout=5000
            )

            if add_request.status_code == 200:
                return f"    ✅ ALREADY HAD ACCESS: {username}"

            elif add_request.status_code == 201:
                return f"    ✅ ADDED: {username}"

            elif add_request.status_code == 422:
                return f"    ❌ TV USERNAME NOT VALID: {username}"

            else:
                return f"    ❌ FAILED TO ADD: {username}"

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error trying to add\n"
                f"USERNAME: {username}\n"
                f"PINE_ID: {pine_id}\n"
                f"SESSION_ID: {self.session_id}\n"
                f"{e}"
            )

            return f"    ❗️ ERROR IN ADDING: {username} "

    def remove(self, username: str, pine_id: str) -> str:
        """
        Remove user from indicator access

        Args:
            username (str):
            pine_id (str): PUB ID for the indicator

        Returns:
            str: status
        """

        try:
            payload: dict[str, Any] = {
                "pine_id": pine_id,
                "username_recip": username,
                "noExpiration": True,
            }

            _, content_type = encode_multipart_formdata(fields=payload)

            headers: dict[str, str] = {
                "origin": "https://www.tradingview.com",
                "Content-Type": content_type,
                "cookie": (f"sessionid={self.session_id}"),
            }

            remove_request: Response = requests.post(
                url=REMOVE_ACCESS_URL, headers=headers, timeout=5000
            )

            if remove_request.status_code == 200 or remove_request.status_code == 201:
                return f"    ✅ REMOVED: {username}"

            elif remove_request.status_code == 422:
                return f"    ❌ TV USERNAME NOT VALID: {username}"

            else:
                return f"    ❌ FAILED TO REMOVE: {username}"

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error trying to remove\n"
                f"USERNAME: {username}\n"
                f"PINE_ID: {pine_id}\n"
                f"SESSION_ID: {self.session_id}\n"
                f"{e}"
            )

            return f"    ❗️ ERROR IN REMOVING: {username} "

    def get(self, username: str, pine_id: str) -> str:
        """
        Gets indicator access for a username

        Args:
            username (str):
            pine_id (str): PUB ID for the indicator

        Returns:
            str: status
        """

        try:
            payload: dict[str, Any] = {
                "pine_id": pine_id,
                "username_recip": username,
            }

            _, content_type = encode_multipart_formdata(fields=payload)

            headers: dict[str, str] = {
                "origin": "https://www.tradingview.com",
                "Content-Type": content_type,
                "cookie": (f"sessionid={self.session_id}"),
            }

            request: Response = requests.post(
                url=USER_ACCESS_LIST_URL, headers=headers, timeout=5000
            )

            request_json = request.json()
            current_access_list = request_json["results"]
            has_access = False

            for user in current_access_list:
                if user["username"].lower() == username.lower():
                    has_access = True

            if has_access:
                return "    ✅ HAS ACCESS"

            else:
                return "    ❌ NO ACCESS"

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error trying to get access\n"
                f"USERNAME: {username}\n"
                f"PINE_ID: {pine_id}\n"
                f"SESSION_ID: {self.session_id}\n"
                f"{e}"
            )

            return f"    ❗️ ERROR IN GETTING ACCESS: {username} "

    def get_access_list(self, pine_id: str) -> list[str]:
        """
        Returns a list of usernames that have access to an indicator

        Args:
            pine_id (str): The PUB ID of the indicator

        Returns:
            list[str]: List of users who currently have access
        """

        user_list: list[str] = []
        try:
            payload: dict[str, Any] = {
                "pine_id": pine_id,
            }

            body, content_type = encode_multipart_formdata(fields=payload)

            headers: dict[str, str] = {
                "origin": "https://www.tradingview.com",
                "Content-Type": content_type,
                "cookie": (f"sessionid={self.session_id}"),
            }

            counter = 1
            user_count = 1
            next_url = "/pine_perm/list_users/?limit=10&order_by=user__username"

            while next_url is not None:
                request: Response = requests.post(
                    url=("https://www.tradingview.com" + next_url),
                    data=body,
                    headers=headers,
                    timeout=5000,
                )
                request_json: Any = json.loads(s=request.content)
                body_dict: dict = request_json["results"]

                for user in body_dict:
                    user_count += 1
                    user_list.append(user["username"].lower())

                if "next" in request_json:
                    next_url: str = request_json["next"]
                    counter += 1

                else:
                    break

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error trying to get user list\n"
                f"PINE_ID: {pine_id}\n"
                f"SESSION_ID: {self.session_id}\n"
                f"{e}"
            )

        return user_list
