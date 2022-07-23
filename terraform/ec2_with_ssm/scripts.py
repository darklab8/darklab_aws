
from types import SimpleNamespace

import darklab_utils as utils

class InputDataFactory(utils.AbstractInputDataFactory):

    @staticmethod
    def register_cli_arguments(argpase_reader: utils.ArgparseReader) -> utils.ArgparseReader:
        return argpase_reader \
        .add_argument("--ec2_id", type=str, help="id of created ec2 instance, looks like i-0671be41e5f55488e, outputed by terraform script")

    @staticmethod
    def register_env_arguments(env_reader: utils.EnvReader) -> utils.EnvReader:
        return env_reader.add_arguments(

        )

class MyScripts(utils.AbstractScripts):
    input_data_factory = InputDataFactory

    @utils.registered_action
    def connect(self):
        self.shell(f"aws ssm start-session --target={self.globals.ec2_id}")

if __name__=="__main__":
    MyScripts().process()