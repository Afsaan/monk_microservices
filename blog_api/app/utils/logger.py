from dotenv import dotenv_values
from logtail import LogtailHandler
import logging
import sys

config = dotenv_values(".env")

def setup_logger():
    token = config['BETTER_STACK_TOKEN']

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler("app.log")
    better_stack_handler = LogtailHandler(source_token=token)

    formatter = logging.Formatter(
        fmt= '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        datefmt= '%d-%m-%Y %H:%M:%S:%MS'
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    better_stack_handler.setFormatter(formatter)

    logger.handlers = [stream_handler, file_handler, better_stack_handler]
    return logger