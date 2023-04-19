import os
import abc
from typing import List, Union
from .common import ConfigurableObject


class CommandGeneratorInterface(ConfigurableObject):
    @abc.abstractmethod
    def generate_configure_command(self, config_path: Union[str, os.PathLike],
                                   install_path: Union[str, os.PathLike]) -> List[str]:
        pass

    @abc.abstractmethod
    def generate_install_command(self) -> List[str]:
        pass


class AbstractCommandGenerator(CommandGeneratorInterface):
    def __init__(self, directory: Union[str, os.PathLike]) -> None:
        super().__init__()
        self._project_directory = directory
        self._info = None

    def project_directory(self):
        return self._project_directory


class CommandGeneratorFactory:
    @staticmethod
    def create(project_directory: Union[str, os.PathLike], info: dict) -> AbstractCommandGenerator:
        generator_type = info["build_tool_type"]
        current_package = __import__(__package__)
        generator_map = getattr(current_package, "__builtin_generator")
        RealGeneratorType = generator_map[generator_type]

        generator = RealGeneratorType(project_directory)
        generator.configure(info)

        return generator
