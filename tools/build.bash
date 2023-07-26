cd $(dirname "$0")/..
source .venv/bin/activate

pyinstaller \
--clean \
--onefile \
--specpath ./build \
--distpath ./build/dist \
--bootloader-ignore-signals \
fdw.py
