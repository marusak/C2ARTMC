"""Global tests."""
import os
from os.path import abspath, dirname, join
import sys
import filecmp
from subprocess import Popen, PIPE


def run_once(files_dir, exec_file):
    """Run one c2artmc command."""
    files = os.listdir(files_dir)
    os.chdir(files_dir)
    for f in files:
        if f.endswith(".c"):
            source_file = f
            break
    else:
        sys.exit(1)
    cmd = Popen([exec_file, join(files_dir, source_file)],
                stdout=PIPE,
                stderr=PIPE)
    stdout, stderr = cmd.communicate()
    assert cmd.returncode == 0
    assert filecmp.cmp("program.py", "expected_program.py")
    os.remove("program.py")


def test_all_folders():
    """Run c2artmc on all files in input."""
    exec_file = join(abspath(dirname(dirname(__file__))), "c2artmc.py")
    # each file + typedef in separate folder
    files_dir = (join(abspath(dirname(__file__)), "test_dirs"))
    folders = os.listdir(files_dir)
    for folder in folders:
        if (folder not in ['.', '..'] or not folder.endswith(".py")):
            run_once(join(abspath(dirname(__file__)), "test_dirs", folder),
                     exec_file)
