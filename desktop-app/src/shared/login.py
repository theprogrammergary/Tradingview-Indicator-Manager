"""
Handles verifying/creating tradingview login session ID
"""

# standard imports
import json
import time
import tkinter as tk
from tkinter import messagebox
from typing import Any, List

import chromedriver_autoinstaller
import requests
from requests import Response
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

# custom imports
from shared.config import (
    LOGIN_CHECK_URL,
    MESSAGE_HEIGHT,
    MESSAGE_WIDTH,
    SESSION_FILE,
    logger,
)


class TradingviewLogin(tk.Frame):
    """
    Handles verifying/creating tradingview login session ID
    """

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(master=parent)
        self.parent: tk.Tk = parent
        self.login()

    def login(self) -> bool:
        """
        Entry for class to check the current saved session ID or create a new sesison ID

        Returns:
            bool: Is a valid session ID set?
        """

        session_id: str | None = self.read_saved_session_id()

        if session_id is None or not self.validate_session_id(session_id=session_id):
            user_login_status: int = self.user_tradingview_login()

            return user_login_status == 0

        return True

    def save_session_id(self, session_id: str) -> None:
        """
        Saves session ID to env vars

        Args:
            session_id (str): The ID to be saved
        """

        data: dict[str, str] = {"session_id": session_id}
        with open(file=SESSION_FILE, mode="w", encoding="utf-8") as file:
            json.dump(obj=data, fp=file)

    def read_saved_session_id(self) -> str | None:
        """
        Retrieves the current saved session ID

        Returns:
            str | None: The read ID
        """

        try:
            with open(file=SESSION_FILE, mode="r", encoding="utf-8") as file:
                data: dict[str, str] = json.load(fp=file)
                return data.get("session_id")
        except FileNotFoundError:
            return None

    def create_selenium_webdriver(self) -> WebDriver | None:
        """Creates the browser for user tradingview login.

        Returns:
            WebDriver: Webdriver for user login
        """

        options = Options()
        options.add_argument(argument="--window-size=1920,1200")
        options.add_argument(argument="--disable-blink-features=AutomationControlled")

        web_driver: WebDriver | None = None

        try:
            web_driver = WebDriver(options=options)
        except Exception as e:  # pylint: disable=W0718
            logger.error(
                f"Failed to create driver. Trying now with chromedriver_autoinstaller\n {e}"
            )

            try:
                chromedriver_autoinstaller.install()
                web_driver = WebDriver(options=options)
            except Exception as e2:  # pylint: disable=W0718
                logger.error(
                    f"Failed to create selenium driver with chromedriver_autoinstaller.\n {e2}"
                )
                return None

        return web_driver

    def search_for_cookie(self, web_driver: WebDriver) -> str | None:
        """
        Searches every 2 seconds for the tradingview sessionid cookie.
        Stops after 2 minutes.

        Args:
            web_driver (WebDriver): Selenium webdriver

        Returns:
            str | None: The session ID cookie as a string or none if it is not found
        """

        def update_message_box_countdown(message_box, max_duration, start_time) -> None:
            time.sleep(1)
            time_remaining: int = round(max_duration - (time.time() - start_time))
            new_msg: str = (
                f"Waiting for Tradingview Session ID...\n\n"
                f"Time Remaining to Login {time_remaining}"
            )

            self.update_message_box_text(
                message_box=message_box,
                new_msg=new_msg,
            )

        searching_message_box: tk.Toplevel = self.create_message_box(
            title="Tradingview Login", msg="Waiting for Tradingview Session ID..."
        )

        start_time: float = time.time()
        max_duration: int = 180
        last_test_cookie: str = ""
        cookie_value: str | None = None

        try:
            while time.time() - start_time < max_duration:
                cookies: List[dict[Any, Any]] = web_driver.get_cookies()

                for cookie in cookies:
                    tv_cookie_found: bool = (
                        cookie["domain"] == ".tradingview.com"
                        and cookie["name"] == "sessionid"
                    )

                    if tv_cookie_found:
                        new_cookie_found: bool = cookie["value"] != last_test_cookie

                        if not new_cookie_found:
                            continue

                        cookie_is_valid: bool = self.validate_session_id(
                            session_id=cookie["value"]
                        )

                        if cookie_is_valid:
                            cookie_value = cookie["value"]
                            break

                if cookie_value is not None:
                    break

                update_message_box_countdown(
                    message_box=searching_message_box,
                    max_duration=max_duration,
                    start_time=start_time,
                )

        finally:
            self.close_message_box(message_box=searching_message_box)

        return cookie_value

    def validate_session_id(self, session_id: str) -> bool:
        """
        Checks the extracted cookie to see if it is actually a valid session ID

        Args:
            session_id (str): The test cookie

        Returns:
            bool: Cookie is valid
        """
        headers: dict[str, str] = {"cookie": (f"sessionid={session_id}")}

        try:
            login_request: Response = requests.get(
                url=LOGIN_CHECK_URL, headers=headers, timeout=5000
            )

            if login_request.status_code == 200:
                return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Error trying to validate session ID cookie \n{e}")

        return False

    def user_tradingview_login(self) -> int:
        """
        Manual user login that captures Tradingview Session ID for Tradingview API

        Returns:
            int:
            3 = Session ID is none
            2 = Error creating driver,
            1 = Error in login process,
            0 = Success
        """

        web_driver: WebDriver | None = self.create_selenium_webdriver()
        if web_driver is None:
            messagebox.showerror(
                title="ERROR",
                message=(
                    "ERROR: Unable to create Chrome Browser. \n\nPlease make sure "
                    "that you have Google Chrome installed."
                ),
            )
            return 2

        web_driver.get(url="https://www.tradingview.com/u/")

        session_id: str | None = self.search_for_cookie(web_driver=web_driver)

        if session_id is None:
            messagebox.showerror(
                title="ERROR Tradingview Login", message="Session ID not found."
            )
            return 3

        success_message: str = "Login Successful! \n\nYou can now manage user access."
        messagebox.showinfo(title="Tradingview Login", message=success_message)

        web_driver.close()

        self.save_session_id(session_id=session_id)

        return 0

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

        self.parent.withdraw()
        message_box.lift()
        message_box.update()

        return message_box

    def update_message_box_text(self, message_box: tk.Toplevel, new_msg: str) -> None:
        """
        Changes the text of the custom message box
        """

        for widget in message_box.winfo_children():
            widget.destroy()

        message_label = tk.Label(
            master=message_box,
            text=new_msg,
            font=(None, 16),
        )

        message_label.place(relx=0.5, rely=0.5, anchor="center")

        message_box.update()

    def close_message_box(self, message_box: tk.Toplevel) -> None:
        """
        Closes the provided message box and restores the parent window.
        """

        message_box.destroy()
        self.parent.deiconify()
