#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import glob

# --- ANSI Color Codes ---
RED = '\033[1;31m'
GREEN = '\033[1;32m'
BLUE = '\033[1;34m'
PURPLE = '\033[1;36m'
NC = '\033[0m'

OK_STR = f"{GREEN}[OK]{NC}"
FAIL_STR = f"{RED}[FAIL]{NC}"

# --- Global Variables ---
FAILED_TESTS = []
HOME = os.path.expanduser("~")
DEFAULT_UDIR = os.path.join(HOME, ".TermuxDocker-tests")
TEST_UDIR = os.path.join(HOME, ".TermuxDocker-test-h45y7k9X")
TAR_IMAGE = "centos7.tar"
TAR_CONT = "centos7-cont.tar"
TAR_IMAGE_URL = f"https://download.a.incd.pt/TermuxDocker_test/{TAR_IMAGE}"
TAR_CONT_URL = f"https://download.a.incd.pt/TermuxDocker_test/{TAR_CONT}"
DOCKER_IMG = "ubuntu:22.04"
CONT = "ubuntu"

os.environ["TermuxDocker_DIR"] = DEFAULT_UDIR

# --- Path Resolution ---
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

# --- Helper Functions ---
def TermuxDocker(*args, env=None):
    """Executes the TermuxDocker command."""
    cmd = []
    if PYTHON_CMD:
        cmd.append(PYTHON_CMD)
    cmd.append(TermuxDocker_CMD)
    
    # Process arguments (handling lists or strings)
    for arg in args:
        if isinstance(arg, list):
            cmd.extend(arg)
        else:
            cmd.append(str(arg))
    
    current_env = os.environ.copy()
    if env:
        current_env.update(env)
        
    # Using shell=True for some commands that use pipes in the original script
    # otherwise using subprocess.run for standard execution
    try:
        # Check if we need to pipe (like in T014)
        cmd_str = " ".join(cmd)
        if "|" in cmd_str or ">" in cmd_str:
            process = subprocess.run(cmd_str, shell=True, env=current_env)
        else:
            process = subprocess.run(cmd, env=current_env)
        return process.returncode
    except Exception:
        return 1

def TermuxDocker_get_output(*args):
    """Executes TermuxDocker and returns the stdout (mimics backticks)"""
    cmd = []
    if PYTHON_CMD:
        cmd.append(PYTHON_CMD)
    cmd.append(TermuxDocker_CMD)
    cmd.extend(args)
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip(), res.returncode

def result(ret_code, test_string):
    print(" ")
    if ret_code == 0:
        print(f"{OK_STR}    {test_string}")
    else:
        print(f"{FAIL_STR}    {test_string}")
        FAILED_TESTS.append(test_string)
    print("\\" + "_"*132 + "/")
    print("\n " + "_"*132 + " \n/ " + " "*132 + " \\")

def result_inv(ret_code, test_string):
    """Result for tests expected to fail (return 1)"""
    print(" ")
    if ret_code == 1:
        print(f"{OK_STR}    {test_string}")
    else:
        print(f"{FAIL_STR}    {test_string}")
        FAILED_TESTS.append(test_string)
    print("\\" + "_"*132 + "/")
    print("\n " + "_"*132 + " \n/ " + " "*132 + " \\")

# --- Test Start ---
print("=================================================")
print("* This script tests all TermuxDocker CLI and options *")
print("* except the run command and vol. mount options *")
print("=================================================")

# T001
STRING = "T001: TermuxDocker install"
if os.path.isdir(DEFAULT_UDIR):
    print(f"ERROR test directory exists, remove first: {DEFAULT_UDIR}")
    sys.exit(1)

ret = TermuxDocker("install")
if ret == 0:
    # Check if proot exists
    proot_path = os.path.join(DEFAULT_UDIR, "bin", "proot-x86_64")
    if not os.path.exists(proot_path):
        ret = 1
result(ret, STRING)

# T002
STRING = "T002: TermuxDocker install --force"
ret = TermuxDocker("install", "--force")
result(ret, STRING)

# T003 - T005
result(TermuxDocker(), "T003: TermuxDocker (with no options)")
result(TermuxDocker("help", ">/dev/null 2>&1"), "T004: TermuxDocker help")
result(TermuxDocker("-h", ">/dev/null 2>&1"), "T005: TermuxDocker -h")

# T006 - T011
result(TermuxDocker("showconf"), "T006: TermuxDocker showconf")
result(TermuxDocker("version"), "T007: TermuxDocker version")
result(TermuxDocker("-D", "version"), "T008: TermuxDocker -D version")
result(TermuxDocker("--quiet", "version"), "T009: TermuxDocker --quiet version")
result(TermuxDocker("-q", "version"), "T010: TermuxDocker -q version")
result(TermuxDocker("--debug", "version"), "T011: TermuxDocker --debug version")

# T012 - T013
result(TermuxDocker("-V", ">/dev/null 2>&1"), "T012: TermuxDocker -V")
result(TermuxDocker("--version", ">/dev/null 2>&1"), "T013: TermuxDocker --version")

# T014
STRING = "T014: TermuxDocker search -a"
ret = TermuxDocker("search", "-a", "gromacs", "|", "grep", "^gromacs")
result(ret, STRING)

# T015 - T017
result(TermuxDocker("pull", DOCKER_IMG), f"T015: TermuxDocker pull {DOCKER_IMG}")
result(TermuxDocker("--insecure", "pull", DOCKER_IMG), f"T016: TermuxDocker --insecure pull {DOCKER_IMG}")
result(TermuxDocker("verify", DOCKER_IMG), f"T017: TermuxDocker verify {DOCKER_IMG}")

# T018 - T019
result(TermuxDocker("images"), "T018: TermuxDocker images")
result(TermuxDocker("inspect", DOCKER_IMG), f"T019: TermuxDocker inspect (image)")

# T020
STRING = "T020: TermuxDocker -q create " + DOCKER_IMG
CONT_ID, ret = TermuxDocker_get_output("-q", "create", DOCKER_IMG)
result(ret, STRING)

# T021
STRING = f"T021: TermuxDocker create --name={CONT} {DOCKER_IMG}"
CONT_ID_NAME, ret = TermuxDocker_get_output("create", "--name=" + CONT, DOCKER_IMG)
result(ret, STRING)

# T022
result(TermuxDocker("ps"), "T022: TermuxDocker ps")

# T023
STRING = f"T023: TermuxDocker name {CONT_ID}"
ret = TermuxDocker("name", CONT_ID, "conti")
if ret == 0:
    ret = TermuxDocker("ps", "|", "grep", "conti")
result(ret, STRING)

# T024
STRING = "T024: TermuxDocker rmname"
ret = TermuxDocker("rmname", "conti")
if ret == 0:
    ret = TermuxDocker("ps", "|", "grep", CONT_ID)
result(ret, STRING)

# T025 - T026
result(TermuxDocker("inspect", CONT_ID), f"T025: TermuxDocker inspect (container {CONT_ID})")
result(TermuxDocker("clone", "--name=myclone", CONT_ID), f"T026: TermuxDocker clone --name=myclone {CONT_ID}")

# T027
STRING = f"T027: TermuxDocker export -o myexportcont.tar {CONT_ID}"
root_path = os.path.join(DEFAULT_UDIR, "containers", CONT_ID, "ROOT")
subprocess.run(["chmod", "-R", "u+x", root_path])
ret = TermuxDocker("export", "-o", "myexportcont.tar", CONT_ID)
result(ret, STRING)

# T028 - T029
result(TermuxDocker("rm", CONT_ID), f"T028: TermuxDocker rm {CONT_ID}")
result(TermuxDocker("setup", CONT), f"T029: TermuxDocker setup {CONT}")

# T030 - T033
if os.path.exists(TEST_UDIR):
    shutil.rmtree(TEST_UDIR)

result(TermuxDocker("mkrepo", TEST_UDIR), f"T030: TermuxDocker mkrepo {TEST_UDIR}")
result(TermuxDocker("--repo=" + TEST_UDIR, "pull", DOCKER_IMG), "T031: repo pull")
result(TermuxDocker("--repo=" + TEST_UDIR, "verify", DOCKER_IMG), "T032: repo verify")
result(TermuxDocker("verify", DOCKER_IMG, env={"TermuxDocker_DIR": TEST_UDIR}), "T033: env verify")

# T034 - Download and Load
if os.path.exists(TAR_IMAGE): os.remove(TAR_IMAGE)
print(f"Download a docker tar img file {TAR_IMAGE_URL}")
subprocess.run(["wget", "--no-check-certificate", TAR_IMAGE_URL])
result(TermuxDocker("load", "-i", TAR_IMAGE), "T034: TermuxDocker load")

# T035 - T038
result(TermuxDocker("protect", CONT), "T035: TermuxDocker protect")
result_inv(TermuxDocker("rm", CONT), "T036: TermuxDocker rm (protected)")
result(TermuxDocker("unprotect", CONT), "T037: TermuxDocker unprotect")
result(TermuxDocker("rm", CONT), "T038: TermuxDocker rm (unprotected)")

# T039 - T041 - Import
if os.path.exists(TAR_CONT): os.remove(TAR_CONT)
print(f"Download a docker tar container file {TAR_CONT_URL}")
subprocess.run(["wget", "--no-check-certificate", TAR_CONT_URL])
result(TermuxDocker("import", TAR_CONT, "mycentos1:latest"), "T039: import image")
result(TermuxDocker("import", "--tocontainer", "--name=mycont", TAR_CONT), "T040: import to container")
result(TermuxDocker("import", "--clone", "--name=clone_cont", TAR_CONT), "T041: import clone")

# T042 - T045
result(TermuxDocker("rmi", DOCKER_IMG), "T042: TermuxDocker rmi")
result(TermuxDocker("ps", "-m"), "T043: TermuxDocker ps -m")
result(TermuxDocker("ps", "-s", "-m"), "T044: TermuxDocker ps -s -m")
result(TermuxDocker("images", "-l"), "T045: TermuxDocker images -l")

# T046 - T048 (Regression #359)
result(TermuxDocker("pull", "docker.io/python:3-slim"), "T046: regression #359 pull")
result(TermuxDocker("create", "--name=py3slim", "docker.io/python:3-slim"), "T047: regression #359 create")
result(TermuxDocker("run", "py3slim", "python3", "--version"), "T048: regression #359 run")

# T049 - T051 (Regression #168)
result(TermuxDocker("pull", "public.ecr.aws/docker/library/redis"), "T049: regression #168 pull")
result(TermuxDocker("create", "--name=redis", "public.ecr.aws/docker/library/redis"), "T050: regression #168 create")
result(TermuxDocker("run", "redis", "redis-server", "--version"), "T051: regression #168 run")

# T052 - T053
result(TermuxDocker("login", "--username=username", "--password=password"), "T052: TermuxDocker login")
result(TermuxDocker("logout", "-a"), "T053: TermuxDocker logout")

# --- Cleanup ---
print("Clean up files containers and images used in the tests")
for f in ["myexportcont.tar", TEST_UDIR, TAR_IMAGE, TAR_CONT]:
    if os.path.isdir(f): shutil.rmtree(f, ignore_errors=True)
    elif os.path.exists(f): os.remove(f)

for c in ["mycont", "clone_cont", "myclone", "py3slim", "redis"]:
    TermuxDocker("rm", c)
for i in ["mycentos1", "centos:7", "docker.io/python:3-slim", "public.ecr.aws/docker/library/redis"]:
    TermuxDocker("rmi", i)

# --- Final Report ---
if len(FAILED_TESTS) == 0:
    print(f"{OK_STR}    All tests passed")
    sys.exit(0)
else:
    print(f"{FAIL_STR}    The following tests have failed:")
    for test in FAILED_TESTS:
        print(f"{FAIL_STR}    {test}")
    sys.exit(1)
