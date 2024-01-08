"""
Loads environment vars from .env file
"""

# imports
import os

from loguru import logger

# global vars
RUNTIME_PATH: str = os.path.join(
    os.path.dirname(p=os.path.abspath(path=__file__)), ".."
)

SESSION_FILE: str = os.path.join(RUNTIME_PATH, "shared", "login.json")
INDICATORS_FILE: str = os.path.join(RUNTIME_PATH, "shared", "indicators.json")

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
logger.remove()
logger.add(
    sink="./python/logs/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="14 days",
    backtrace=True,
    format=(
        "\n{time:YYYY-MM-DD HH:mm:ss} {level.icon} {level} \n"
        '{file}>"{function}">{line} \n    {message} \n'
    ),
)
