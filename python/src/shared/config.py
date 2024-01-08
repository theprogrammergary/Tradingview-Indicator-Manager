"""
Loads environment vars from .env file
"""

# imports
import os
import platform

from loguru import logger


def get_base_system_dir() -> str:
    system: str = platform.system()

    if system == "Darwin":
        return os.path.expanduser(
            path="~/Library/Application Support/Tradingview Indicator Access Management"
        )

    elif system == "Windows":
        return os.path.join(
            os.path.expanduser(path="~"),
            "AppData",
            "Roaming",
            "Tradingview Indicator Access Management",
        )

    elif system == "Linux":
        return os.path.join(
            os.path.expanduser(path="~"), ".Tradingview Indicator Access Management"
        )

    else:
        return ""


# path vars
SYSTEM_APP_DIR: str = get_base_system_dir()
if SYSTEM_APP_DIR:
    os.makedirs(name=SYSTEM_APP_DIR, exist_ok=True)


CONFIG_PATH: str = os.path.dirname(p=os.path.abspath(path=__file__))
RUNTIME_PATH: str = os.path.join(CONFIG_PATH, "..")

SESSION_FILE: str = os.path.join(SYSTEM_APP_DIR, "login.json")
INDICATORS_FILE: str = os.path.join(SYSTEM_APP_DIR, "indicators.json")

# gui vars
GUI_WIDTH: int = 1000
GUI_HEIGHT: int = 700
GUI_NAME: str = "Tradingview Indicator Access Management"

MESSAGE_WIDTH: int = 400
MESSAGE_HEIGHT: int = 100


# tradingview
LOGIN_CHECK_URL: str = "https://www.tradingview.com/tvcoins/details/"
ADD_ACCESS_URL: str = "https://www.tradingview.com/pine_perm/add/"
REMOVE_ACCESS_URL: str = "https://www.tradingview.com/pine_perm/remove/"
USER_ACCESS_LIST_URL: str = (
    "https://www.tradingview.com/pine_perm/list_users/?limit=10&order_by=-created"
)
PINE_NAME_SELECTOR: str = (
    "#tv-content > div > div > div.tv-chart-view__section >"
    "div.tv-chart-view__header > div.tv-chart-view__title.selectable"
    "> div > div.tv-chart-view__title-row.tv-chart-view__title-row--name > div > h1"
)
PINE_ID_SELECTOR: str = (
    "#tv-content > div > div > div.tv-chart-view__section >"
    "div.tv-chart-view__permission-block.tv-chart-view__permission"
    "-block--invite-only-access-granted > div.tv-chart-view__script-actions"
    "> button.tv-social-stats__item.i-checked.js-chart-view__manage-access."
    "apply-common-tooltip.tv-social-stats__item--button"
)


# logger
LOG_PATH: str = os.path.join(RUNTIME_PATH, ".logs", "")
logger.remove()
logger.add(
    sink=f"{LOG_PATH}" + "{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="14 days",
    backtrace=True,
    format=(
        "\n{time:YYYY-MM-DD HH:mm:ss} {level.icon} {level} \n"
        '{file}>"{function}">{line} \n    {message} \n'
    ),
)


# debug paths
print(f"RUNTIME: {RUNTIME_PATH}\n")
print(f"LOGGER: {LOG_PATH}\n")
print(f"SESSION_FILE: {SESSION_FILE}\n")
print(f"INDICATORS_FILE: {INDICATORS_FILE}")

print("\n\n\n\n")
