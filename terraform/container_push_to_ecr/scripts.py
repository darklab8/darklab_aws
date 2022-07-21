
from types import SimpleNamespace

import darklab_utils as utils

class InputDataFactory(utils.AbstractInputDataFactory):

    @staticmethod
    def register_cli_arguments(argpase_reader: utils.ArgparseReader) -> utils.ArgparseReader:
        return argpase_reader \
        .add_argument("--aws_docker_registry", type=str, default="example") \
        .add_argument("--docker_tag", type=str, default="latest") \
        .add_argument("--image_buildname", type=str, default="nginx:latest")

    @staticmethod
    def register_env_arguments(env_reader: utils.EnvReader) -> utils.EnvReader:
        return env_reader.add_arguments(
            aws_user_id=env_reader["TF_VAR_AWS_USER_ID"],
            aws_region=env_reader["TF_VAR_AWS_REGION"],
        )

class MyScripts(utils.AbstractScripts):
    input_data_factory = InputDataFactory

    @utils.registered_action
    def example(self, input_: SimpleNamespace):
        args = input_.cli_reader \
            .add_argument("--argument", type=int, default=456) \
            .get_data()
        self.shell(f"echo {args.argument}")

    @utils.registered_action
    def build(self, input_: SimpleNamespace):
        self.shell(f"docker pull {input_.image_buildname}")

    @utils.registered_action
    def tag(self, input_: SimpleNamespace):
        self.shell(
            f"docker tag {input_.image_buildname} {input_.aws_user_id}.dkr.ecr.{input_.aws_region}"
            f".amazonaws.com/{input_.aws_docker_registry}:{input_.docker_tag}"
        )

    @utils.registered_action
    def auth(self, input_: SimpleNamespace):
        self.shell(
            f"aws ecr get-login-password | docker login --username AWS"
            f" --password-stdin {input_.aws_user_id}.dkr.ecr.{input_.aws_region}.amazonaws.com"
        )

    @utils.registered_action
    def push(self, input_: SimpleNamespace):
        self.shell(
            f"docker push {input_.aws_user_id}.dkr.ecr.{input_.aws_region}"
            f".amazonaws.com/{input_.aws_docker_registry}:{input_.docker_tag}"
        )

    @utils.registered_action
    def list(self, input_: SimpleNamespace):
        self.shell(
            f"aws ecr list-images --repository-name {input_.aws_docker_registry}"
        )

if __name__=="__main__":
    MyScripts().process()