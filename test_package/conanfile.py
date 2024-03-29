from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "unstable")
username = os.getenv("CONAN_USERNAME", "sztomi")


class CppastTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "cppast/master@%s/%s" % (username, channel)
    generators = "cmake"
    default_options = ('cppast:compdb=True')

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
