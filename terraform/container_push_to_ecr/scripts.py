
from dataclasses import dataclass
from types import SimpleNamespace

import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))))

from utils import (
    EnumWithValuesAsStrings,
    enum_auto,
    AbstractInputDataFactory,
    AbstractActionSwitcher,
)

@dataclass(frozen=True, kw_only=True)
class InputData:
    aws_user_id: str
    aws_region: str
    action: str
    aws_docker_registry: str
    docker_tag: str
    image_buildname: str
    cli_reader: None

class Actions(EnumWithValuesAsStrings):
    example = enum_auto()
    build = enum_auto()
    tag = enum_auto()
    auth = enum_auto()
    push = enum_auto()
    list = enum_auto()

class InputDataFactory(AbstractInputDataFactory):
    @staticmethod
    def register_cli_arguments(cli_reader):
        return cli_reader \
        .add_argument("--aws_docker_registry", type=str, default="example") \
        .add_argument("--docker_tag", type=str, default="latest") \
        .add_argument("--image_buildname", type=str, default="nginx:latest")

    @staticmethod
    def register_env_arguments(env_reader) -> SimpleNamespace:
        return SimpleNamespace(
            aws_user_id=env_reader["TF_VAR_AWS_USER_ID"],
            aws_region=env_reader["TF_VAR_AWS_REGION"],
        )

class ActionSwitcher(AbstractActionSwitcher):

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
    input_: InputData = InputDataFactory(model=InputData, actions=Actions).get_input_data()
    ActionSwitcher().handle_actions(input_)