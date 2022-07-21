import argparse
import logging
from enum import Enum, auto, EnumMeta
from types import SimpleNamespace
from copy import copy
import os

class EnumDirectValueMeta(EnumMeta):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.name
        return value

class EnumGetKey(Enum):
    @classmethod
    def get_keys(cls):
        return [e.name for e in cls]


def get_logger()-> logging.Logger:
    # create logger with 'spam_application'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

class SimpleNameSpaceWithDict(SimpleNamespace):
    """for typing / documentation purposes exposed to user"""
    def get_as_dict() -> dict:
        pass

class CliReader:
    def __init__(self):
        self._parser = argparse.ArgumentParser()

    def add_argument(self, *args, **kwargs) -> 'CliReader':
        self._parser.add_argument(*args, **kwargs)
        return self

    def get_data(self) -> SimpleNameSpaceWithDict:
        args = self._parser.parse_args()
        def get_as_dict() -> dict:
            data = copy(args.__dict__)
            data.pop("args")
            data.pop("get_as_dict")
            return data

        args.get_as_dict = get_as_dict 
        return args

    def ignore_others(self) -> 'CliReader':
        self._parser.add_argument('args', nargs=argparse.REMAINDER)
        return self # chain for easy data access

class ShellMixin:
    logger = get_logger()

    @classmethod
    def _shell(cls, cmd):
        return_code = os.system(cmd)
        cls.logger.debug(f"return_code={return_code}, cmd={cmd}")
        if return_code != 0:
            raise Exception(f"return code is not zero for command: {cmd}")

class EnvReader:
    def __getitem__(self, key):
        return os.environ[key]

    def get(self, key, default = None):
        return os.environ.get(key, default)