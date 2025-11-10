import argparse
import subprocess
import sys
import os

# folder containing cli.py
PACKAGE_DIR = os.path.dirname(__file__)

def main():
    parser = argparse.ArgumentParser(
        description="Broadcast Server CLI",
        usage="broadcast-server <command> [options]"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    parser_start = subparsers.add_parser(
        "start", help="Start the broadcast server"
    )

    parser_connect = subparsers.add_parser(
        "connect", help="Connect to a broadcast server"
    )

    args = parser.parse_args()

    if args.command == "start":
        cmd = [sys.executable, os.path.join(PACKAGE_DIR, "server.py")]

    elif args.command == "connect":
        cmd = [sys.executable, os.path.join(PACKAGE_DIR, "client.py")]
    else:
        print("❌ Please choose either 'start' or 'connect'.")
        sys.exit(1)

    subprocess.run(cmd)
