"""
Shared helper functions for managaing tradingview user access
"""

# standard imports
import json
import tkinter as tk
from tkinter import ttk
from typing import Any

# custom imports
from shared.config import INDICATORS_FILE, logger


class Manage(tk.Frame):
    """
    Shared helper functions for managaing tradingview user access

    Args:
        tk (tk.Frame): Single user GUI tk.Frame
    """

    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(master=parent)
        self.parent: ttk.Frame = parent

    def get_pine_ids(self) -> list[str]:
        """
        Gets the list of pine_ids for management

        Returns:
            list[str]: Pine IDs
        """

        pine_ids: list[str] = []

        try:
            with open(
                file=INDICATORS_FILE, mode="r", encoding="utf-8"
            ) as indicators_file:
                indicators: Any = json.load(fp=indicators_file)

            for indicator in indicators:
                pine_ids.append(indicator["id"])

            return pine_ids

        except FileNotFoundError:
            logger.info("No indicators.json file found")
            return pine_ids

    def get_stored_pine_info(self) -> list[dict[str, str]]:
        """
        Gets the json list of indicator info

        Returns:
            list[dict[str, str]]:
        """

        pine_info: list[dict[str, str]] = []

        try:
            with open(
                file=INDICATORS_FILE, mode="r", encoding="utf-8"
            ) as indicators_file:
                pine_info = json.load(fp=indicators_file)

                return pine_info

        except FileNotFoundError:
            logger.info("No indicators.json file found")
            return pine_info
