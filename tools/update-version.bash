cd $(dirname "$0")/..


python3 - <<END
import os

with open('pyproject.toml', 'rt') as f:
    pyproject = f.read()

version = os.environ['VERSION'].replace('v', '')
pyproject = pyproject.replace('version = "0.0.0.dev0"', f'version = "{version}"')

with open('pyproject.toml', 'wt') as f:
    f.write(pyproject)
END
