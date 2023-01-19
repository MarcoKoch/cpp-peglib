import os
from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.build import check_min_cppstd
from conan.tools.layout import basic_layout
from conan.tools.files import copy
from conan.tools.microsoft import is_msvc

required_conan_version = '>=2.0'


class RkmCppPeglibConan(ConanFile):
    name = 'cpp-peglib-rkm'
    description = """A modified version of cpp-peglib with experimental \
features and bugfixes.

NOTE:
You should probably use the original cpp-peglib instead unless you have a \
specific reason to use this one. The original version is available as package \
'cpp-peglib' in the conan center. See <https://github.com/yhirose/cpp-peglib> \
for the original source code.

WARNING:
This is experimental software. The modifications made in this version of \
cpp-peglib are subject to change and/or may be discarded entirely without \
prior notice. Changes that prove useful will be contributed upstream once \
they are ready."""
    homepage = 'https://gibhub.com/marcokoch/cpp-peglib'
    url = 'https://gibhub.com/marcokoch/cpp-peglib'
    package_type = 'header-library'
    license = 'MIT'
    author = 'Marco Koch'
    provides = 'cpp-peglib'
    topics = 'c++', 'parser', 'peg', 'header-only'
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
        self.output.warning("This package contains experimental software. You \
should probably use package 'cpp-peglib' from the Conan Center instead.")

        if self.settings.compiler.get_safe('cppstd'):
            check_min_cppstd(self, 17)

    def package_id(self):
        self.info.clear()

    def layout(self):
        self.folders.root = self._root_folder
        self.folders.subproject = self._subproject_folder
        basic_layout(self)

    def export_sources(self):
        root_folder = os.path.join(self.recipe_folder, self._root_folder)
        copy(self, 'peglib.h', root_folder, self.export_sources_folder)
        copy(self, 'peg.vim', root_folder, self.export_sources_folder)
        copy(self, 'LICENSE', root_folder, self.export_sources_folder)

    def build(self):
        pass

    def package(self):
        source_root_folder = os.path.join(self.source_folder,
                                          self._root_folder)
        include_folder = os.path.join(self.package_folder, 'include')
        data_folder = os.path.join(self.package_folder, 'share')
        license_folder = os.path.join(self.package_folder, 'licenses')
        copy(self, 'peglib.h', source_root_folder, include_folder)
        copy(self, 'peg.vim', source_root_folder, data_folder)
        copy(self, 'LICENSE', source_root_folder, license_folder)

    def package_info(self):
        self.cpp_info.resdirs = ['share']
        self.cpp_info.set_property('cmake_target_name', 'cpp-peglib')
        self.cpp_info.set_property('cmake_file_name', 'cpp-peglib')
        if self.settings.get_safe('os') in ['Linux', 'FreeBSD']:
            self.cpp_info.system_libs.append('pthread')
            self.cpp_info.cxxflags.append('-pthread')
            self.cpp_info.exelinkflags.append('-pthread')
            self.cpp_info.sharedlinkflags.append('-pthread')
        if is_msvc(self):
            self.cpp_info.cxxflags.append('/Zc:__cplusplus')
