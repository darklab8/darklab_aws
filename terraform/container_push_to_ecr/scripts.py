
from dataclasses import dataclass
from types import SimpleNamespace

from utils import (
    AbstractActions,
    auto_action,
    AbstractInputDataFactory,
    AbstractActionSwitcher,
    AbstractInputData,
    AbstractScripts,
)

@dataclass(frozen=True, kw_only=True)
class InputData(AbstractInputData):
    aws_user_id: str
    aws_region: str
    aws_docker_registry: str
    docker_tag: str
    image_buildname: str
    

class Actions(AbstractActions):
    example = auto_action()
    build = auto_action()
    tag = auto_action()
    auth = auto_action()
    push = auto_action()
    list = auto_action()

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
    AbstractScripts(
        model=InputData,
        action_switcher=ActionSwitcher,
        actions=Actions,
        input_data_factory=InputDataFactory,
    ).run()