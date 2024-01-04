"""
GUI for managing a json list of Tradingview Indicators
"""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from shared.tradingview import Tradingview


class EditIndicatorsPage(tk.Frame):
    def __init__(self, parent) -> None:
        self.parent: tk.Tk = parent
        super().__init__(master=parent)

        self.pack(fill="both", expand=True)

        # Create back button
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
            text="Edit Tradingview Indicator List",
            font=(None, 32, "bold"),
            anchor="center",
        )

        label_page.place(relx=0.5, rely=0.05, anchor="center")

        # Create listbox to display indicators
        listbox_indicators = ScrolledText(
            master=self, highlightthickness=1, state="disabled", font=(None, 18)
        )

        listbox_indicators.place(
            relx=0.35,
            rely=0.55,
            anchor="center",
            relheight=0.7,
            relwidth=0.65,
        )

        # Create scrollbar for listbox
        scrollbar = ttk.Scrollbar(
            master=self, orient="vertical", command=listbox_indicators.yview
        )

        scrollbar.place(
            relx=0.665,
            rely=0.55,
            anchor="center",
            relheight=0.7,
            relwidth=0.02,
        )

        listbox_indicators.config(yscrollcommand=scrollbar.set)

        # Create Add button
        button_add = ttk.Button(
            master=self,
            text="     Add\nIndicator",
            style="xl.primary.TButton",
            command=self.add_indicator,
        )

        button_add.place(
            relx=0.835, rely=0.38, relwidth=0.25, relheight=0.3, anchor="center"
        )

        # Create Remove button
        button_remove = ttk.Button(
            master=self,
            text="Remove\nIndicator",
            style="xl.primary.TButton",
            command=self.remove_indicator,
        )

        button_remove.place(
            relx=0.835, rely=0.72, relwidth=0.25, relheight=0.3, anchor="center"
        )

    def add_indicator(self) -> None:
        Tradingview(parent=self.parent)

    def remove_indicator(self) -> None:
        # Implement logic to remove an indicator
        pass
