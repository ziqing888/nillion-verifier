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
    credentials_path = "nillion/verifier/credentials.json"
    if os.path.isfile(credentials_path):
        show("找到已有的 credentials.json。是否备份并删除它？ (y/n)：", "progress")
        backup_choice = input("输入 'y' 进行备份并删除，或输入其他键保留：")
        if backup_choice.lower() == 'y':
            show("正在将 credentials.json 备份到 nillion-existing-wallet.json...", "progress")
            os.rename(credentials_path, "nillion-existing-wallet.json")
            show("备份成功。")
            os.remove(credentials_path)
            show("已有的 credentials.json 已删除。")
        else:
            show("保留已有的 credentials.json。")

    show("正在创建所需目录...", "progress")
    os.makedirs("nillion/verifier", exist_ok=True)

    show("正在拉取 Nillion verifier Docker 镜像...", "progress")
    result = subprocess.run(["docker", "pull", "nillion/verifier:v1.0.1"], shell=True)
    if result.returncode != 0:
        show("Docker 镜像拉取失败，请检查 Docker 是否正确安装和运行。", "error")
        return
    else:
        show("Docker 镜像拉取成功。")

    # 添加更多逻辑，根据已有或新建钱包进行节点安装

