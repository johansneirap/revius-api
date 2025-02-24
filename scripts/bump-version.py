import sys

new_version = sys.argv[1]

with open("app/version.py", "w") as f:
    f.write(f'VERSION = "v{new_version}"\n')
