"""
:mod:`zsl.utils.deploy.integrator`
----------------------------------
"""

from __future__ import unicode_literals
import tempfile
import os


def integrate_to_file(what, filename, start_line, end_line):
    """WARNING this is working every second run.. so serious bug
    Integrate content into a file withing "line marks"
    """

    try:
        with open(filename) as f:
            lines = f.readlines()
    except IOError:
        lines = []

    tmp_file = tempfile.NamedTemporaryFile(delete=False)

    lines.reverse()

    # first copy before start line
    while lines:
        line = lines.pop()

        if line == start_line:
            break

        tmp_file.write(line)

    # insert content
    tmp_file.write(start_line)
    tmp_file.write(what)
    tmp_file.write(end_line)

    # skip until end line
    while lines:
        line = lines.pop()

        if line == end_line:
            break

    # copy rest
    tmp_file.writelines(lines)
    tmp_file.close()

    os.rename(tmp_file.name, filename)
