__author__ = "chenhui.lux.yu"
__emil__ = "chenhui.lux.yu@outlook.com"

from .cmd_generator import CommandGeneratorInterface, CommandGeneratorFactory
from .project_storage import StorageMethodInterface, StorageMethodFactory
from .executor import FileLogExecutor

# builtin command generator
from .generators.cmake import CMakeCommandGenerator

__builtin_generator = {
    "cmake": CMakeCommandGenerator
}

from .getters.git import RemoteGitProject
from .getters.zip import ZipFile

__builtin_storage_method = {
    "git_remote": RemoteGitProject,
    "zip_file": ZipFile
}
