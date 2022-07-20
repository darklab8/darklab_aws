import argparse
from dataclasses import dataclass
import os
import logging
from types import SimpleNamespace
import unittest

def init_logger()-> logging.Logger:
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

class CliReader:
    def __init__(self):
        self._parser = argparse.ArgumentParser()

    def add_argument(self, *args, **kwargs):
        return self._parser.add_argument(*args, **kwargs)

    def get_data(self) -> SimpleNamespace:
        return self._parser.parse_args()

    def read_group(self) -> 'CliReader':
        self._parser.add_argument('action', type=str, help='positional argument to choose action')
        return self # chain for easy data access


@dataclass
class InputData:
    aws_user_id: str
    action: str

    @staticmethod
    def get_cli() -> dict:
        args = CliReader().read_group().get_data()

        return {
            "action": args.action
        }

    @staticmethod
    def get_env() -> dict:
        return {
            "aws_user_id": os.environ["TF_VAR_AWS_USER_ID"]
        }

    @classmethod
    def get_input_data(cls) -> 'InputData':
        return InputData(
            **(cls.get_cli()),
            **(cls.get_env()),
        )

class ActionExecutor:
    logger = init_logger()

    @classmethod
    def shell(cls, cmd):
        return_code = os.system(cmd)
        cls.logger.debug(f"return_code={return_code}, cmd={cmd}")
        if return_code != 0:
            raise Exception(f"return code is not zero for command: {cmd}")

    @classmethod
    def handle_actions(cls, input_: InputData):
        match input_.action:
            case "build":
                cls.shell("docker pull nginx:latest")
            case "tag":
                cls.shell(
                    f"docker tag {input_.aws_user_id}.dkr.ecr.$AWS_REGION.amazonaws.com/aws-cookbook-repo:latest"
                )
            


if __name__=="__main__":
    input_ = InputData.get_input_data()
    ActionExecutor().handle_actions(input_)

class TestStuff(unittest.TestCase):

    def test_upper(self):
        self.assertTrue(True)