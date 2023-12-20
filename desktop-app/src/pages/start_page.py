"""
Start page/frame for tkinter app

Acts as main navigator between managing single user, list of users, or editing indicators
"""

import tkinter as tk
from tkinter import ttk


class StartPage(tk.Frame):
    """
    Allows users to navigate to 3 options
    1. Edit Tradingview Indicators for Managing Access
    2. Manage a single user
    3. Manage a list of users

    Args:
        tk (tk.Frame):
    """

    def __init__(self, parent) -> None:
        super().__init__(master=parent)

        self.pack(fill="both", expand=True)

        # Edit button
        self.edit_indicator_button = ttk.Button(
            master=self,
            text="\nEdit Indicator List\n",
            style="edit.primary.TButton",
            command=lambda: parent.show_frame("edit_indicator_list"),
        )

        self.edit_indicator_button.pack(
            fill="both", padx=300, pady=(75, 0), anchor="center"
        )

        # Manage User button
        self.manage_single_button = ttk.Button(
            master=self,
            text=" Manage User ",
            style="xl.primary.TButton",
            command=lambda: parent.show_frame("manage_single"),
        )

        self.manage_single_button.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(75, 40),
            pady=(125, 75),
            anchor="center",
        )

        # Manage List button
        self.manage_list_button = ttk.Button(
            master=self,
            text="Manage Users \n      with List",
            style="xl.primary.TButton",
            command=lambda: parent.show_frame("manage_list"),
        )

        self.manage_list_button.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(40, 75),
            pady=(125, 75),
            anchor="center",
        )
