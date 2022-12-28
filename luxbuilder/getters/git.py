from ..project_storage import StorageMethodInterface
from rich import console, progress
from typing import Union
import os
import git
import abc
from typing import List

class GitRemoteProgress(git.RemoteProgress):
    OP_CODES = [
        "BEGIN",
        "CHECKING_OUT",
        "COMPRESSING",
        "COUNTING",
        "END",
        "FINDING_SOURCES",
        "RECEIVING",
        "RESOLVING",
        "WRITING",
    ]
    OP_CODE_MAP = {
        getattr(git.RemoteProgress, _op_code): _op_code for _op_code in OP_CODES
    }

    def __init__(self) -> None:
        super().__init__()
        self.progressbar = progress.Progress(
            progress.SpinnerColumn(),
            # *progress.Progress.get_default_columns(),
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(),
            progress.TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            "eta",
            progress.TimeRemainingColumn(),
            progress.TextColumn("{task.fields[message]}"),
            console=console.Console(),
            transient=False,
        )
        self.progressbar.start()
        self.active_task = None

    def __del__(self) -> None:
        # logger.info("Destroying bar...")
        self.progressbar.stop()

    @classmethod
    def get_curr_op(cls, op_code: int) -> str:
        """Get OP name from OP code."""
        # Remove BEGIN- and END-flag and get op name
        op_code_masked = op_code & cls.OP_MASK
        return cls.OP_CODE_MAP.get(op_code_masked, "?").title()
    def update(
        self,
        op_code: int,
        cur_count: str | float,
        max_count: str | float | None = None,
        message: str | None = "",
    ) -> None:
        # Start new bar on each BEGIN-flag
        if op_code & self.BEGIN:
            self.curr_op = self.get_curr_op(op_code)
            # logger.info("Next: %s", self.curr_op)
            self.active_task = self.progressbar.add_task(
                description=self.curr_op,
                total=max_count,
                message=message,
            )
        self.progressbar.update(
            task_id=self.active_task,
            completed=cur_count,
            message=message,
        )
        # End progress monitoring on each END-flag
        if op_code & self.END:
            # logger.info("Done: %s", self.curr_op)
            self.progressbar.update(
                task_id=self.active_task,
                message=f"[bright_black]{message}",
            )

class RemoteGitProject(StorageMethodInterface):
    def __init__(self) -> None:
        super().__init__()

    def necessary_config_key(self) -> List[str]:
        return ["url", "branch"]

    def enable(self, target_directory : Union[str, os.PathLike]):
        try:
            # target repo is exists
            repo = git.Repo(target_directory)
            print("Target repo is exist")
            repo.git.checkout(self._info["branch"])
        except Exception as e:
            if os.path.exists(target_directory):
                os.removedirs(target_directory)
                os.makedirs(target_directory)
            remote_repo_url = self._info["url"]
            print(f"start clone repo from {remote_repo_url}")
            git.Repo.clone_from(
                remote_repo_url,
                target_directory,
                progress = GitRemoteProgress(),
                branch = self._info["branch"],
                multi_options=[
                    "--depth=1",
                ]
            )
