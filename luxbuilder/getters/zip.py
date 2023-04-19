import os
from ..project_storage import StorageMethodInterface
from zipfile import ZipFile
from typing import Union, List


class CompressFile(StorageMethodInterface):
    def __init__(self) -> None:
        super().__init__()

    def necessary_config_key(self) -> List[str]:
        return ["path"]

    def enable(self, target_directory: Union[str, os.PathLike]):
        with ZipFile(self._info["path"]) as _pack_file:
            _pack_file.extractall(target_directory)
