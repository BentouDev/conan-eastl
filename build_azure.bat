python --version
pip --version

pip install conan conan_package_tools --upgrade --upgrade-strategy only-if-needed

conan user
move conan-fallback-settings.yml %USERPROFILE%/.conan/settings.yml
set CONAN_VISUAL_VERSIONS=16
set CI=true
set AZURE=true
set AZURE_BUILD_NUMBER=$(Build.BuildNumber)
python build.py