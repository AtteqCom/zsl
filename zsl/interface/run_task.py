import sys
import os
# TODO: Consider removing automatic path initialization!
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from zsl.interface.importer import initialize_cli_application, InitializationContext
initialize_cli_application(InitializationContext(unit_test=False))

from zsl.interface.run import run_task

# Run it!
if __name__ == "__main__":
    print run_task(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
