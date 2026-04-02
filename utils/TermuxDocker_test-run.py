#!/usr/bin/env python3
"""
High-level TermuxDocker testing script
Converted from the full udocker bash test script.
Tests pull, create, setup, run for multiple execmodes and images.
"""

import subprocess
import os
import sys
import shutil

# ------------------------------
# Colors and Strings
# ------------------------------
RED = '\033[1;31m'
GREEN = '\033[1;32m'
BLUE = '\033[1;34m'
PURPLE = '\033[1;36m'
NC = '\033[0m'

OK_STR = f"{GREEN}[OK]{NC}"
FAIL_STR = f"{RED}[FAIL]{NC}"

# ------------------------------
# Configuration
# ------------------------------
PYTHON_CMD = sys.executable
TERMXDOCKER_CMD = os.path.expanduser("~/TermuxDocker/termuxdocker.py")
TEST_DIR = os.path.expanduser("~/.termuxdocker-tests")

if not os.path.isfile(TERMXDOCKER_CMD):
    print(f"{FAIL_STR} TermuxDocker CLI not found at {TERMXDOCKER_CMD}")
    sys.exit(1)

os.environ["TERMXDOCKER_DIR"] = TEST_DIR

# ------------------------------
# Test containers/images
# ------------------------------
IMAGES = [
    ("centos", "7"),
    ("ubuntu", "22.04"),
    ("openjdk", "8-jdk-alpine")
]

CONTAINERS = [
    ("c7", "centos", "7"),
    ("ub22", "ubuntu", "22.04"),
    ("jv", "openjdk", "8-jdk-alpine")
]

EXECS = ["P1", "P2", "F1", "F2", "F3", "F4", "R1", "R2", "R3"]

FAILED_TESTS = []

# ------------------------------
# Helper functions
# ------------------------------

def run_td(*args):
    """Run TermuxDocker CLI command"""
    cmd = [PYTHON_CMD, TERMXDOCKER_CMD, *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def print_result(returncode, msg):
    """Assert success if returncode==0"""
    print("\n" + "_"*120)
    if returncode == 0:
        print(f"{OK_STR}    {msg}")
    else:
        print(f"{FAIL_STR}    {msg}")
        FAILED_TESTS.append(msg)
    print("_"*120 + "\n")

def print_result_inv(returncode, msg):
    """Assert success if returncode==1"""
    print("\n" + "_"*120)
    if returncode == 1:
        print(f"{OK_STR}    {msg}")
    else:
        print(f"{FAIL_STR}    {msg}")
        FAILED_TESTS.append(msg)
    print("_"*120 + "\n")

def cleanup():
    """Remove test directory if exists"""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR, exist_ok=True)

def rm_container(name):
    run_td("rm", name)

def rmi_image(image_tag):
    run_td("rmi", image_tag)

# ------------------------------
# Setup
# ------------------------------
cleanup()
print(f"{OK_STR} Test directory ready: {TEST_DIR}")

# Remove any leftover containers/images (ignore errors)
for name, _, _ in CONTAINERS:
    rm_container(name)

for image, tag in IMAGES:
    rmi_image(f"{image}:{tag}")

# ------------------------------
# Pull Images
# ------------------------------
for image, tag in IMAGES:
    res = run_td("pull", f"{image}:{tag}")
    print_result(res.returncode, f"Pull image {image}:{tag}")

# ------------------------------
# Create containers
# ------------------------------
for name, image, tag in CONTAINERS:
    res = run_td("create", "--name", name, f"{image}:{tag}")
    print_result(res.returncode, f"Create container {name} from {image}:{tag}")

# ------------------------------
# Run tests for all execmodes
# ------------------------------
for execmode in EXECS:
    print(f"\n{'='*30} Testing execmode = {execmode} {'='*30}")
    
    # Setup containers
    for name, _, _ in CONTAINERS:
        res = run_td("setup", f"--execmode={execmode}", name)
        print_result(res.returncode, f"Setup {name} with execmode={execmode}")
    
    # Run commands
    for name, image, _ in CONTAINERS:
        cmd = "java -version" if "jv" in name else "ls --version"
        res = run_td("run", "--env=LANG=C", name, cmd)
        print_result(res.returncode, f"Run {name} ({cmd}) execmode={execmode}")

# ------------------------------
# Final report
# ------------------------------
if not FAILED_TESTS:
    print(f"{OK_STR} All tests passed successfully!")
    sys.exit(0)
else:
    print(f"{FAIL_STR} Some tests failed:")
    for t in FAILED_TESTS:
        print(f"{FAIL_STR} {t}")
    sys.exit(1)echo "============================================="

DEFAULT_UDIR=$HOME/.udocker-tests
export UDOCKER_DIR=${DEFAULT_UDIR}
if [ -d ${DEFAULT_UDIR} ]
then
  echo "ERROR test directory exists, remove first: ${DEFAULT_UDIR}"
  exit 1
fi

echo "\____________________________________________________________________________________________________________________________________/"
udocker rm c7
udocker rm ub22
udocker rm jv

## Use openjdk:8-jdk-alpine for regression of issue #363

echo "\____________________________________________________________________________________________________________________________________/"
udocker rmi centos:7
udocker rmi ubuntu:22.04
udocker rmi openjdk:8-jdk-alpine

echo "\____________________________________________________________________________________________________________________________________/"
udocker pull centos:7; return=$?
udocker pull ubuntu:22.04; return=$?
udocker pull openjdk:8-jdk-alpine; return=$?

echo "\____________________________________________________________________________________________________________________________________/"
udocker images; return=$?
udocker create --name=c7 centos:7; return=$?
udocker create --name=ub22 ubuntu:22.04; return=$?
udocker create --name=jv openjdk:8-jdk-alpine; return=$?
udocker ps; return=$?

echo "===================="
echo "* Test udocker run *"
echo "===================="

echo "===================================== execmode = P1"
STRING="T001: udocker setup jv == execmode = P1"
udocker setup jv; return=$?
result

STRING="T002: udocker run jv java -version == execmode = P1"
udocker run --env="LANG=C" jv java -version; return=$?
result

STRING="T003: udocker setup c7 == execmode = P1"
udocker setup c7; return=$?
result

STRING="T004: udocker run c7 ls --version == execmode = P1"
udocker run c7 ls --version; return=$?
result

STRING="T005: udocker setup ub22 == execmode = P1"
udocker setup ub22; return=$?
result

STRING="T006: udocker run ub22 ls --version == execmode = P1"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = P2"
STRING="T007: udocker setup --execmode=P2 jv == execmode = P2"
udocker setup --execmode=P2 jv; return=$?
result

STRING="T008: udocker run jv java -version == execmode = P2"
udocker run --env="LANG=C" jv java -version; return=$?
result

STRING="T009: udocker setup --execmode=P2 c7 == execmode = P2"
udocker setup --execmode=P2 c7; return=$?
result

STRING="T010: udocker run c7 ls --version == execmode = P2"
udocker run c7 ls --version; return=$?
result

STRING="T011: udocker setup --execmode=P2 ub22 == execmode = P2"
udocker setup --execmode=P2 ub22; return=$?
result

STRING="T012: udocker run ub22 ls --version == execmode = P2"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = F1"
STRING="T013: udocker setup --execmode=F1 c7 == execmode = F1"
udocker setup --execmode=F1 c7; return=$?
result

STRING="T014: udocker run c7 ls --version == execmode = F1"
udocker run c7 ls --version; return=$?
result

STRING="T015: udocker setup --execmode=F1 ub22 == execmode = F1"
udocker setup --execmode=F1 ub22; return=$?
result

STRING="T016: udocker run ub22 ls --version == execmode = F1"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = F2"
STRING="T017: udocker setup --execmode=F2 c7 == execmode = F2"
udocker setup --execmode=F2 c7; return=$?
result

STRING="T018: udocker run c7 ls --version == execmode = F2"
udocker run c7 ls --version; return=$?
result

STRING="T019: udocker setup --execmode=F2 ub22 == execmode = F2"
udocker setup --execmode=F2 ub22; return=$?
result

STRING="T020: udocker run ub22 ls --version == execmode = F2"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = F3"
STRING="T021: udocker setup --execmode=F3 jv == execmode = F3"
udocker setup --execmode=F3 jv; return=$?
result

STRING="T022: udocker run jv java -version == execmode = F3"
udocker run --env="LANG=C" jv java -version; return=$?
result

STRING="T023: udocker setup --execmode=F3 c7 == execmode = F3"
udocker setup --execmode=F3 c7; return=$?
result

STRING="T024: udocker run c7 ls --version == execmode = F3"
udocker run c7 ls --version; return=$?
result

STRING="T025: udocker setup --execmode=F3 ub22 == execmode = F3"
udocker setup --execmode=F3 ub22; return=$?
result

STRING="T026: udocker run ub22 ls --version == execmode = F3"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = F4"
STRING="T027: udocker setup --execmode=F4 jv == execmode = F4"
udocker setup --execmode=F4 jv; return=$?
result

STRING="T028: udocker run jv java -version == execmode = F4"
udocker run --env="LANG=C" jv java -version; return=$?
result

STRING="T029: udocker setup --execmode=F4 c7 == execmode = F4"
udocker setup --execmode=F4 c7; return=$?
result

STRING="T030: udocker run c7 ls --version == execmode = F4"
udocker run c7 ls --version; return=$?
result

STRING="T031: udocker setup --execmode=F4 ub22 == execmode = F4"
udocker setup --execmode=F4 ub22; return=$?
result

STRING="T032: udocker run ub22 ls --version == execmode = F4"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = R1"
STRING="T033: udocker setup --execmode=R1 jv == execmode = R1"
udocker setup --execmode=R1 jv; return=$?
result

STRING="T034: udocker run jv java -version == execmode = R1"
udocker run --env="LANG=C" jv java -version; return=$?
result

STRING="T035: udocker setup --execmode=R1 c7 == execmode = R1"
udocker setup --execmode=R1 c7; return=$?
result

STRING="T036: udocker run c7 ls --version == execmode = R1"
udocker run c7 ls --version; return=$?
result

STRING="T037: udocker setup --execmode=R1 ub22 == execmode = R1"
udocker setup --execmode=R1 ub22; return=$?
result

STRING="T038: udocker run ub22 ls --version == execmode = R1"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = R2"
STRING="T039: udocker setup --execmode=R2 jv == execmode = R2"
udocker setup --execmode=R2 jv; return=$?
result

STRING="T040: udocker run jv java -version == execmode = R2"
udocker run --env="LANG=C" jv java -version; return=$?
result

STRING="T041: udocker setup --execmode=R2 c7 == execmode = R2"
udocker setup --execmode=R2 c7; return=$?
result

STRING="T042: udocker run c7 ls --version == execmode = R2"
udocker run c7 ls --version; return=$?
result

STRING="T043: udocker setup --execmode=R2 ub22 == execmode = R2"
udocker setup --execmode=R2 ub22; return=$?
result

STRING="T044: udocker run ub22 ls --version == execmode = R2"
udocker run ub22 ls --version; return=$?
result

echo "===================================== execmode = R3"
STRING="T045: udocker setup --execmode=R3 jv == execmode = R3"
udocker setup --execmode=R3 jv; return=$?
result

STRING="T046: udocker run jv java -version == execmode = R3"
udocker run --env="LANG=C" jv java -version; return=$?
result

STRING="T047: udocker setup --execmode=R3 c7 == execmode = R3"
udocker setup --execmode=R3 c7; return=$?
result

STRING="T048: udocker run c7 ls --version == execmode = R3"
udocker run c7 ls --version; return=$?
result

STRING="T049: udocker setup --execmode=R3 ub22 == execmode = R3"
udocker setup --execmode=R3 ub22; return=$?
result

STRING="T050: udocker run ub22 ls --version == execmode = R3"
udocker run ub22 ls --version; return=$?
result

# Report failed tests
if [ "${#FAILED_TESTS[*]}" -le 0 ]
then
    printf "${OK_STR}    All tests passed\n"
    exit 0
fi

printf "${FAIL_STR}    The following tests have failed:\n"
for (( i=0; i<${#FAILED_TESTS[@]}; i++ ))
do
    printf "${FAIL_STR}    ${FAILED_TESTS[$i]}\n"
done
exit 1
