"""
Tradingview Indicator Access Management Program

    -Can individually manage users for multiple scripts at once
    -Can manage users from a .csv list for multiple sripts at once
"""

# standard imports
import os
import tkinter as tk
from tkinter import messagebox
from typing import Any

# custom imports
import ttkbootstrap as ttk
from config import GUI_HEIGHT, GUI_NAME, GUI_WIDTH, RUNTIME_PATH

# from pages.edit_indicators import StartPage
from pages.manage_list import ListPage
from pages.manage_single import SingleUserPage
from pages.start_page import StartPage


class MainApplication(tk.Tk):
    """
    Tk application for Tradingview Indicator Access Management
    """

    def __init__(self) -> None:
        super().__init__()

        # Create GUI styles
        style = ttk.Style(theme="darkly")
        style.configure(style="edit.primary.TButton", font=(None, 18))
        style.configure(style="xl.primary.TButton", font=(None, 35))
        style.configure(style="medium.primary.TButton", font=(None, 16))
        style.configure(style="upload.primary.TButton", font=(None, 16))

        # Create GUI frame
        screen_width: int = self.winfo_screenwidth()
        screen_height: int = self.winfo_screenheight()
        x: int = int((screen_width - GUI_WIDTH) // 2)
        y: int = int((screen_height - GUI_HEIGHT) // 2)
        self.geometry(newGeometry=f"{GUI_WIDTH}x{GUI_HEIGHT}+{x}+{y}")
        self.resizable(width=False, height=False)
        # self.wm_attributes("-topmost", True)

        # Create GUI name/styling
        self.title(string=GUI_NAME)
        icon_path: str = os.path.join(RUNTIME_PATH, "..", ".setup", "tv_round.png")
        icon = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, icon)

        # Create the start page
        self.start_page = StartPage(parent=self)
        self.start_page.pack()

    def show_frame(self, frame_name) -> None:
        """
        Shows the frame based on the provided frame_name.

        Args:
            frame_name (str): The name of the frame to be shown.
        """

        frame_mapping: dict[str, Any] = {
            "manage_list": ListPage,
            "manage_single": SingleUserPage,
            "start_page": StartPage,
        }

        if frame_name in frame_mapping:
            new_frame = frame_mapping[frame_name](parent=self)

            if self.start_page is not None:
                self.start_page.pack_forget()

            new_frame.pack()
            self.start_page: tk.Frame = new_frame

        else:
            error_message: str = f"Frame '{frame_name}' not found."
            messagebox.showerror(title="Error", message=error_message)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
