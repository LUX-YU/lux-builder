import abc
import os
import subprocess
from typing import List, Callable


class CommandExecutor:
    def __init__(self, cwd=None, finish_callback: Callable[[int, [List]], bool] = None) -> None:
        self.__cwd = os.path.curdir if cwd is None else cwd
        if finish_callback is None:
            def default_cb(ret, cmd) -> bool:
                print("Execute %s finished, return code %d." % (str(cmd), ret))
                return ret == 0

            self._finished_cb = default_cb
        else:
            self._finished_cb = finish_callback

    def work_directory(self):
        return self.__cwd

    @abc.abstractclassmethod
    def execute(self, commands: List[List[str]], echo=True):
        ...


class LogExecutor(CommandExecutor):
    def __init__(self, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd: str = None,
                 finish_callback: Callable[[int, [List]], bool] = None) -> None:
        super().__init__(cwd, finish_callback)
        self._stdout = stdout
        self._stderr = stderr

    def execute(self, commands: List[List[str]], echo=True):
        for command in commands:
            if echo:
                print(f"Start executing command {str(command)}")
            process = subprocess.Popen(command, cwd=self.work_directory(), stdout=self._stdout, stderr=self._stderr)
            ret_code = process.wait()
            should_continue = self._finished_cb(ret_code, command)
            if not should_continue:
                break


class FileLogExecutor(LogExecutor):
    def __init__(self, out_file_path, error_file_path, cwd: str = None,
                 finish_callback: Callable[[int, [List]], bool] = None) -> None:
        _stdout = open(out_file_path, "w")
        _stderr = open(error_file_path, "w")
        super().__init__(_stdout, _stderr, cwd, finish_callback)

    def __del__(self):
        self._stdout.close()
        self._stderr.close()
