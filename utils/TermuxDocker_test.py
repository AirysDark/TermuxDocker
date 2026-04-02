#!/usr/bin/env python3
"""
TermuxDocker Test Script
Demonstrates basic pull and run functionality.
"""

import os
import sys
from core import image_manager, container

def main():
    print("=== TermuxDocker Test ===")

    # Test image name and tag
    image_name = "hello-world"
    tag = "latest"

    print(f"\nStep 1: Pulling image '{image_name}:{tag}'")
    image_manager.pull_image(image_name, tag)

    print(f"\nStep 2: Running container '{image_name}:{tag}'")
    # Run default shell or command in container
    container.run_container(image_name, tag, cmd="echo Hello from TermuxDocker container!")

    print("\n=== Test Completed Successfully ===")

if __name__ == "__main__":
    main()
