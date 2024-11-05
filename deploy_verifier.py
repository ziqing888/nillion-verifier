import os
import subprocess
import time

BOLD = "\033[1m"
NORMAL = "\033[0m"
BLUE = "\033[1;34m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
RESET = "\033[0m"

RED_RAIN = "\033[1;31m"
ORANGE_RAIN = "\033[1;33m"
YELLOW_RAIN = "\033[1;93m"
GREEN_RAIN = "\033[1;32m"
CYAN_RAIN = "\033[1;36m"
BLUE_RAIN = "\033[1;34m"
PURPLE_RAIN = "\033[1;35m"


def rainbow_box():
    width = 60

    # Print top border
    for i in range(width):
        color = [RED_RAIN, ORANGE_RAIN, YELLOW_RAIN, GREEN_RAIN, CYAN_RAIN, BLUE_RAIN][i % 6]
        print(f"{color}═", end="")
    print(RESET)

    # Print content and side borders
    print(f"{RED_RAIN}║{RESET}  {CYAN_RAIN}{BOLD}🚀 nillion-验证器
 🎮{RESET}                                       {RED_RAIN}║{RESET}")
    print(f"{ORANGE_RAIN}║{RESET}  {BLUE}脚本由子清编写 🌐 欢迎加入 电报频道：{YELLOW}https://t.me/ksqxszq{RESET} {ORANGE_RAIN}║{RESET}")

    # Print bottom border
    for i in range(width):
        color = [RED_RAIN, ORANGE_RAIN, YELLOW_RAIN, GREEN_RAIN, CYAN_RAIN, BLUE_RAIN][i % 6]
        print(f"{color}═", end="")
    print(RESET)


def show(message, msg_type="success"):
    if msg_type == "error":
        print(f"{RED}{BOLD}❌ {message}{NORMAL}")
    elif msg_type == "progress":
        print(f"{YELLOW}{BOLD}⏳ {message}{NORMAL}")
    else:
        print(f"{GREEN}{BOLD}✅ {message}{NORMAL}")


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

    if subprocess.call(["docker", "image", "inspect", "nillion/verifier:v1.0.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        show("正在拉取 Nillion verifier Docker 镜像...", "progress")
        subprocess.run(["docker", "pull", "nillion/verifier:v1.0.1"], shell=True)
    else:
        show("Nillion verifier Docker 镜像已存在。")

    print("\n您想使用已有的钱包还是创建一个新的钱包来运行 verifier 节点？ 🤔")
    wallet_choice = input("输入 '1' 创建新钱包，或输入 '2' 使用已有钱包：")

    if wallet_choice == "2":
        private_key = input("输入您的私钥：")
        show("正在生成公钥和地址...", "progress")
        subprocess.run(["npm", "install", "@cosmjs/proto-signing"], shell=True)
        with open("address_and_pubkey.txt", "w") as f:
            subprocess.run([
                "node", "-e",
                f"""
const {{ DirectSecp256k1Wallet }} = require('@cosmjs/proto-signing');

(async function() {{
    const privateKeyBytes = Uint8Array.from(
        "{private_key}".match(/.{1,2}/g).map(byte => parseInt(byte, 16))
    );
    const wallet = await DirectSecp256k1Wallet.fromKey(privateKeyBytes, 'nillion');
    const [{{ address, pubkey }}] = await wallet.getAccounts();
    console.log(address);
    console.log(Buffer.from(pubkey).toString('hex'));
}})();
                """
            ], stdout=f, shell=True)

        with open("address_and_pubkey.txt") as f:
            wallet_address = f.readline().strip()
            pub_key = f.readline().strip()

        show(f"地址：{wallet_address}")
        show(f"公钥：{pub_key}")

        with open(credentials_path, "w") as f:
            f.write(f"{{\n  \"priv_key\": \"{private_key}\",\n  \"pub_key\": \"{pub_key}\",\n  \"address\": \"{wallet_address}\"\n}}")
        os.remove("address_and_pubkey.txt")

    elif wallet_choice == "1":
        show("正在创建新的 verifier 节点...", "progress")
        subprocess.run(["docker", "run", "-v", "./nillion/verifier:/var/tmp", "nillion/verifier:v1.0.1", "initialise"], shell=True)

        print("\n现在访问：https://verifier.nillion.com/verifier")
        print("连接一个新的 Keplr 钱包。")
        print("请求 faucet 到 nillion 地址：https://faucet.testnet.nillion.com\n")

        faucet_requested = input("您是否已请求 faucet？ (y/n)：")
        if faucet_requested.lower() != 'y':
            show("请请求 faucet 后再试。", "error")
            return

        print("\n在网站 https://verifier.nillion.com/verifier 上输入以下信息：")
        subprocess.run(["jq", "-r", "'.address'", credentials_path], shell=True)
        subprocess.run(["jq", "-r", "'.pub_key'", credentials_path], shell=True)

        info_inputted = input("您是否已在网站上输入地址和公钥？ (y/n)：")
        if info_inputted.lower() != 'y':
            show("请输入信息后再试。", "error")
            return
    else:
        show("无效的选择。请选择 1 或 2。", "error")
        return

    show("正在启动 verifier 节点...", "progress")
    subprocess.run([
        "sudo", "docker", "run", "-d", "--name", "nillion",
        "-v", "./nillion/verifier:/var/tmp", "nillion/verifier:v1.0.1", "verify",
        "--rpc-endpoint", "https://nillion-testnet-rpc.polkachu.com"
    ], shell=True)

    show("正在显示 nillion 容器日志...", "progress")
    subprocess.run(["sudo", "docker", "logs", "nillion", "-fn", "50"], shell=True)


def delete_node():
    credentials_path = "nillion/verifier/credentials.json"
    backup_path = "nillion-backup.json"

    show("正在将 credentials.json 备份到 nillion-backup.json...", "progress")
    if os.path.isfile(credentials_path):
        os.rename(credentials_path, backup_path)
        show("备份成功。")
    else:
        show("未找到 credentials.json 进行备份。", "error")

    show("正在停止并删除 Nillion Docker 容器...", "progress")
    subprocess.run(["sudo", "docker", "stop", "nillion"], stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo", "docker", "rm", "nillion"], stderr=subprocess.DEVNULL, shell=True)

    show("正在删除 verifier 节点...", "progress")
    if os.path.isdir("nillion/verifier"):
        os.rmdir("nillion/verifier")
        show("verifier 节点删除成功。")


if __name__ == "__main__":
    rainbow_box()
    while True:
        print("\n1. 安装 verifier 节点")
        print("2. 删除 verifier 节点")
        print("3. 退出\n")
        option = input("请选择一个选项：")
        if option == "1":
            install_node()
        elif option == "2":
            delete_node()
        elif option == "3":
            break
        else:
            show("无效的选项。请重试。", "error")
