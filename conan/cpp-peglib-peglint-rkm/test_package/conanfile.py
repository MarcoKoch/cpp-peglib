import os
from conan import ConanFile
from conan.tools.layout import basic_layout

required_conan_version = '>=2.0'


class RkmCppPeglibPeglintTestPackageConan(ConanFile):
    settings = 'os', 'arch', 'compiler', 'build_type'
    no_copy_source = True
    generators = 'VirtualBuildEnv'

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        basic_layout(self)

    def build(self):
        pass

    def test(self):
        grammar_file = os.path.join(self.source_folder, 'grammar.peg')
        self.run(f'peglint "{grammar_file}"', env='conanbuild')
