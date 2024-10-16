import logging

def initialize_logging():
    # adding the logging feature
    logging.basicConfig(level=logging.DEBUG, filename="chess_log.log",
                        filemode="w", format="%(levelname)s - %(message)s")


initialize_logging()