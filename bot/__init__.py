"""
Package description:
This package contains bot logic, database connection and flask server.
"""

import logging

logging.basicConfig(
    filename="main.log",
    format='%(asctime)s: %(thread)d - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
    level=logging.INFO
)
