python --version
pip --version
@powershell -NoProfile -ExecutionPolicy Bypass -Command "$root = ((New-Object System.Net.WebClient).DownloadString('https://bootstrap.pypa.io/get-pip.py')) | python $root"
pip install conan conan_package_tools --upgrade --upgrade-strategy only-if-needed
refreshenv
conan user
move conan-fallback-settings.yml %USERPROFILE%/.conan/settings.yml
python build.py