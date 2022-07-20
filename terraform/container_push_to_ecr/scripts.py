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
    aws_region: str
    action: str
    aws_docker_registry: str = "example"
    docker_tag: str = "latest"
    image_buildname: str = "nginx:latest"

    @classmethod
    def _get_cli_vars(cls) -> dict:
        args = CliReader().read_group().get_data()
        return SimpleNamespace(
            action=args.action,
        )

    @classmethod
    def _get_env_vars(cls):
        return SimpleNamespace(
            aws_user_id=os.environ["TF_VAR_AWS_USER_ID"],
            aws_region=os.environ["TF_VAR_AWS_REGION"],
        )

    @classmethod
    def get_input_data(cls) -> 'InputData':
        
        env_vars = cls._get_env_vars()
        cli_vars = cls._get_cli_vars()
        instance = InputData(
            **(env_vars.__dict__),
            **(cli_vars.__dict__),
        )
        return instance

class ActionExecutor:
    logger = init_logger()

    @classmethod
    def _shell(cls, cmd):
        return_code = os.system(cmd)
        cls.logger.debug(f"return_code={return_code}, cmd={cmd}")
        if return_code != 0:
            raise Exception(f"return code is not zero for command: {cmd}")

    @classmethod
    def handle_actions(cls, input_: InputData):
        match input_.action:
            case "build":
                cls._shell(f"docker pull {input_.image_buildname}")
            case "tag":
                cls._shell(
                    f"docker tag {input_.image_buildname} {input_.aws_user_id}.dkr.ecr.{input_.aws_region}"
                    f".amazonaws.com/{input_.aws_docker_registry}:{input_.docker_tag}"
                )
            case "auth":
                cls._shell(
                    f"aws ecr get-login-password | docker login --username AWS"
                    f" --password-stdin {input_.aws_user_id}.dkr.ecr.{input_.aws_region}.amazonaws.com"
                )
            case "push":
                cls._shell(
                    f"docker push {input_.aws_user_id}.dkr.ecr.{input_.aws_region}"
                    f".amazonaws.com/{input_.aws_docker_registry}:{input_.docker_tag}"
                )
            
if __name__=="__main__":
    input_ = InputData.get_input_data()
    ActionExecutor().handle_actions(input_)

class TestStuff(unittest.TestCase):

    def test_upper(self):
        self.assertTrue(True)