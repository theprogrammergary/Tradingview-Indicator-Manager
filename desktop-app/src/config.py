"""
Loads environment vars from .env file
"""

# imports
import os

# from dotenv import load_dotenv
from loguru import logger

# environment vars
# load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".setup", ".env"))

# global vars
RUNTIME_PATH: str = os.path.dirname(p=os.path.abspath(path=__file__))
print(RUNTIME_PATH)


# gui vars
GUI_WIDTH: int = 1000
GUI_HEIGHT: int = 700
GUI_NAME: str = "Tradingview Indicator Access Management"

# logger
logger.remove()
logger.add(
    sink="./logs/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="14 days",
    backtrace=True,
    format=(
        "\n{time:YYYY-MM-DD HH:mm:ss} {level.icon} {level} \n"
        '{file}>"{function}">{line} \n    {message} \n'
    ),
)
