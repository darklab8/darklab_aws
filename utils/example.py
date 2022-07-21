
from dataclasses import dataclass
from types import SimpleNamespace

from utils import (
    AbstractInputDataFactory,
    AbstractInputData,
    AbstractScripts,
    registered_action,
)

@dataclass(frozen=True, kw_only=True)
class InputData(AbstractInputData):
    cli_argument: str
    env_argument1: str
    env_argument2: str
   

class InputDataFactory(AbstractInputDataFactory):
    @staticmethod
    def register_cli_arguments(cli_reader):
        return cli_reader \
        .add_argument("--cli_argument", type=str, default="example")

    @staticmethod
    def register_env_arguments(env_reader) -> SimpleNamespace:
        return SimpleNamespace(
            env_argument1=env_reader["PWD"],
            env_argument2=env_reader.get("NOT_EXISTING_VAR", "default_value"),
        )

class MyScripts(AbstractScripts):

    @registered_action
    def build(self, input_):
        self.shell(f"echo {input_.cli_argument}")

    @registered_action
    def example(self, input_):
        args = input_.cli_reader \
            .add_argument("--argument", type=int, default=456) \
            .get_data()
        self.shell(f"echo debug_{args.argument}")

if __name__=="__main__":
    MyScripts(
        model=InputData,
        input_data_factory=InputDataFactory,
    ).process()