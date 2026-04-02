#!/usr/bin/env python3
import argparse
from core import image_manager, container

parser = argparse.ArgumentParser(prog="td")
parser.add_argument("command", choices=["pull", "run"])
parser.add_argument("args", nargs="*")
args = parser.parse_args()

if args.command == "pull":
    if len(args.args) == 0:
        print("Usage: td pull <image_name> [tag]")
    else:
        tag = args.args[1] if len(args.args) > 1 else "latest"
        image_manager.pull_image(args.args[0], tag)
elif args.command == "run":
    if len(args.args) == 0:
        print("Usage: td run <image_name> [tag] [cmd]")
    else:
        tag = args.args[1] if len(args.args) > 1 else "latest"
        cmd = args.args[2] if len(args.args) > 2 else "/bin/sh"
        container.run_container(args.args[0], tag, cmd)