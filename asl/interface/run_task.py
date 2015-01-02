import sys
import os
from asl.interface.run import run_task
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'));

# Run it!
if __name__ == "__main__":
    print run_task(sys.argv)
