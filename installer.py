import subprocess
import os
from utils import show

def install_package(command, name):
    if subprocess.call(["command", "-v", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        show(f"{name} 未安装。正在安装 {name}...", "progress")
        if name == "npm":
            subprocess.run(["wget", "-O", "-", "https://deb.nodesource.com/setup_16.x"], shell=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "nodejs"], shell=True)
        elif name == "docker":
            subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"], shell=True)
            subprocess.run(["sh", "get-docker.sh"], shell=True)
        else:
            subprocess.run(["sudo", "apt", "update"], shell=True)
            subprocess.run(["sudo", "apt", "install", "-y", name], shell=True)
        show(f"{name} 安装成功。")
    else:
        show(f"{name} 已经安装。")

def install_node():
    # Add logic for installing node, e.g., checking credentials and setting up verifier
    pass
