"""
GUI for managing a single tradingview user
"""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class SingleUserPage(tk.Frame):
    """
    Provides GUI for managing a single tradingview user

    Args:
        tk (tk.Frame): Single user GUI tk.Frame
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
            text="Single User Management",
            font=(None, 32, "bold"),
            anchor="center",
        )

        label_page.place(relx=0.5, rely=0.05, anchor="center")

        # Create enter username label
        label_username = ttk.Label(
            master=self, text="Enter Tradingview Username", font=(None, 24)
        )

        label_username.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        # Create enter user input
        manage_user_input = tk.StringVar()

        input_username = ttk.Entry(
            master=self, textvariable=manage_user_input, font=(None, 14)
        )

        input_username.place(
            relx=0.5, rely=0.2, anchor=tk.CENTER, relheight=0.05, relwidth=0.5
        )

        # Create add, check, & remove access button
        button_add = ttk.Button(
            master=self,
            text="ADD",
            style="medium.primary.TButton",
            # command=lambda: threading.Thread(
            # target=lambda: tv_manager(textbox_username.get(), "ADDING PREMIUM")
            # ).start(),
        )

        button_check = ttk.Button(
            master=self,
            text="CHECK",
            style="medium.primary.TButton",
            # command=lambda: threading.Thread(
            # target=lambda: tv_manager(textbox_username.get(), "ADDING PREMIUM")
            # ).start(),
        )

        button_remove = ttk.Button(
            master=self,
            text="REMOVE",
            style="medium.primary.TButton",
            # command=lambda: threading.Thread(
            # target=lambda: tv_manager(textbox_username.get(), "ADDING PREMIUM")
            # ).start(),
        )

        button_add.place(relx=0.25, rely=0.265, relwidth=0.24, anchor=tk.CENTER)
        button_check.place(relx=0.5, rely=0.265, relwidth=0.24, anchor=tk.CENTER)
        button_remove.place(relx=0.75, rely=0.265, relwidth=0.24, anchor=tk.CENTER)

        # Create output textbox
        listbox_output = ScrolledText(
            master=self,
            highlightthickness=1,
        )
        listbox_output.place(
            relx=0.5, rely=0.65, anchor=tk.CENTER, relheight=0.63, relwidth=0.95
        )
