python --version
pip --version

choco upgrade cmake

pip install conan conan_package_tools --upgrade --upgrade-strategy only-if-needed

conan user
move conan-fallback-settings.yml %USERPROFILE%/.conan/settings.yml
cmake --version
python build.py