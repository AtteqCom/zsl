from asl.interface.importer import initialize_cli_application
initialize_cli_application()

from asl.interface.run import run_task
import sys

# Run it!
if __name__ == "__main__":
    print run_task(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
