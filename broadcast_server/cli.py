import argparse
import os
import subprocess
import sys

# folder containing cli.py
PACKAGE_DIR = os.path.dirname(__file__)

def main():
    parser = argparse.ArgumentParser(
        description="Broadcast Server CLI",
        usage="broadcast-server <command>"
    )

    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("start", help="Start the broadcast server")
    subparsers.add_parser("connect", help="Connect to a broadcast server")

    args = parser.parse_args()

    COMMANDS = {
        "start": "server.py",
        "connect": "client.py",
        "status": "status.py",
    }

    cmd_file = COMMANDS.get(args.action, None)
    if not cmd_file:
        print("❌ Unknown command.")
        sys.exit(1)

    subprocess.run([sys.executable, os.path.join(PACKAGE_DIR, cmd_file)])
