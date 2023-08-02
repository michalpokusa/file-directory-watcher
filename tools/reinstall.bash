cd $(dirname "$0")/..

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

rm -rf ./build/*

pip uninstall -y file-directory-watcher
pip install .
