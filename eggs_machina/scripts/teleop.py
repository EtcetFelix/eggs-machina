import os
import sys


def main():
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
