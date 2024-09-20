import os
import sys
from typing import Any, List


def instantiate_robots() -> List[Any]:
    """Define and instantiate all robots used during teleop."""
    return []


def start_teleop():
    """Trigger teleop when user input is entered."""
    pass


def teleop():
    """Start tele-operation."""
    pass


def main():
    pass


def shutdown_robots_gracefully(robots: List[Any]):
    """Gracefully turn off all robots."""
    pass


if __name__ == "__main__":
    robots = instantiate_robots()
    try:
        main()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        shutdown_robots_gracefully(robots)
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
