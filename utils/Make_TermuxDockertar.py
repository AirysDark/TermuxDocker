#!/usr/bin/env python3
import os
import re
import shutil
import tarfile


def make_release():
    # cd .. (Move to the parent directory of the script)
    os.chdir("..")

    # Extract version: VER=`grep "__version__" TermuxDocker/__init__.py|cut -d'"' -f 2`
    version = "unknown"
    init_file = os.path.join("TermuxDocker", "__init__.py")
    if os.path.exists(init_file):
        with open(init_file, "r") as f:
            content = f.read()
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                version = match.group(1)

    print("===========================================================")
    print(f"* This script produces TermuxDocker-{version}.tar.gz, for release *")
    print("===========================================================")

    # Clean up: rm -rf `find . -name '*pycache*'` `find . -name '*.pyc'`
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if "pycache" in d:
                shutil.rmtree(os.path.join(root, d))
        for f in files:
            if f.endswith(".pyc"):
                os.remove(os.path.join(root, f))

    release_dir = f"TermuxDocker-{version}"
    tarball_name = f"{release_dir}.tar.gz"

    # mkdir -p TermuxDocker-${VER}
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)

    # cp -prv TermuxDocker TermuxDocker-${VER}/
    shutil.copytree("TermuxDocker", os.path.join(release_dir, "TermuxDocker"), symlinks=True)

    # ln -s maincmd.py TermuxDocker (inside the release folder)
    # cd TermuxDocker-${VER}/TermuxDocker/ && ln -s maincmd.py TermuxDocker
    link_path = os.path.join(release_dir, "TermuxDocker", "TermuxDocker")
    try:
        os.symlink("maincmd.py", link_path)
    except FileExistsError:
        os.remove(link_path)
        os.symlink("maincmd.py", link_path)

    # tar zcvf TermuxDocker-${VER}.tar.gz TermuxDocker-${VER}
    print(f"Creating archive: {tarball_name}")
    with tarfile.open(tarball_name, "w:gz") as tar:
        tar.add(release_dir, arcname=release_dir)

    # rm -rf TermuxDocker-${VER}
    shutil.rmtree(release_dir)
    print("Release complete.")

if __name__ == "__main__":
    make_release()
