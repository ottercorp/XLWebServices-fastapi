import argparse

import uvicorn
from app import get_app

app = get_app()


def cli():
    parser = argparse.ArgumentParser(description='XLWeb-fastapi')
    subparsers = parser.add_subparsers(metavar='子命令')

    start_server = subparsers.add_parser('start', help='启动服务器')
    start_server.set_defaults(handle=start_server_func)

    init_server = subparsers.add_parser('init', help='初始化服务器')
    init_server.set_defaults(handle=init_server_func)

    args = parser.parse_args()
    if hasattr(args, 'handle'):
        args.handle(args)
    else:
        parser.print_help()


def start_server_func(args):
    from logs import logger
    logger.info('Starting server...')
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8080)


def init_server_func(args):
    from regen import regen_main
    regen_main()
    from app.utils.tasks import regen_pluginmaster
    regen_pluginmaster(repo_url="https://github.com/ottercorp/DalamudPlugins.git")


if __name__ == '__main__':
    cli()
