"""
Handles adding indicators to the indicators.json list
"""

# standard imports
import json
import tkinter as tk
from tkinter import messagebox, ttk

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# custom imports
from shared.config import (
    INDICATORS_FILE,
    MESSAGE_HEIGHT,
    MESSAGE_WIDTH,
    PINE_ID_SELECTOR,
    PINE_NAME_SELECTOR,
    logger,
)
from shared.login import Login


class Indicator(tk.Frame):
    """
    Handles adding indicators to the indicators.json list
    """

    def __init__(self, parent: ttk.Frame, login: Login) -> None:
        super().__init__(master=parent)
        self.parent: ttk.Frame = parent
        self.login: Login = login

    def add_indicator(self) -> None:
        """
        Event driver for adding an indicator to json list / listbox GUI
        """

        url: str = self.ask_for_url()
        if url is None:
            return

        message_box: tk.Toplevel | None = None
        web_driver: WebDriver | None = self.create_browser()

        try:
            message_box = self.create_message_box(
                title="Fetching Info", msg="Fetching Indicator Info. Please wait."
            )

            if web_driver is None:
                return

            valid_url: bool = url.startswith("https://www.tradingview.com/script")

            if valid_url:
                pine_name: str | None = None
                pine_id: str | None = None

                pine_name, pine_id = self.get_pine_info(url=url, web_driver=web_driver)

                print(pine_name)
                print(pine_id)
                valid_pine_info: bool = (
                    pine_name is not None
                    and pine_id is not None
                    and pine_name != ""
                    and pine_id != ""
                )

                if valid_pine_info:
                    new_entry: dict[str, str | None] = {
                        "name": pine_name,
                        "url": url,
                        "id": pine_id,
                    }

                    self.update_json_list(new_entry=new_entry)

        finally:
            # if web_driver is not None:
            # web_driver.quit()

            if message_box is not None:
                message_box.destroy()

    def update_json_list(self, new_entry: dict[str, str | None]) -> None:
        """
        Add new indicator to indicators.json list

        Args:
            new_entry (dict[str, str | None]): New indicator info
        """

        data: list[dict] = []

        try:
            with open(file=INDICATORS_FILE, mode="r", encoding="utf-8") as file:
                data = json.load(fp=file)
        except FileNotFoundError:
            logger.error("INDICATORS_FILE not found")

        data.append(new_entry)

        with open(file=INDICATORS_FILE, mode="w", encoding="utf-8") as file:
            json.dump(obj=data, fp=file, indent=4)

    def get_pine_info(
        self, url: str, web_driver: WebDriver
    ) -> tuple[str | None, str | None]:
        """
        Scraps user given URL for pine indicator name and pub ID key

        Args:
            url (str): URL to scrape
            web_driver (WebDriver): Selenium Web Driver

        Returns:
            tuple[str | None, str | None]: pine_name, pine_id
        """

        pine_name: str | None = None
        pine_id: str | None = None

        def get_pine_name() -> str | None:
            try:
                element: WebElement = WebDriverWait(driver=web_driver, timeout=5).until(
                    method=EC.element_to_be_clickable(
                        mark=(By.CSS_SELECTOR, PINE_NAME_SELECTOR)
                    )
                )

                pine_name: str | None = element.text

                return pine_name

            except TimeoutException:
                logger.error("Unable to find pine name")

                return None

        def get_pine_id() -> str | None:
            try:
                element: WebElement = WebDriverWait(driver=web_driver, timeout=5).until(
                    method=EC.element_to_be_clickable(
                        mark=(By.CSS_SELECTOR, PINE_ID_SELECTOR)
                    )
                )

                data_script_id_part: str | None = element.get_attribute(
                    name="data-script-id-part"
                )

                return data_script_id_part

            except TimeoutException:
                logger.error("Unable to find pine ID")

                return None

        web_driver.get(url=url)
        pine_name = get_pine_name()
        pine_id = get_pine_id()

        return pine_name, pine_id

    def create_browser(self) -> WebDriver | None:
        """
        Creates a Selenium Web Driver to capture
        PUB ID or indicator ID

        Returns:
            WebDriver | None: A Selenium Web Driver
        """

        web_driver: WebDriver | None = self.login.headless_web

        if web_driver is None:
            messagebox.showerror(
                title="ERROR",
                message=(
                    "ERROR: Unable to create Chrome Browser. \n\nPlease make sure "
                    "that you have Google Chrome installed."
                ),
            )
            return None

        session_id: str | None = self.login.read_saved_session_id()

        web_driver.get(url="https://www.tradingview.com/u/#published-scripts")

        if session_id:
            cookie: dict[str, str] = {
                "name": "sessionid",
                "value": session_id,
                "domain": ".tradingview.com",
                "path": "/",
            }
            web_driver.add_cookie(cookie_dict=cookie)

        return web_driver

    def ask_for_url(self) -> str:
        """
        Creates a dialog window for user to enter a tradingview indicator URL

        Returns:
            str | None: User entered url
        """
        entered_url = tk.StringVar()

        def get_input() -> None:
            entered_url.set(value=entry.get())
            dialog.destroy()

        # Create input GUI
        dialog = tk.Toplevel(master=self.parent)
        screen_width: int = dialog.winfo_screenwidth()
        screen_height: int = dialog.winfo_screenheight()
        x: int = int((screen_width - MESSAGE_WIDTH) // 2)
        y: int = int(((screen_height - MESSAGE_HEIGHT) // 2))

        dialog.attributes("-topmost", True)
        dialog.resizable(width=False, height=False)
        dialog.title(string="Enter Indicator URL")
        dialog.geometry(newGeometry=f"{MESSAGE_WIDTH}x{MESSAGE_HEIGHT}+{x}+{y}")

        entry = ttk.Entry(master=dialog)
        entry.place(relx=0.5, rely=0.3, relheight=0.35, relwidth=0.95, anchor="center")
        entry.insert(
            0, "https://www.tradingview.com/script/fllPsRHH-Testing-Invite-Only/"
        )

        ok_button = ttk.Button(master=dialog, text="OK", command=get_input)
        ok_button.place(relx=0.5, rely=0.72, relwidth=0.3, anchor="center")

        # dialog.transient(master=self.parent)
        dialog.grab_set()
        self.parent.wait_window(window=dialog)

        return entered_url.get()

    def create_message_box(self, title: str, msg: str) -> tk.Toplevel:
        """
        Shows a custom message box
        """

        # Create message box
        message_box = tk.Toplevel(master=self.parent)
        screen_width: int = message_box.winfo_screenwidth()
        screen_height: int = message_box.winfo_screenheight()
        height_offset: int = int(message_box.winfo_screenheight() * 0.2)
        x: int = int((screen_width - MESSAGE_WIDTH) // 2)
        y: int = int(((screen_height - MESSAGE_HEIGHT) // 2) - height_offset)

        message_box.attributes("-topmost", True)
        message_box.resizable(width=False, height=False)
        message_box.title(string=title)
        message_box.geometry(newGeometry=f"{MESSAGE_WIDTH}x{MESSAGE_HEIGHT}+{x}+{y}")

        # Create message
        message_label = tk.Label(
            master=message_box,
            text=msg,
            font=(None, 16),
        )

        message_label.place(relx=0.5, rely=0.5, anchor="center")

        # self.parent.withdraw()
        message_box.lift()
        message_box.update()

        return message_box
