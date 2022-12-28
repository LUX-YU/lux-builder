import os
import abc
from typing import Union
from .common import ConfigurableObject

"""
    ProjectStorage and it's sub class
"""
class StorageMethodInterface(ConfigurableObject):
    @abc.abstractclassmethod
    def enable(self, target_directory : Union[str, os.PathLike]):
        pass

class StorageMethodFactory:
    @staticmethod
    def create(info : dict) -> StorageMethodInterface:
        storage_method_type = info["storage_type"]
        current_package = __import__(__package__)
        method_map = getattr(current_package, "__builtin_storage_method")
        RealStorageMethodType = method_map[storage_method_type]

        method = RealStorageMethodType()
        method.configure(info)

        return method
