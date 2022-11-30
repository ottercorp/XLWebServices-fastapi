import sys
import asyncio
from app.utils.tasks import *


if __name__ == '__main__':
    print(sys.argv)
    task_list = ['dalamud', 'asset', 'plugin', 'xivlauncher'] \
        if len(sys.argv) == 1 else sys.argv[1:]
    asyncio.run(regen(task_list))
