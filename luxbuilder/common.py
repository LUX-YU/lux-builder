import abc
from typing import List, Tuple

class InfomationIncompleteError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def lost_word(self) -> Tuple[str]:
        return self.args

class ConfigurableObject(object):
    @abc.abstractclassmethod
    def necessary_config_key(self) -> List[str]:
        return []

    @abc.abstractclassmethod
    def allowed_config_key(self) -> List[str]:
        return []

    def configure(self, info : dict):
        lost_key = []
        is_lost_key = False
        for key in self.necessary_config_key():
            if not key in info:
                is_lost_key = True
                lost_key.append(key)
        if is_lost_key:
            raise InfomationIncompleteError(*tuple(lost_key))
        
        self._info = info
        