
from dataclasses import dataclass
from types import SimpleNamespace
import unittest

import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))))

from utils import (
    EnumWithValuesAsStrings,
    auto,
    CliReader,
    ShellMixin,
    EnvReader,
    get_logger,
)

@dataclass(frozen=True, kw_only=True)
class InputData:
    aws_user_id: str
    aws_region: str
    action: str
    aws_docker_registry: str
    docker_tag: str
    image_buildname: str
    cli_reader: CliReader

class Actions(EnumWithValuesAsStrings):
    example = auto()
    build = auto()
    tag = auto()
    auth = auto()
    push = auto()
    list = auto()

class InputDataFactory:
    model = InputData

    def __init__(self):
        self._cli_reader = CliReader() \
            .add_argument(
                'action',
                type=str,
                help='positional argument to choose action',
                choices=Actions.get_keys(),
            )
        self._env_reader = EnvReader()

    def _get_cli_vars(self) -> SimpleNamespace:
        args = self._cli_reader \
            .add_argument("--aws_docker_registry", type=str, default="example") \
            .add_argument("--docker_tag", type=str, default="latest") \
            .add_argument("--image_buildname", type=str, default="nginx:latest") \
            .ignore_others().get_data()

        data: dict = args.get_as_dict()
        return SimpleNamespace(**data)

    def _get_env_vars(self) -> SimpleNamespace:
        return SimpleNamespace(
            aws_user_id=self._env_reader["TF_VAR_AWS_USER_ID"],
            aws_region=self._env_reader["TF_VAR_AWS_REGION"],
        )

    def get_input_data(self):
        
        env_vars = self._get_env_vars()
        cli_vars = self._get_cli_vars()
        instance = self.model(
            **(env_vars.__dict__),
            **(cli_vars.__dict__),
            cli_reader = self._cli_reader,
        )
        return instance

class ActionExecutor(ShellMixin):

    @classmethod
    def handle_actions(cls, input_: InputData):
        match input_.action:
            case Actions.example:
                # Example how to read additional arguments                
                args = input_.cli_reader \
                    .add_argument("--argument", type=int, default=456) \
                    .get_data()
                cls._shell(f"echo {args.argument}")
            case Actions.build:
                cls._shell(f"docker pull {input_.image_buildname}")
            case Actions.tag:
                cls._shell(
                    f"docker tag {input_.image_buildname} {input_.aws_user_id}.dkr.ecr.{input_.aws_region}"
                    f".amazonaws.com/{input_.aws_docker_registry}:{input_.docker_tag}"
                )
            case Actions.auth:
                cls._shell(
                    f"aws ecr get-login-password | docker login --username AWS"
                    f" --password-stdin {input_.aws_user_id}.dkr.ecr.{input_.aws_region}.amazonaws.com"
                )
            case Actions.push:
                cls._shell(
                    f"docker push {input_.aws_user_id}.dkr.ecr.{input_.aws_region}"
                    f".amazonaws.com/{input_.aws_docker_registry}:{input_.docker_tag}"
                )
            case Actions.list:
                cls._shell(
                    f"aws ecr list-images --repository-name {input_.aws_docker_registry}"
                )
            
if __name__=="__main__":
    input_: InputData = InputDataFactory().get_input_data()
    ActionExecutor().handle_actions(input_)

class TestStuff(unittest.TestCase):

    def test_upper(self):
        self.assertTrue(True)