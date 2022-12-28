import os
from typing import Union
from ..cmd_generator import AbstractCommandGenerator
from multiprocessing import cpu_count

class CMakeInstallCommandGenerator:
    def __init__(self, config_path :str, build_type :str, cpu_count : int) -> None:
        self.config_path = config_path
        self.cpu_count   = cpu_count
        self.build_type  = build_type

    def generate_command(self) -> list:
        ret_commands = [
            "cmake",
            "--build",      self.config_path,
            "--parallel",   str(self.cpu_count),
            "--target",     "install",
            "--config",     self.build_type
        ]
        return ret_commands

class CMakeConfigCommandGenerator:
    def __init__(self, project_path, config_path, install_path, build_type, extra_commands : list) -> None:
        self.project_path    = project_path
        self.config_path     = config_path
        self.install_path    = install_path
        self.build_type      = build_type
        self.extra_commands  = extra_commands

    def generate_command(self) -> list:
        ret_commands = ["cmake"]
        ret_commands.append("-B" + self.config_path)
        ret_commands.append(self.project_path)
        ret_commands.append("-DCMAKE_BUILD_TYPE=" + self.build_type)
        ret_commands.append("-DCMAKE_INSTALL_PREFIX=" + self.install_path)
        for command in self.extra_commands:
            ret_commands.append(command)
        return ret_commands

class CMakeToolChainFileGenerator:
    def __init__(self, target_system_rootfs, stage_path, 
        triple, c_compiler, cxx_compiler) -> None:
        self.target_fs      = target_system_rootfs
        self.stage_path     = stage_path
        self.triple         = triple
        self.c_compiler     = c_compiler
        self.cxx_compiler   = cxx_compiler

    # return toolchain-file's path
    def generate(self, generate_path : str):
        toolchain_parent_dir = os.path.dirname(generate_path)
        if not os.path.exists(toolchain_parent_dir):
            os.makedirs(toolchain_parent_dir)
        current_path = os.path.dirname(os.path.realpath(__file__))
        cmake_template_toolchain_path = os.path.join(current_path, "cmake_toolchain.cmake.template")
        with open(cmake_template_toolchain_path, "r", encoding="utf-8") as rf, open(generate_path, "w") as wf:
            cmake_toolchain_template = rf.read()
            cmake_toolchain = cmake_toolchain_template.format(
                triple          = self.triple,
                system_rootfs   = self.target_fs,
                c_compiler      = self.c_compiler,
                cxx_compiler    = self.cxx_compiler,
                install_dir     = self.stage_path
            )
            wf.write(cmake_toolchain)

class CMakeCommandGenerator(AbstractCommandGenerator):
    def __init__(self, directory : Union[str, os.PathLike]) -> None:
        super().__init__(directory)

    def allowed_config_key(self):
        return ["cpu_count", "config_options"]

    def necessary_config_key(self):
        return ["build_type"]

    def generate_configure_command(self, config_path : Union[str, os.PathLike], 
        install_path : Union[str, os.PathLike]):

        self.config_path = config_path
        extra_cmds = self._info["config_options"] if "config_options" in self._info else []

        cmd = CMakeConfigCommandGenerator(
            self.project_directory(),
            config_path,
            install_path,
            self._info["build_type"],
            extra_cmds
        ).generate_command()
        return [cmd, ]
    
    def generate_install_command(self):
        use_cpu_count  = int(self._info["cpu_count"])\
            if "cpu_count" in self._info else cpu_count()
        
        cmd = CMakeInstallCommandGenerator(
            self.config_path,
            self._info["build_type"],
            use_cpu_count
        ).generate_command()

        return [cmd, ]
