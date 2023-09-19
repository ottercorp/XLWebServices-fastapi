import sys
from app.utils.tasks import regen


def regen_main():
    task_list = ['dalamud', 'dalamud_changelog', 'asset', 'plugin', 'xivlauncher','injector'] \
        if len(sys.argv) == 1 else sys.argv[1:]
    regen(task_list)


if __name__ == '__main__':
    regen_main()
