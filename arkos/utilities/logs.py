"""
Classes for management of arkOS process logging.

arkOS Core
(c) 2016 CitizenWeb
Written by Jacob Cook
Licensed under GPLv3, see LICENSE.md
"""

import datetime
import logging

from .utils import random_string


class StreamFormatter(logging.Formatter):
    def format(self, record):
        if type(record.msg) in [str, bytes]:
            id = random_string(16)
            data = {"id": id, "message_id": id, "title": None,
                    "message": record.msg, "comp": "Unknown", "cls": "runtime",
                    "complete": True}
        else:
            data = record.msg.copy()
        levelname = "CRITICAL"
        logtime = datetime.datetime.fromtimestamp(record.created)
        logtime = logtime.strftime("%Y-%m-%d %H:%M:%S")
        logtime = "%s,%03d" % (logtime, record.msecs)
        if record.levelname == "DEBUG":
            levelname = "\033[37mDEBUG\033[0m  "
        if record.levelname == "INFO":
            levelname = "\033[36mINFO\033[0m   "
        if record.levelname == "SUCCESS":
            levelname = "\033[32mSUCCESS\033[0m"
        if record.levelname == "WARNING":
            levelname = "\033[33mWARN\033[0m   "
        if record.levelname == "ERROR":
            levelname = "\033[31mERROR\033[0m  "
        data.update({"cls": data["cls"].upper()[0], "levelname": levelname,
                     "asctime": logtime})
        result = self._fmt.format(**data)
        return result


class RuntimeFilter(logging.Filter):
    def filter(self, record):
        return 1 if record.msg["cls"].startswith("r") else 0


class NotificationFilter(logging.Filter):
    def filter(self, record):
        cls = "r" if type(record.msg) != dict else record.msg["cls"][0]
        return 1 if cls == "n" else 0


class LoggingControl:
    """Control logging for runtime events, using `logging` module API."""

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("arkos")
        logging.addLevelName(25, "SUCCESS")

    def add_stream_logger(
            self, st="{asctime} [{cls}] [{levelname}] {comp}: {message}",
            debug=False):
        """Create a new stream logger."""
        self.logger.handlers = []
        stdout = logging.StreamHandler()
        self.logger.setLevel(logging.DEBUG)
        stdout.setLevel(logging.DEBUG if debug else logging.INFO)
        dformatter = StreamFormatter(st)
        stdout.setFormatter(dformatter)
        self.logger.addHandler(stdout)

    def _log(self, level, mobj, exc_info=False):
        self.logger.log(level, mobj, exc_info=exc_info)

    def debug(self, comp, message, id=None):
        """Send a message with log level DEBUG."""
        id = id or random_string(16)
        self._log(10, {
            "id": id, "message_id": id, "cls": "runtime",
            "comp": comp, "title": None, "message": message
        })

    def info(self, comp, message, id=None):
        """Send a message with log level INFO."""
        id = id or random_string(16)
        self._log(20, {
            "id": id, "message_id": id, "cls": "runtime",
            "comp": comp, "title": None, "message": message
        })

    def success(self, comp, message, id=None):
        """Send a message with log level SUCCESS."""
        id = id or random_string(16)
        self._log(25, {
            "id": id, "message_id": id, "cls": "runtime",
            "comp": comp, "title": None, "message": message
        })

    def warning(self, comp, message, id=None):
        """Send a message with log level WARNING."""
        id = id or random_string(16)
        self._log(30, {
            "id": id, "message_id": id, "cls": "runtime",
            "comp": comp, "title": None, "message": message
        })

    def error(self, comp, message, id=None):
        """Send a message with log level ERROR."""
        id = id or random_string(16)
        self._log(40, {
            "id": id, "message_id": id, "cls": "runtime",
            "comp": comp, "title": None, "message": message
        }, exc_info=True)

    def critical(self, comp, message, id=None):
        """Send a message with log level CRITICAL."""
        id = id or random_string(16)
        self._log(50, {
            "id": id, "message_id": id, "cls": "runtime",
            "comp": comp, "title": None, "message": message
        })
