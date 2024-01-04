"""
Tradingview Manage Private Script Access API
"""

# standard imports
import tkinter as tk
from typing import Any

import requests
from requests import Response

# custom imports
from shared.config import ADD_ACCESS_URL, logger
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
            pine_id (str): PUBID for the indicator

        Returns:
            str: _description_
        """
        return_response: str = ""

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
                return_response = f"    ✅ ALREADY HAD ACCESS: {username}"

            elif add_request.status_code == 201:
                return_response = f"    ✅ ADDED: {username}"

            elif add_request.status_code == 422:
                return_response = f"    ❌ TV USERNAME NOT VALID: {username}"

            else:
                return_response = f"    ❌ FAILED TO ADD: {username}"

        except requests.exceptions.RequestException as e:
            logger.error(f"Error trying to validate session ID cookie \n{e}")

        return return_response

    # def remove(self, username: str, pine_id: str) -> None:
    #     return

    # def get(self, username: str, pine_id: str) -> None:
    #     return

    # def get_list(self, pine_id: str) -> None:
    #     return
