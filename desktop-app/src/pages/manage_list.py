"""
GUI for managing a tradingview users with a csv list
"""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class ListPage(tk.Frame):
    """
    Provides GUI for managing tradingview users with a csv list

    Args:
        tk (tk.Frame): List GUI tk.Frame
    """

    def __init__(self, parent) -> None:
        super().__init__(master=parent)

        self.pack(fill="both", expand=True)

        # Create back to start page button
        button_back = ttk.Button(
            master=self,
            text="Go Back",
            style="medium.primary.TButton",
            command=lambda: parent.show_frame("start_page"),
        )

        button_back.place(
            relx=0.02,
            rely=0.02,
        )

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
            # command=lambda: threading.Thread(
            # target=lambda: tv_manager(textbox_username.get(), "ADDING PREMIUM")
            # ).start(),
        )

        button_upload.place(
            relx=0.5, rely=0.18, relheight=0.12, relwidth=0.6, anchor="center"
        )

        # Create output textbox
        listbox_output = ScrolledText(
            master=self, highlightthickness=1, state="normal", font=(None, 18)
        )
        listbox_output.place(
            relx=0.5, rely=0.62, anchor=tk.CENTER, relheight=0.68, relwidth=0.95
        )

        # Create scrollbar for textbox
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=listbox_output.yview)

        scrollbar.place(
            relx=0.97,
            rely=0.62,
            anchor="center",
            relheight=0.68,
            relwidth=0.02,
        )

        listbox_output.config(yscrollcommand=scrollbar.set)
