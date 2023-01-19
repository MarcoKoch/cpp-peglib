import os
from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import cmake_layout, CMakeToolchain, CMake
from conan.tools.files import copy

required_conan_version = '>=2.0'


class RkmCppPeglibPeglintConan(ConanFile):
    name = 'cpp-peglib-peglint-rkm'
    description = """The peglint CLI tool from rakkom’s experimental modified \
version of the cpp-peglib project.

WARNING:
This is experimental software. The modifications made in this version of \
cpp-peglib are subject to change and/or may be discarded entirely without \
prior notice. Changes that prove useful will be contributed upstream once \
they are ready.

See <https://github.com/yhirose/cpp-peglib> for the original cpp-peglib \
project."""
    homepage = 'https://gibhub.com/marcokoch/cpp-peglib'
    url = 'https://gibhub.com/marcokoch/cpp-peglib'
    package_type = 'application'
    license = 'MIT'
    author = 'Marco Koch'
    topics = 'c++', 'parser', 'peg', 'linter'
    provides = 'cpp-peglib-peglint'
    settings = 'os', 'arch', 'compiler', 'build_type'
    no_copy_source = True

    @property
    def _root_folder(self):
        return os.path.join(os.pardir, os.pardir)

    @property
    def _subproject_folder(self):
        return os.path.join('conan', self.name)

    def set_version(self):
        root_folder = os.path.join(self.recipe_folder, self._root_folder)
        git = Git(self, folder=root_folder)
        self.version = f'git.{git.get_commit()[:7]}'
        if git.is_dirty():
            self.version += '+dirty'

    def validate(self):
        self.output.warning("This package contains experimental software, \
which is subject to change without prior notice. Do not rely on it for \
productive purposes!")
        if self.settings.compiler.get_safe('cppstd'):
            check_min_cppstd(self, 17)

    def compatibility(self):
        build_types = [None, 'Release', 'Debug', 'RelWithDebInfo',
                       'MinSizeRel']
        compatible_configs = []
        for bt in build_types:
            if bt == self.settings.get_safe('build_type'):
                continue
            compatible_configs.append({'settings': [('build_type', bt)]})
        return compatible_configs

    def layout(self):
        self.folders.root = self._root_folder
        cmake_layout(self)

    def export_sources(self):
        root_folder = os.path.join(self.recipe_folder, self._root_folder)
        copy(self, 'lint/*', root_folder, self.export_sources_folder)
        copy(self, 'peglib.h', root_folder, self.export_sources_folder)
        copy(self, 'CMakeLists.txt', root_folder, self.export_sources_folder)
        copy(self, 'LICENSE', root_folder, self.export_sources_folder,
             excludes=['README.md'])

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables['BUILD_TESTS'] = False
        tc.cache_variables['BUILD_EXAMPLES'] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build(target='peglint')

    def package(self):
        binary_folder = os.path.join(self.package_folder, 'bin')
        license_folder = os.path.join(self.package_folder, 'licenses')
        copy(self, os.path.join('lint', 'peglint*'), self.build_folder,
             binary_folder, keep_path=False)
        copy(self, 'LICENSE', self.source_folder, license_folder)

    def package_info(self):
        self.cpp_info.set_property('cmake_target_name', 'cpp-peglib::peglint')
        self.cpp_info.set_property('cmake_file_name', 'cpp-peglib-peglint')
