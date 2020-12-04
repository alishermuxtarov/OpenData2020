import sys
import os


def execfile(file_name):
    with open(file_name, "r") as f:
        exec(f.read(), sys._getframe(1).f_globals,
             sys._getframe(1).f_locals)


apps_conf_dir = os.path.dirname(__file__)
for filename in os.listdir(apps_conf_dir):
    if not filename.startswith('__') and filename.endswith('.py'):
        execfile(os.path.join(apps_conf_dir, filename))
