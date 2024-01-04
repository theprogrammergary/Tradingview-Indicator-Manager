"""
GUI for managing a json list of Tradingview Indicators
"""

# standard imports
import json
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any

# custom imports
from shared.config import INDICATORS_FILE, logger

# from shared.tradingview import Tradingview
from shared.indicators import Indicator


class EditIndicatorsPage(tk.Frame):
    """
    Provides GUI for managing a json list of Tradingview Indicators

    Args:
        tk (tk.Frame): Main GUI tk.Frame
    """

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
        # self.listbox_indicators = ScrolledText(
        #     master=self, highlightthickness=1, state="disabled", font=(None, 18)
        # )

        self.listbox_indicators = tk.Listbox(
            master=self,
            selectmode=tk.SINGLE,
            font=(None, 18),
        )

        self.listbox_indicators.place(
            relx=0.35,
            rely=0.55,
            anchor="center",
            relheight=0.7,
            relwidth=0.65,
        )

        # Create scrollbar for listbox
        scrollbar = ttk.Scrollbar(
            master=self, orient="vertical", command=self.listbox_indicators.yview
        )

        scrollbar.place(
            relx=0.665,
            rely=0.55,
            anchor="center",
            relheight=0.7,
            relwidth=0.02,
        )

        self.listbox_indicators.config(yscrollcommand=scrollbar.set)

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

        self.load_indicators()
        self.update()

    def add_indicator(self) -> None:
        """
        Adds indicator from list for GUI listbox and local storage
        """

        Indicator(parent=self.parent).add_indicator()
        self.load_indicators()

    def remove_indicator(self) -> None:
        """
        Removes indicator from list for GUI listbox and local storage
        """

        def remove_from_listbox() -> None:
            self.listbox_indicators.delete(first=remove_index)

        def remove_from_json() -> None:
            del self.indicators[remove_index]

            with open(
                file=INDICATORS_FILE, mode="w", encoding="utf-8"
            ) as indicators_file:
                json.dump(obj=self.indicators, fp=indicators_file, indent=4)

        selected_index: tuple = self.listbox_indicators.curselection()
        if selected_index:
            remove_index: int = selected_index[0]
            remove_name: str = self.indicators[remove_index]["name"]
            remove_msg: str = (
                f'Are you sure that you want to remove \n\n"{remove_name}"'
            )

            removal_confirmed: bool | None = messagebox.askyesno(
                title="Confirm Removal", message=remove_msg
            )

            if removal_confirmed:
                remove_from_listbox()
                remove_from_json()
                self.load_indicators()

    def load_indicators(self) -> None:
        """
        Reads indicators from local storage and loads them to GUI listbox
        """
        try:
            with open(
                file=INDICATORS_FILE, mode="r", encoding="utf-8"
            ) as indicators_file:
                self.indicators: Any = json.load(fp=indicators_file)

            self.listbox_indicators.delete(first=0, last=tk.END)

            for index, indicator in enumerate(self.indicators, start=1):
                indicator_text: str = f"{index}.     {indicator['name']}"
                self.listbox_indicators.insert(tk.END, indicator_text)

        except FileNotFoundError:
            logger.info("No indicators.json file found")
