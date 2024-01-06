"""
GUI for managing a single tradingview user
"""

# standard imports
import threading
import tkinter as tk
from tkinter import ttk
from typing import Any

# custom imports
from shared.config import logger
from shared.login import Login
from shared.manage import Manage
from shared.tradingview import Tradingview


class SingleUserPage(tk.Frame):
    """
    Provides GUI for managing a single tradingview user

    Args:
        tk (tk.Frame): Single user GUI tk.Frame
    """

    def __init__(self, parent: ttk.Frame, login: Login) -> None:
        super().__init__(master=parent)
        self.parent: ttk.Frame = parent
        self.login: Login = login
        self.manage = Manage(parent=self.parent)
        self.pack(fill="both", expand=True)

        # Create page label
        label_page = ttk.Label(
            master=self.parent,
            text="Single User Management",
            font=(None, 32, "bold"),
            anchor="center",
        )

        label_page.place(relx=0.5, rely=0.05, anchor="center")

        # Create enter username label
        label_username = ttk.Label(
            master=self.parent, text="Enter Tradingview Username", font=(None, 24)
        )

        label_username.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        # Create enter user input
        manage_user_input = tk.StringVar()

        input_username = ttk.Entry(
            master=self.parent, textvariable=manage_user_input, font=(None, 18)
        )

        input_username.place(
            relx=0.5, rely=0.2, anchor=tk.CENTER, relheight=0.05, relwidth=0.5
        )

        # Create add, check, & remove access button
        button_add = ttk.Button(
            master=self.parent,
            text="ADD",
            style="medium.primary.TButton",
            command=lambda: threading.Thread(
                target=lambda: self.add_user(username=input_username.get())
            ).start(),
        )

        button_check = ttk.Button(
            master=self.parent,
            text="CHECK",
            style="medium.primary.TButton",
            command=lambda: threading.Thread(
                target=lambda: self.get_user(username=input_username.get())
            ).start(),
        )

        button_remove = ttk.Button(
            master=self.parent,
            text="REMOVE",
            style="medium.primary.TButton",
            command=lambda: threading.Thread(
                target=lambda: self.remove_user(username=input_username.get())
            ).start(),
        )

        button_add.place(
            relx=0.25, rely=0.265, relwidth=0.24, relheight=0.05, anchor=tk.CENTER
        )
        button_check.place(
            relx=0.5, rely=0.265, relwidth=0.24, relheight=0.05, anchor=tk.CENTER
        )
        button_remove.place(
            relx=0.75, rely=0.265, relwidth=0.24, relheight=0.05, anchor=tk.CENTER
        )

        # Create output textbox
        self.listbox_output = tk.Listbox(
            master=self.parent,
            selectmode=tk.SINGLE,
            font=(None, 18),
        )

        self.listbox_output.place(
            relx=0.5, rely=0.65, anchor=tk.CENTER, relheight=0.63, relwidth=0.95
        )

        # Create scrollbar for textbox
        scrollbar = ttk.Scrollbar(
            master=self.parent, orient="vertical", command=self.listbox_output.yview
        )

        scrollbar.place(
            relx=0.97,
            rely=0.65,
            anchor="center",
            relheight=0.63,
            relwidth=0.02,
        )

        self.listbox_output.config(yscrollcommand=scrollbar.set)

        self.tradingview = Tradingview(parent=self.parent, login=self.login)

    def add_user(self, username: str) -> None:
        """
        Adds a single user to a list of tradngview indicators

        Args:
            username (str): User to be added
        """

        self.add_to_listbox(msg=f"ADDING ACCESS: {username}", space=True)

        pine_info: list[dict[str, str]] = self.manage.get_stored_pine_info()
        if len(pine_info) <= 0:
            self.add_to_listbox(
                msg="⚠️ NO INDICATORS AVAILABLE FOR MANAGEMENT", space=False
            )
            return

        for indicator in pine_info:
            response: str = self.tradingview.add(
                username=username, pine_id=indicator["id"]
            )

            self.add_to_listbox(msg=f"{response} - {indicator['name']}", space=False)

    def remove_user(self, username: str) -> None:
        """
        Removes a single user to a list of tradngview indicators

        Args:
            username (str): User to be removed
        """

        self.add_to_listbox(msg=f"REMOVING ACCESS: {username}", space=True)

        pine_info: list[dict[str, str]] = self.manage.get_stored_pine_info()
        if len(pine_info) <= 0:
            self.add_to_listbox(
                msg="⚠️ NO INDICATORS AVAILABLE FOR MANAGEMENT", space=False
            )
            return

        for indicator in pine_info:
            response: str = self.tradingview.remove(
                username=username, pine_id=indicator["id"]
            )

            self.add_to_listbox(msg=f"{response} - {indicator['name']}", space=False)

    def get_user(self, username: str) -> None:
        """
        Gets current access for a single user to a list of tradngview indicators

        Args:
            username (str): User to be checked
        """

        self.add_to_listbox(msg=f"CHECKING ACCESS: {username}", space=True)

        pine_info: list[dict[str, str]] = self.manage.get_stored_pine_info()
        if len(pine_info) <= 0:
            self.add_to_listbox(
                msg="⚠️ NO INDICATORS AVAILABLE FOR MANAGEMENT", space=False
            )
            return

        for indicator in pine_info:
            response: str = self.tradingview.get(
                username=username, pine_id=indicator["id"]
            )

            self.add_to_listbox(msg=f"{response} - {indicator['name']}", space=False)

    def add_to_listbox(self, msg: str, space: bool) -> None:
        """
        Adds a log message to the GUI

        Args:
            msg (str): Message to display
            space (bool): If true puts a line space before
        """

        logger.info(msg)

        selected_item: Any = self.listbox_output.get(tk.ACTIVE)
        if space and selected_item is not None and selected_item != "":
            self.listbox_output.insert(tk.END, " ")

        self.listbox_output.insert(tk.END, msg)
        self.listbox_output.selection_clear(first=0, last=tk.END)
        self.listbox_output.select_set(first=tk.END)
        self.listbox_output.see(index=tk.END)

        self.update()
