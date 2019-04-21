from conans import ConanFile, CMake
import os

eastl_version = os.getenv('EASTL_VERSION', '0.0')
eastl_commit = os.getenv('EASTL_COMMIT', '')

class EASTLConan(ConanFile):
    name = "eastl"
    license = "MIT"
    url = "https://github.com/BentouDev/conan-eastl"
    version = eastl_version
    commit = eastl_commit

    description = "EASTL stands for Electronic Arts Standard Template Library. It is an extensive and robust implementation that has an emphasis on high performance."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["eastl-source/*"]

    options = {"build_type": ["Release", "Debug", "RelWithDebInfo", "MinSizeRel"]}
    default_options = "build_type=MinSizeRel",

    def package_id(self):
        self.info.include_build_settings()
        self.info.settings.compiler
        self.info.settings.arch
        self.info.settings.build_type

    def build(self):
        print (' [DEBUG] Searching for CMake at standard path...')
        cmake_path = '"C:\\Program Files\\CMake\\bin\\cmake.exe"'
        if os.path.isfile(cmake_path):
            print (' [DEBUG] Forcing CMake : ' + cmake_path)
            os.environ['CONAN_CMAKE_PROGRAM'] = cmake_path
        else:
            print (' [DEBUG] Not found CMake at standard path! Aquired version is ' + CMake.get_version())

        cmake = CMake(self)
        #cmake.definitions['EASTL_VERSION'] = self.version
        #cmake.definitions['EASTL_COMMIT'] = self.commit
        #cmake.definitions['EASTL_CHANNEL'] = self.channel
        cmake.configure(source_folder="eastl-source")
        cmake.build()

    def package(self):
        self.copy("*.h", src="eastl-source/test/packages/EABase/include/Common/EABase", dst="include/EABase", keep_path=True)
        self.copy("*.h", src="eastl-source/include", dst="include", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [ self.name ]
