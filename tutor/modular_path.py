import sys
from os import path

root_directory = path.abspath(path.join(path.dirname(__file__), '..'))

# For importing CSound-Python code that lives in modular.
modular = path.join(root_directory, 'tutor', 'modular')
sys.path.append(modular)

systemfiles = path.join(root_directory, 'data', 'system')
sys.path.append(systemfiles)

userfiles = path.join(root_directory, 'data', 'user')
sys.path.append(userfiles)
