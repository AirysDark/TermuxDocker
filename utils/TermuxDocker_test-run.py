#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

# --- Formatting Constants ---
RED = '\033[1;31m'
GREEN = '\033[1;32m'
BLUE = '\033[1;34m'
PURPLE = '\033[1;36m'
NC = '\033[0m'

OK_STR = f"{GREEN}[OK]{NC}"
FAIL_STR = f"{RED}[FAIL]{NC}"

FAILED_TESTS = []

# --- Argument Parsing & Environment ---
if len(sys.argv) > 1:
    TermuxDocker_CMD = sys.argv[1]
else:
    TermuxDocker_CMD = shutil.which("TermuxDocker")

if not TermuxDocker_CMD or not os.access(TermuxDocker_CMD, os.X_OK):
    print(f"ERROR TermuxDocker file not executable: {TermuxDocker_CMD}")
    sys.exit(1)

PYTHON_CMD = sys.argv[2] if len(sys.argv) > 2 else ""

if PYTHON_CMD and not os.access(PYTHON_CMD, os.X_OK):
    print(f"ERROR python interpreter not executable: {PYTHON_CMD}")
    sys.exit(1)

# --- Functions ---
def print_ok():
    print(OK_STR, end="")

def print_fail():
    print(FAIL_STR, end="")

def result(ret_code, test_string):
    print(" ")
    if ret_code == 0:
        print_ok()
        print(f"    {test_string}")
    else:
        print_fail()
        print(f"    {test_string}")
        FAILED_TESTS.append(test_string)
    print("\\____________________________________________________________________________________________________________________________________/")
    print("")
    print(" ____________________________________________________________________________________________________________________________________ ")
    print("/                                                                                                                                    \\ ")

def TermuxDocker(*args):
    """Replicates the bash TermuxDocker function: $PYTHON_CMD $TermuxDocker_CMD $*"""
    cmd = []
    if PYTHON_CMD:
        cmd.append(PYTHON_CMD)
    cmd.append(TermuxDocker_CMD)
    
    # Flatten args in case lists are passed
    for arg in args:
        if isinstance(arg, list):
            cmd.extend(arg)
        else:
            cmd.append(str(arg))
            
    process = subprocess.run(cmd)
    return process.returncode

# --- Main Script Execution ---
print("=============================================")
print("* This script tests TermuxDocker run and options *")
print("* and volume mount options                  *")
print("=============================================")

DEFAULT_UDIR = os.path.expanduser("~/.TermuxDocker-tests")
os.environ["TermuxDocker_DIR"] = DEFAULT_UDIR

if os.path.isdir(DEFAULT_UDIR):
    print(f"ERROR test directory exists, remove first: {DEFAULT_UDIR}")
    sys.exit(1)

print("\\____________________________________________________________________________________________________________________________________/")
TermuxDocker("rm", "c7")
TermuxDocker("rm", "ub22")
TermuxDocker("rm", "jv")

print("\\____________________________________________________________________________________________________________________________________/")
TermuxDocker("rmi", "centos:7")
TermuxDocker("rmi", "ubuntu:22.04")
TermuxDocker("rmi", "openjdk:8-jdk-alpine")

print("\\____________________________________________________________________________________________________________________________________/")
TermuxDocker("pull", "centos:7")
TermuxDocker("pull", "ubuntu:22.04")
TermuxDocker("pull", "openjdk:8-jdk-alpine")

print("\\____________________________________________________________________________________________________________________________________/")
TermuxDocker("images")
TermuxDocker("create", "--name=c7", "centos:7")
TermuxDocker("create", "--name=ub22", "ubuntu:22.04")
TermuxDocker("create", "--name=jv", "openjdk:8-jdk-alpine")
TermuxDocker("ps")

print("====================")
print("* Test TermuxDocker run *")
print("====================")

# --- EXECMODE P1 ---
print("===================================== execmode = P1")
STRING = "T001: TermuxDocker setup jv == execmode = P1"
ret = TermuxDocker("setup", "jv")
result(ret, STRING)

STRING = "T002: TermuxDocker run jv java -version == execmode = P1"
ret = TermuxDocker("run", "--env=LANG=C", "jv", "java", "-version")
result(ret, STRING)

STRING = "T003: TermuxDocker setup c7 == execmode = P1"
ret = TermuxDocker("setup", "c7")
result(ret, STRING)

STRING = "T004: TermuxDocker run c7 ls --version == execmode = P1"
ret = TermuxDocker("run", "c7", "ls", "--version")
result(ret, STRING)

STRING = "T005: TermuxDocker setup ub22 == execmode = P1"
ret = TermuxDocker("setup", "ub22")
result(ret, STRING)

STRING = "T006: TermuxDocker run ub22 ls --version == execmode = P1"
ret = TermuxDocker("run", "ub22", "ls", "--version")
result(ret, STRING)

# --- EXECMODE P2 ---
print("===================================== execmode = P2")
STRING = "T007: TermuxDocker setup --execmode=P2 jv == execmode = P2"
result(TermuxDocker("setup", "--execmode=P2", "jv"), STRING)

STRING = "T008: TermuxDocker run jv java -version == execmode = P2"
result(TermuxDocker("run", "--env=LANG=C", "jv", "java", "-version"), STRING)

STRING = "T009: TermuxDocker setup --execmode=P2 c7 == execmode = P2"
result(TermuxDocker("setup", "--execmode=P2", "c7"), STRING)

STRING = "T010: TermuxDocker run c7 ls --version == execmode = P2"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T011: TermuxDocker setup --execmode=P2 ub22 == execmode = P2"
result(TermuxDocker("setup", "--execmode=P2", "ub22"), STRING)

STRING = "T012: TermuxDocker run ub22 ls --version == execmode = P2"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- EXECMODE F1 ---
print("===================================== execmode = F1")
STRING = "T013: TermuxDocker setup --execmode=F1 c7 == execmode = F1"
result(TermuxDocker("setup", "--execmode=F1", "c7"), STRING)

STRING = "T014: TermuxDocker run c7 ls --version == execmode = F1"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T015: TermuxDocker setup --execmode=F1 ub22 == execmode = F1"
result(TermuxDocker("setup", "--execmode=F1", "ub22"), STRING)

STRING = "T016: TermuxDocker run ub22 ls --version == execmode = F1"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- EXECMODE F2 ---
print("===================================== execmode = F2")
STRING = "T017: TermuxDocker setup --execmode=F2 c7 == execmode = F2"
result(TermuxDocker("setup", "--execmode=F2", "c7"), STRING)

STRING = "T018: TermuxDocker run c7 ls --version == execmode = F2"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T019: TermuxDocker setup --execmode=F2 ub22 == execmode = F2"
result(TermuxDocker("setup", "--execmode=F2", "ub22"), STRING)

STRING = "T020: TermuxDocker run ub22 ls --version == execmode = F2"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- EXECMODE F3 ---
print("===================================== execmode = F3")
STRING = "T021: TermuxDocker setup --execmode=F3 jv == execmode = F3"
result(TermuxDocker("setup", "--execmode=F3", "jv"), STRING)

STRING = "T022: TermuxDocker run jv java -version == execmode = F3"
result(TermuxDocker("run", "--env=LANG=C", "jv", "java", "-version"), STRING)

STRING = "T023: TermuxDocker setup --execmode=F3 c7 == execmode = F3"
result(TermuxDocker("setup", "--execmode=F3", "c7"), STRING)

STRING = "T024: TermuxDocker run c7 ls --version == execmode = F3"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T025: TermuxDocker setup --execmode=F3 ub22 == execmode = F3"
result(TermuxDocker("setup", "--execmode=F3", "ub22"), STRING)

STRING = "T026: TermuxDocker run ub22 ls --version == execmode = F3"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- EXECMODE F4 ---
print("===================================== execmode = F4")
STRING = "T027: TermuxDocker setup --execmode=F4 jv == execmode = F4"
result(TermuxDocker("setup", "--execmode=F4", "jv"), STRING)

STRING = "T028: TermuxDocker run jv java -version == execmode = F4"
result(TermuxDocker("run", "--env=LANG=C", "jv", "java", "-version"), STRING)

STRING = "T029: TermuxDocker setup --execmode=F4 c7 == execmode = F4"
result(TermuxDocker("setup", "--execmode=F4", "c7"), STRING)

STRING = "T030: TermuxDocker run c7 ls --version == execmode = F4"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T031: TermuxDocker setup --execmode=F4 ub22 == execmode = F4"
result(TermuxDocker("setup", "--execmode=F4", "ub22"), STRING)

STRING = "T032: TermuxDocker run ub22 ls --version == execmode = F4"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- EXECMODE R1 ---
print("===================================== execmode = R1")
STRING = "T033: TermuxDocker setup --execmode=R1 jv == execmode = R1"
result(TermuxDocker("setup", "--execmode=R1", "jv"), STRING)

STRING = "T034: TermuxDocker run jv java -version == execmode = R1"
result(TermuxDocker("run", "--env=LANG=C", "jv", "java", "-version"), STRING)

STRING = "T035: TermuxDocker setup --execmode=R1 c7 == execmode = R1"
result(TermuxDocker("setup", "--execmode=R1", "c7"), STRING)

STRING = "T036: TermuxDocker run c7 ls --version == execmode = R1"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T037: TermuxDocker setup --execmode=R1 ub22 == execmode = R1"
result(TermuxDocker("setup", "--execmode=R1", "ub22"), STRING)

STRING = "T038: TermuxDocker run ub22 ls --version == execmode = R1"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- EXECMODE R2 ---
print("===================================== execmode = R2")
STRING = "T039: TermuxDocker setup --execmode=R2 jv == execmode = R2"
result(TermuxDocker("setup", "--execmode=R2", "jv"), STRING)

STRING = "T040: TermuxDocker run jv java -version == execmode = R2"
result(TermuxDocker("run", "--env=LANG=C", "jv", "java", "-version"), STRING)

STRING = "T041: TermuxDocker setup --execmode=R2 c7 == execmode = R2"
result(TermuxDocker("setup", "--execmode=R2", "c7"), STRING)

STRING = "T042: TermuxDocker run c7 ls --version == execmode = R2"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T043: TermuxDocker setup --execmode=R2 ub22 == execmode = R2"
result(TermuxDocker("setup", "--execmode=R2", "ub22"), STRING)

STRING = "T044: TermuxDocker run ub22 ls --version == execmode = R2"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- EXECMODE R3 ---
print("===================================== execmode = R3")
STRING = "T045: TermuxDocker setup --execmode=R3 jv == execmode = R3"
result(TermuxDocker("setup", "--execmode=R3", "jv"), STRING)

STRING = "T046: TermuxDocker run jv java -version == execmode = R3"
result(TermuxDocker("run", "--env=LANG=C", "jv", "java", "-version"), STRING)

STRING = "T047: TermuxDocker setup --execmode=R3 c7 == execmode = R3"
result(TermuxDocker("setup", "--execmode=R3", "c7"), STRING)

STRING = "T048: TermuxDocker run c7 ls --version == execmode = R3"
result(TermuxDocker("run", "c7", "ls", "--version"), STRING)

STRING = "T049: TermuxDocker setup --execmode=R3 ub22 == execmode = R3"
result(TermuxDocker("setup", "--execmode=R3", "ub22"), STRING)

STRING = "T050: TermuxDocker run ub22 ls --version == execmode = R3"
result(TermuxDocker("run", "ub22", "ls", "--version"), STRING)

# --- Final Report ---
if len(FAILED_TESTS) == 0:
    print(f"{OK_STR}    All tests passed")
    sys.exit(0)
else:
    print(f"{FAIL_STR}    The following tests have failed:")
    for failed in FAILED_TESTS:
        print(f"{FAIL_STR}    {failed}")
    sys.exit(1)
