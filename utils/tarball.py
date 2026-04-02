#!/usr/bin/env python3
"""
tarball.py
Utility to create, extract, list, and inspect tarballs (.tar, .tar.gz, .tar.xz)
Designed for Python 3 builds and TermuxDocker workflow
"""

import tarfile
import os
import sys

# ----------------------------
# Functions
# ----------------------------
def extract(tar_path, dest_dir="."):
    """
    Extract a tarball (.tar, .tar.gz, .tar.xz) to a destination directory
    """
    if not os.path.exists(tar_path):
        raise FileNotFoundError(f"Tarball not found: {tar_path}")
    os.makedirs(dest_dir, exist_ok=True)

    mode = "r"
    if tar_path.endswith(".tar.gz"):
        mode = "r:gz"
    elif tar_path.endswith(".tar.xz"):
        mode = "r:xz"

    with tarfile.open(tar_path, mode) as tar:
        tar.extractall(path=dest_dir)
    print(f"Extracted {tar_path} → {dest_dir}")


def create(source_dir, tar_path, compress="gz"):
    """
    Create a tarball from a directory
    compress: None, "gz", or "xz"
    """
    if compress == "gz":
        mode = "w:gz"
    elif compress == "xz":
        mode = "w:xz"
    else:
        mode = "w"

    with tarfile.open(tar_path, mode) as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    print(f"Created tarball {tar_path} from {source_dir}")


def list_contents(tar_path):
    """
    List contents of a tarball
    """
    if not os.path.exists(tar_path):
        raise FileNotFoundError(f"Tarball not found: {tar_path}")

    mode = "r"
    if tar_path.endswith(".tar.gz"):
        mode = "r:gz"
    elif tar_path.endswith(".tar.xz"):
        mode = "r:xz"

    with tarfile.open(tar_path, mode) as tar:
        for member in tar.getmembers():
            print(member.name)


# ----------------------------
# CLI interface
# ----------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Tarball utility for build system")
    subparsers = parser.add_subparsers(dest="command")

    # Extract
    extract_parser = subparsers.add_parser("extract", help="Extract tarball")
    extract_parser.add_argument("tar_path", help="Path to tarball")
    extract_parser.add_argument("--dest", default=".", help="Destination directory")

    # Create
    create_parser = subparsers.add_parser("create", help="Create tarball")
    create_parser.add_argument("source_dir", help="Source directory to tar")
    create_parser.add_argument("tar_path", help="Output tarball path")
    create_parser.add_argument("--compress", choices=["gz","xz","none"], default="gz", help="Compression type")

    # List
    list_parser = subparsers.add_parser("list", help="List contents of tarball")
    list_parser.add_argument("tar_path", help="Path to tarball")

    args = parser.parse_args()

    if args.command == "extract":
        extract(args.tar_path, args.dest)
    elif args.command == "create":
        compress = None if args.compress=="none" else args.compress
        create(args.source_dir, args.tar_path, compress)
    elif args.command == "list":
        list_contents(args.tar_path)
    else:
        parser.print_help()
