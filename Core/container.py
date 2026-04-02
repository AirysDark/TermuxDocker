import os, subprocess
from .config import load_config

def run_container(image_name: str, tag: str = "latest", cmd="/bin/sh"):
    config = load_config()
    arch = "auto"  # Could be improved to read from image folder
    image_dir = os.path.join(config["images_path"], f"{image_name}_{tag}_{arch}")
    
    if not os.path.exists(image_dir):
        print("Error: Image not found, pull first")
        return
    
    print(f"Running container {image_name}:{tag}...")
    subprocess.run(cmd, cwd=image_dir, shell=True, env={"PATH": "/bin:/usr/bin"})