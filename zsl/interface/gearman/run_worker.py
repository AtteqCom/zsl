"""
:mod:`zsl.interface.gearman.run_worker`
---------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import print_function
from __future__ import unicode_literals

from zsl import Zsl
from zsl.application.containers.gearman_container import GearmanContainer


def main():
    print("Initializing app.")

    app = Zsl(__name__, modules=GearmanContainer.modules())
    app.run_worker()


if __name__ == "__main__":
    main()
