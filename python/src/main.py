"""
Tradingview Indicator Access Management Program

    -Can individually manage users for multiple scripts at once
    -Can manage users from a .csv list for multiple sripts at once
"""


# standard imports
import os
import threading
import tkinter as tk
from tkinter import messagebox

# custom imports
import ttkbootstrap as ttk
from pages.edit_indicators import EditIndicatorsPage
from pages.manage_list import ListPage
from pages.manage_single import SingleUserPage
from shared.config import GUI_HEIGHT, GUI_NAME, GUI_WIDTH, RUNTIME_PATH
from shared.login import Login


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

        self.login = Login(parent=self)
        if self.login.logged_in:
            self.create_ui()

        else:
            self.withdraw()
            messagebox.showerror(
                title="Login Failed",
                message="Please login to Tradingview to use the app.",
            )

            self.exit_application()

    def create_ui(self) -> None:
        """
        Create the UI tabs for the application
        """

        self.notebook = ttk.Notebook(master=self)

        edit_indicators_frame: ttk.Frame = ttk.Frame(master=self.notebook)
        single_management_frame: ttk.Frame = ttk.Frame(master=self.notebook)
        list_management_frame: ttk.Frame = ttk.Frame(master=self.notebook)

        self.notebook.add(child=edit_indicators_frame, text="Edit")
        EditIndicatorsPage(parent=edit_indicators_frame, login=self.login)

        self.notebook.add(child=single_management_frame, text="Single User Management")
        SingleUserPage(parent=single_management_frame, login=self.login)

        self.notebook.add(child=list_management_frame, text="List Management")
        ListPage(parent=list_management_frame, login=self.login)

        self.notebook.pack(fill="both", expand=True)

    def exit_application(self) -> None:
        """
        Full closes the application
        """

        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join()
        self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
