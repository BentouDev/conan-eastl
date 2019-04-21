from conans import ConanFile, CMake, tools
import os, platform

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

    def fix_linkage(self):
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("%s/CMakeLists.txt" % ("assimp-source"), "PROJECT( Assimp )", 

"""PROJECT( Assimp )
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        self.fix_linkage()
        # Workaround for conan choosing cmake embedded in Visual Studio
        if platform.system() == "Windows" and 'AZURE' in os.environ:
            cmake_path = '"C:\\Program Files\\CMake\\bin\\cmake.exe"'
            print (' [DEBUG] Forcing CMake : ' + cmake_path)
            os.environ['CONAN_CMAKE_PROGRAM'] = cmake_path

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
