import abc
from typing import List, Tuple, Any


class InformationIncompleteError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def lost_word(self) -> tuple[Any, ...]:
        return self.args


class ConfigurableObject(object):
    def __init__(self):
        self._info = None

    @abc.abstractmethod
    def necessary_config_key(self) -> List[str]:
        return []

    @abc.abstractmethod
    def allowed_config_key(self) -> List[str]:
        return []

    def configure(self, info: dict):
        lost_key = []
        is_lost_key = False
        for key in self.necessary_config_key():
            if not key in info:
                is_lost_key = True
                lost_key.append(key)
        if is_lost_key:
            raise InformationIncompleteError(*tuple(lost_key))

        self._info = info
