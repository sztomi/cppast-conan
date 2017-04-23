from conans import ConanFile, CMake, tools
import os


class CppastConan(ConanFile):
    name = "cppast"
    version = "master"
    license = "MIT"
    url = "https://github.com/sztomi/cppast-conan"
    settings = "os", "compiler", "build_type", "arch"
    options = {"compdb": [True, False]}
    default_options = "compdb=False"
    generators = "cmake"

    def source(self):
        self.run("git clone --depth 1 https://github.com/foonathan/cppast.git")

    def build(self):
        cmake = CMake(self)
        compdb = '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON' if self.options.compdb else ''
        self.run('cmake cppast %s %s' % (cmake.command_line, compdb))
        self.run("cmake --build . %s -- -j %d" % (cmake.build_config, tools.cpu_count()))

    def package(self):
        self.copy("*.hpp", dst="include", src="cppast/include")
        self.copy("*.hpp", dst="include", src="cppast/external/type_safe/include")
        self.copy("*.hpp", dst="include", src="cppast/external/type_safe/external/debug_assert")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cppast", "_cppast_tiny_process"]
