import sys
from app.utils.tasks import *


if __name__ == '__main__':
    task_list = ['dalamud', 'dalamud_changelog', 'asset', 'plugin', 'xivlauncher'] \
        if len(sys.argv) == 1 else sys.argv[1:]
    regen(task_list)
