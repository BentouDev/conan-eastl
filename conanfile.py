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

    options = {}
    default_options = {}

    def source(self):
        if platform.system() != "Windows":
            return

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        print (' [*] Injecting conanbuildinfo.cmake...')
        tools.replace_in_file("%s/CMakeLists.txt" % ("eastl-source"), "project(EASTL CXX)", 

"""project(EASTL CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
add_definitions(-DEASTL_EABASE_DISABLED)""")

    def build(self):
        # Workaround for conan choosing cmake embedded in Visual Studio
        if platform.system() == "Windows" and 'AZURE' in os.environ:
            cmake_path = '"C:\\Program Files\\CMake\\bin\\cmake.exe"'
            print (' [DEBUG] Forcing CMake : ' + cmake_path)
            os.environ['CONAN_CMAKE_PROGRAM'] = cmake_path

        cmake = CMake(self)
        #cmake.definitions['CMAKE_CXX_COMPILER_ID'] = 'gcc'#self.settings.compiler
        #cmake.definitions['CMAKE_CC_COMPILER'] = self.settings.compiler
        #cmake.definitions['CMAKE_CC_COMPILER_VERSION'] = self.settings.compiler.version
        #cmake.definitions['CMAKE_CXX_COMPILER_VERSION'] = self.settings.compiler.version
        #cmake.definitions['EASTL_VERSION'] = self.version
        #cmake.definitions['EASTL_COMMIT'] = self.commit
        #cmake.definitions['EASTL_CHANNEL'] = self.channel
        cmake.definitions['EASTL_BUILD_TESTS'] = True
        cmake.configure(source_folder="eastl-source")
        cmake.build()

    def package(self):
        self.copy("*.h", src="eastl-source/test/packages/EABase/include/Common/EABase", dst="include/EABase", keep_path=True)
        self.copy("*.h", src="eastl-source/include", dst="include", keep_path=True)
        self.copy("*.natvis", src="eastl-source/doc", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.pdb", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [ self.name ]
        # self.cpp_info.defines = ["EASTL_EABASE_DISABLED"]
