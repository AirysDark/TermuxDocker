import os, tarfile, requests
from .config import load_config

def get_architecture():
    import platform
    arch = platform.machine()
    if arch in ["aarch64", "arm64"]:
        return "arm64"
    elif arch in ["x86_64", "amd64"]:
        return "amd64"
    else:
        return "unknown"

def pull_image(image_name: str, tag: str = "latest"):
    config = load_config()
    arch = get_architecture() if config["default_arch"] == "auto" else config["default_arch"]
    image_dir = os.path.join(config["images_path"], f"{image_name}_{tag}_{arch}")
    os.makedirs(image_dir, exist_ok=True)
    
    print(f"Pulling image {image_name}:{tag} for {arch}...")

    # Simplified example: just download a tarball from a fixed URL for demo
    tar_url = f"https://github.com/AirysDark/TermuxDockerImages/raw/main/{image_name}_{tag}_{arch}.tar"
    tar_path = os.path.join(image_dir, "image.tar")
    
    r = requests.get(tar_url, stream=True)
    if r.status_code != 200:
        print("Error: Image not found on server")
        return
    
    with open(tar_path, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    
    print("Extracting image...")
    with tarfile.open(tar_path) as tf:
        tf.extractall(image_dir)
    print(f"Image {image_name}:{tag} ready at {image_dir}")