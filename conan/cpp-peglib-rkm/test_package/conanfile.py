import os
from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMake
from conan.tools.build import can_run

required_conan_version = '>=2.0'


class RkmCppPeglibTestPackageConan(ConanFile):
    settings = 'os', 'arch', 'compiler', 'build_type'
    no_copy_source = True,
    generators = 'CMakeDeps', 'CMakeToolchain', 'VirtualRunEnv'

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not can_run(self):
            return
        testapp = os.path.join(self.cpp.build.bindirs[0], 'testapp')
        self.run(testapp, env='conanrun')
