"""
GUI for managing a tradingview users with a csv list
"""

# standard imports
import csv
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any

# custom imports
from shared.config import logger
from shared.login import Login
from shared.manage import Manage
from shared.tradingview import Tradingview


class ListPage(tk.Frame):
    """
    Provides GUI for managing tradingview users with a csv list

    Args:
        tk (tk.Frame): List GUI tk.Frame
    """

    def __init__(self, parent: ttk.Frame, login: Login) -> None:
        super().__init__(master=parent)
        self.parent: ttk.Frame = parent
        self.login: Login = login

        self.pack(fill="both", expand=True)

        # Create page label
        label_page = ttk.Label(
            master=self,
            text="List User Management",
            font=(None, 32, "bold"),
            anchor="center",
        )

        label_page.place(relx=0.5, rely=0.05, anchor="center")

        # Create upload list button
        button_upload = ttk.Button(
            master=self,
            text="UPLOAD LIST",
            style="xl.primary.TButton",
            command=lambda: threading.Thread(target=self.list_management()).start(),
        )

        button_upload.place(
            relx=0.5, rely=0.18, relheight=0.12, relwidth=0.6, anchor="center"
        )

        # Create output textbox
        self.listbox_output = tk.Listbox(
            master=self.parent,
            selectmode=tk.SINGLE,
            font=(None, 18),
        )

        self.listbox_output.place(
            relx=0.5, rely=0.62, anchor=tk.CENTER, relheight=0.69, relwidth=0.95
        )

        # Create scrollbar for textbox
        scrollbar = ttk.Scrollbar(
            master=self.parent, orient="vertical", command=self.listbox_output.yview
        )

        scrollbar.place(
            relx=0.97,
            rely=0.62,
            anchor="center",
            relheight=0.69,
            relwidth=0.02,
        )

        self.listbox_output.config(yscrollcommand=scrollbar.set)

    def list_management(self) -> None:
        """
        Handles user file upload flow
        """

        file_path: str = self.user_upload_file()
        if file_path is None or file_path == "":
            return

        csv_contents: list[list[str]] = self.read_user_file(file_path=file_path)
        if not csv_contents:
            return

        username_column_index: int = self.user_select_username_column(
            csv_contents=csv_contents
        )
        if username_column_index is None or username_column_index == 0:
            return

        active_usernames: list[str] = self.get_user_list_from_column_index(
            csv_contents=csv_contents, username_column=username_column_index
        )
        if len(active_usernames) == 0:
            return

        user_confirmed_upload: bool = self.user_confirm_active_list(
            usernames=active_usernames
        )
        if not user_confirmed_upload:
            return

        manage = Manage(parent=self.parent)

        pine_info: list[dict[str, str]] = manage.get_stored_pine_info()
        if len(pine_info) <= 0:
            self.add_to_listbox(
                msg="⚠️ NO INDICATORS AVAILABLE FOR MANAGEMENT", space=False
            )
            return

        tradingview = Tradingview(parent=self.parent, login=self.login)

        for indicator in pine_info:
            self.add_to_listbox(
                msg=f"Indicator:    {indicator['name']}     |   {indicator['url']}",
                space=True,
            )
            self.manage_indicator(
                indicator=indicator,
                active_list=active_usernames,
                tradingview=tradingview,
            )

    def user_select_username_column(self, csv_contents: list[list[str]]) -> int:
        """
        Prompts user to select a column index by name from their uploaded
        csv file

        Args:
            csv_contents (list[list[str]]): CSV file contents

        Returns:
            int: User selected index
        """

        def handle_selection(dialog) -> None:
            dialog.destroy()

        headers: list[str] = csv_contents[0]

        # Create a custom dialog window
        selected_index = tk.IntVar()
        selected_index.set(value=0)

        dialog = tk.Toplevel(master=self.parent)
        dialog.attributes("-topmost", True)
        dialog.resizable(width=False, height=False)
        dialog.title(string="Select Column")

        radio_buttons: list[ttk.Radiobutton] = []
        for i, header in enumerate(iterable=headers[1:], start=1):
            radio_button = ttk.Radiobutton(
                master=dialog,
                text=f"{header.lower()}",
                variable=selected_index,
                value=i,
                padding=(5, 5),
            )

            radio_button.pack(anchor="w", padx=10)
            radio_buttons.append(radio_button)

        ok_button = ttk.Button(
            master=dialog,
            text="OK",
            command=lambda: handle_selection(dialog=dialog),
        )

        ok_button.pack(pady=10)

        dialog.update_idletasks()
        screen_width: int = dialog.winfo_screenwidth()
        screen_height: int = dialog.winfo_screenheight()
        x: int = (screen_width - dialog.winfo_width()) // 2
        y: int = (screen_height - dialog.winfo_height()) // 2
        dialog.geometry(newGeometry=f"+{x}+{y}")

        dialog.grab_set()
        self.parent.wait_window(window=dialog)

        return selected_index.get()

    def user_confirm_active_list(self, usernames: list[str]) -> bool:
        """
        Prompts the user if the list that they uploaded looks correct

        Args:
            usernames (list[str]): List of users

        Returns:
            bool: User input
        """

        if len(usernames) <= 10:
            usernames_to_display: str = ",".join(usernames)
            end_msg: str = ""

        else:
            usernames_to_display: str = ",".join(usernames[:10])
            end_msg: str = "(more not shown)"

        confirm_msg: str = (
            "Is this the list of active members tradingview usernames?"
            f"\n\n{usernames_to_display}\n{end_msg}"
        )

        user_confirmed_upload: bool = messagebox.askyesno(
            title="Valid Uploaded List", message=confirm_msg
        )

        return user_confirmed_upload

    def get_user_list_from_column_index(
        self, csv_contents: list[list[str]], username_column: int
    ) -> list[str]:
        """
        List comprehension of an entire column by a specified index

        Args:
            csv_contents (list[list[str]]): CSV contents
            username_column (int): Column index

        Returns:
            list[str]: All row values by a specified column index
        """

        return [row[username_column].lower() for row in csv_contents[1:]]

    def user_upload_file(self) -> str:
        """
        Prompt user to upload csv file

        Returns:
            str: CSV file path
        """
        return filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    def read_user_file(self, file_path) -> list[list[str]]:
        """
        Converts csv file to a list[list[str]]

        Args:
            file_path (_type_): CSV file_path

        Returns:
            list[list[str]]: CSV file contents
        """

        csv_contents: list[list[str]] = []

        with open(file=file_path, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

            for row in csv_reader:
                csv_contents.append(row)

        return csv_contents

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

    def manage_indicator(
        self,
        indicator: dict[str, str],
        active_list: list[str],
        tradingview: Tradingview,
    ) -> None:
        """
        Retrieves tradingview indicator usernames list and then add/removes after comparing
        to the active uploaded usernames list

        Args:
            indicator (dict[str, str]): Indicator info
            active_list (list[str]): Uploaded list
            tradingview (Tradingview): Tradingview API
        """

        tradingview_list: list[str] = tradingview.get_access_list(
            pine_id=indicator["id"]
        )

        add_list: list[str] = list(set(active_list) - set(tradingview_list))
        remove_list: list[str] = list(set(tradingview_list) - set(active_list))

        if len(add_list) > 0:
            self.add_to_listbox(msg="    ---ADDING---", space=False)
            for user in add_list:
                add_response: str = tradingview.add(
                    username=user, pine_id=indicator["id"]
                )
                self.add_to_listbox(
                    msg=f"{add_response} - {indicator['name']}", space=False
                )
        else:
            self.add_to_listbox(msg="    ---NO ADDITIONS---", space=False)

        if len(remove_list) > 0:
            self.add_to_listbox(msg="    ---REMOVING---", space=False)
            for user in remove_list:
                remove_response: str = tradingview.remove(
                    username=user, pine_id=indicator["id"]
                )
                self.add_to_listbox(
                    msg=f"{remove_response} - {indicator['name']}", space=False
                )
        else:
            self.add_to_listbox(msg="    ---NO REMOVALS---", space=False)
