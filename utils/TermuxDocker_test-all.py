#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys

# Equivalent to UTILS_DIR="$(dirname $0)"
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))

# Equivalent to TermuxDocker_CMD="${UTILS_DIR}/../TermuxDocker/maincmd.py"
TermuxDocker_CMD = os.path.join(UTILS_DIR, "..", "TermuxDocker", "maincmd.py")

# Equivalent to PYTHON_LIST="$(type -p python2.7) $(type -p python3.6) $(type -p python3.11)"
python_versions = ["python2.7", "python3.6", "python3.11"]
PYTHON_LIST = []

for p_ver in python_versions:
    path = shutil.which(p_ver)
    if path:
        PYTHON_LIST.append(path)

# Test directory path
TEST_DIR = os.path.expanduser("~/.TermuxDocker-tests")

def clean_test_dir():
    """Equivalent to /bin/rm -rf ${HOME}/.TermuxDocker-tests"""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR, ignore_errors=True)

# Main loop
for PYTHON_CMD in PYTHON_LIST:
    # First test suite
    clean_test_dir()
    test_script_1 = os.path.join(UTILS_DIR, "TermuxDocker_test.sh")
    subprocess.run(["sh", test_script_1, TermuxDocker_CMD, PYTHON_CMD])

    # Second test suite
    clean_test_dir()
    test_script_2 = os.path.join(UTILS_DIR, "TermuxDocker_test-run.sh")
    subprocess.run(["sh", test_script_2, TermuxDocker_CMD, PYTHON_CMD])

# Final cleanup
clean_test_dir()
