import argparse
import logging
from enum import Enum, auto, EnumMeta
from types import SimpleNamespace
from copy import copy, deepcopy
import os
import unittest
import abc
from dataclasses import dataclass

# ================================== EnumWithValuesAsStrings ==================================

class _EnumDirectValueMeta(EnumMeta):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.name
        return value

class _EnumGetKey(Enum):
    @classmethod
    def get_keys(cls):
        return [e.name for e in cls]

class AbstractActions(_EnumGetKey, metaclass=_EnumDirectValueMeta):
    pass

auto_action = auto

class _EnumForTests(AbstractActions):
    example1 = auto_action()
    example2 = auto_action()

class TestEnum(unittest.TestCase):
    
    def setUp(self):
        self.instance = _EnumForTests

    def test_i_get_value(self):
        self.assertEqual(self.instance.example1, "example1")

    def test_i_get_keys(self):
        self.assertEqual(self.instance.get_keys(), ["example1", "example2"])

# ================================== Logger ==================================

def get_logger()-> logging.Logger:
    # create logger with 'spam_application'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)
    return logger

class TestLogger(unittest.TestCase):
    
    def test_check_init(self):
        logger = get_logger()
        logger.info("123")

# ================================== CliReader ==================================

class _SimpleNameSpaceWithDict(SimpleNamespace):
    """for typing / documentation purposes exposed to user"""
    def get_as_dict() -> dict:
        pass

class ArgparseWithAugmentedArgs(argparse.ArgumentParser):
    def parse_args(self, *args, ignore_args, **kwargs) -> _SimpleNameSpaceWithDict:
        args = super().parse_args(*args, **kwargs)

        def get_as_dict() -> dict:
            data = copy(args.__dict__)
            if ignore_args and "args" in data:
                data.pop("args")
            if "get_as_dict" in data:
                data.pop("get_as_dict")
            return data

        args.get_as_dict = get_as_dict
        return args

class ArgparseReader:
    def __init__(self):
        self._parser = ArgparseWithAugmentedArgs()

    def add_argument(self, *args, **kwargs) -> 'ArgparseReader':
        copy_of_self = deepcopy(self)
        copy_of_self._parser.add_argument(*args, **kwargs)
        return copy_of_self

    def get_data(self, ignore_args=False) -> _SimpleNameSpaceWithDict:
        args = self._parser.parse_args(ignore_args=ignore_args)
        return args

    def ignore_others(self) -> 'ArgparseReader':
        copy_of_self = deepcopy(self)
        copy_of_self._parser.add_argument('args', nargs=argparse.REMAINDER)
        return copy_of_self # chain for easy data access

class TestCliReader(unittest.TestCase):

    def setUp(self):
        self.instance = ArgparseReader()

    def _read_args(self, cli_reader, cmd):
        return cli_reader._parser.parse_args(cmd.split(), ignore_args=False)

    def test_help(self):
        self._read_args(self.instance,"")

    def test_register_and_read_arguments(self):
        instance = self.instance
        instance = instance.add_argument("--argument", type=int)
        args = self._read_args(instance, "--argument=123")
        self.assertEqual(args.argument, 123)

    def test_ignore_unregistered(self):
        with self.assertRaises(SystemExit) as context:
            args = self._read_args(self.instance, "--argument=123")

        self.assertTrue(isinstance(context.exception, SystemExit))
    
    def test_get_data(self):
        instance = self.instance.add_argument("--argument", type=int)
        args = self._read_args(instance, "--argument=123")

        self.assertEqual(args.get_as_dict(), {'argument': 123})

# ================================== EnvReader ==================================

class EnvReader:
    def __init__(self):
        self._storage = SimpleNamespace()

    def __getitem__(self, key) -> str:
        return os.environ[key]

    def get(self, key, default = None) -> str:
        return os.environ.get(key, default)

    def add_arguments(self, **kwargs) -> 'EnvReader':
        self = deepcopy(self)
        for key, value in kwargs.items():
            setattr(self._storage, key, value)
        return self

    def get_storage(self) -> 'SimpleNamespace':
        return self._storage


class TestEnvReader(unittest.TestCase):
    
    def setUp(self):
        self.env_reader = EnvReader()
        os.environ["TEST_VAR"] = "123"

    def test_i_can_get_var(self):
        self.assertEqual(self.env_reader["TEST_VAR"], "123")

    def test_i_get_default_if_value_does_not_exist(self):
        self.assertEqual(self.env_reader.get("NOT_EXISTING_VAR", "456"), "456")

    def test_u_get_exception_for_non_existing_value(self):
        with self.assertRaises(KeyError) as context:
            self.env_reader["NOT_EXISTING_VAR"]

        self.assertTrue("NOT_EXISTING_VAR" in str(context.exception))
        self.assertTrue(isinstance(context.exception, KeyError))

# ================================== ShellMixin ==================================

class ShellException(Exception):
    pass

def _shell_execute(cmd, show_cmd=True):

    if show_cmd:
        print(f"$ {cmd}")
    
    return_code = os.system(cmd)
    if return_code != 0:
        raise ShellException(f"return code is not zero for command: {cmd}")

class ShellMixin:
    @classmethod
    def shell(cls, cmd, show_cmd=True):
        _shell_execute(cmd, show_cmd=print)
        

class TestShellMixin(unittest.TestCase):

    def test_get_good_cmd_command(self):
        _shell_execute("echo 123")

    def test_wrong_cmd_command(self):
        with self.assertRaises(ShellException) as context:
            _shell_execute("mkdir 1/2/3/6/5/7")

        self.assertTrue(isinstance(context.exception, ShellException))

# ================================== InputDataFactory ==================================

class AbstractInputDataFactory(abc.ABC):
    def __init__(self, registered_actions: list):
        self._argpase_reader = ArgparseReader() \
            .add_argument(
                'action',
                type=str,
                help='positional argument to choose action',
                choices=registered_actions
            )
        self._env_reader = EnvReader()

    @abc.abstractstaticmethod
    def register_cli_arguments(cli_reader: ArgparseReader) -> ArgparseReader:
        pass

    @abc.abstractstaticmethod
    def register_env_arguments(env_reader: EnvReader) -> EnvReader:
        pass

    def _get_cli_vars(self) -> SimpleNamespace:
        args = self.register_cli_arguments(self._argpase_reader) \
            .ignore_others().get_data(ignore_args=True)
        data: dict = args.get_as_dict()
        return SimpleNamespace(**data)

    def _get_env_vars(self) -> SimpleNamespace:
        return self.register_env_arguments(self._env_reader).get_storage()

    def get_input_data(self) -> 'SimpleNamespace':
        
        env_vars = self._get_env_vars()
        cli_vars = self._get_cli_vars()
        instance = SimpleNamespace(
            **env_vars.__dict__,
            **cli_vars.__dict__,
            cli_reader = self._argpase_reader,
        )
        return instance


def registered_action(f):
    def wrapper(*args):
        return f(*args)
    return wrapper


class AbstractScripts(ShellMixin):
    def __init__(
        self,
    ):
        self.registered_actions: list = [
            key for key, value in self.__class__.__dict__.items()
            if callable(value) and "registered_action" in value.__qualname__
        ]

    def process(self):
        input_data_factory: AbstractInputDataFactory = self.input_data_factory
        input_: SimpleNamespace = input_data_factory(
            registered_actions=self.registered_actions
        ).get_input_data()
        getattr(self, input_.action)(input_)
