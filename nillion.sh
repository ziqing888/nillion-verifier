#!/bin/bash

# 控制台输出样式
BOLD=$(tput bold)
NORMAL=$(tput sgr0)
BLUE='\033[1;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# 彩虹颜色定义
RED_RAIN='\033[1;31m'
ORANGE_RAIN='\033[1;33m'
YELLOW_RAIN='\033[1;93m'
GREEN_RAIN='\033[1;32m'
CYAN_RAIN='\033[1;36m'
BLUE_RAIN='\033[1;34m'
PURPLE_RAIN='\033[1;35m'

# 彩虹方框函数，使用细边框字符包围内容
rainbow_box() {
    local width=60  # 设置边框宽度

    # 打印顶部边框
    for ((i=0; i<width; i++)); do
        case $((i % 6)) in
            0) printf "${RED_RAIN}═" ;;
            1) printf "${ORANGE_RAIN}═" ;;
            2) printf "${YELLOW_RAIN}═" ;;
            3) printf "${GREEN_RAIN}═" ;;
            4) printf "${CYAN_RAIN}═" ;;
            5) printf "${BLUE_RAIN}═" ;;
        esac
    done
    echo -e "${RESET}"

    # 打印内容和左右边框
    printf "${RED_RAIN}║${RESET}  ${CYAN_RAIN}${BOLD}🚀 Nillion-验证器 🎮${RESET}                                       ${RED_RAIN}║\n${RESET}"
    printf "${ORANGE_RAIN}║${RESET}  ${BLUE}脚本由子清编写 🌐 欢迎加入 电报频道：${YELLOW}https://t.me/ksqxszq${RESET} ${ORANGE_RAIN}║\n${RESET}"

    # 打印底部边框
    for ((i=0; i<width; i++)); do
        case $((i % 6)) in
            0) printf "${RED_RAIN}═" ;;
            1) printf "${ORANGE_RAIN}═" ;;
            2) printf "${YELLOW_RAIN}═" ;;
            3) printf "${GREEN_RAIN}═" ;;
            4) printf "${CYAN_RAIN}═" ;;
            5) printf "${BLUE_RAIN}═" ;;
        esac
    done
    echo -e "${RESET}"
}

# 显示信息的函数
show() {
    case $2 in
        "error")
            echo -e "${RED}${BOLD}❌ $1${NORMAL}"
            ;;
        "progress")
            echo -e "${YELLOW}${BOLD}⏳ $1${NORMAL}"
            ;;
        *)
            echo -e "${GREEN}${BOLD}✅ $1${NORMAL}"
            ;;
    esac
}

# 安装所需包
install_package() {
    local command=$1
    local name=$2

    if ! command -v $command &> /dev/null; then
        show "$name 未安装。正在安装 $name..." "progress"
        if [[ "$name" == "npm" ]]; then
            curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
            sudo apt-get install -y nodejs
        elif [[ "$name" == "docker" ]]; then
            curl -fsSL https://get.docker.com -o get-docker.sh
            sh get-docker.sh
        else
            sudo apt update && sudo apt install -y $name
        fi
        show "$name 安装成功。"
    else
        show "$name 已经安装。"
    fi
}

# 安装 Node.js 和配置 Nillion 节点
install_node() {
    local credentials_path="nillion/verifier/credentials.json"
    
    if [[ -f $credentials_path ]]; then
        show "找到已有的 credentials.json。" "progress"
        read -p "是否备份并删除它？ (y/n)： " backup_choice
        if [[ "$backup_choice" =~ ^[yY]$ ]]; then
            show "正在将 credentials.json 备份到 nillion-existing-wallet.json..." "progress"
            mv $credentials_path nillion-existing-wallet.json
            show "备份成功。"
            rm $credentials_path
            show "已有的 credentials.json 已删除。"
        else
            show "保留已有的 credentials.json。"
        fi
    fi

    show "正在创建所需目录..." "progress"
    mkdir -p nillion/verifier

    if ! docker image inspect nillion/verifier:v1.0.1 &>/dev/null; then
        show "正在拉取 Nillion verifier Docker 镜像..." "progress"
        docker pull nillion/verifier:v1.0.1
        if [[ $? -ne 0 ]]; then
            show "Docker 镜像拉取失败，请检查 Docker 是否正确安装和运行。" "error"
            return
        fi
    else
        show "Nillion verifier Docker 镜像已存在。"
    fi

    echo
    echo "您想使用已有的钱包还是创建一个新的钱包来运行 verifier 节点？ 🤔"
    read -p "输入 '1' 创建新钱包，或输入 '2' 使用已有钱包：" wallet_choice

    if [[ "$wallet_choice" == "2" ]]; then
        read -p "请输入您的私钥（64位十六进制）：" private_key
        # 检查私钥格式
        if [[ ! "$private_key" =~ ^[0-9a-fA-F]{64}$ ]]; then
            show "无效的私钥格式，请检查后重试。" "error"
            exit 1
        fi
        show "正在生成公钥和地址..." "progress"
        npm install @cosmjs/proto-signing
        node -e "
const { DirectSecp256k1Wallet } = require('@cosmjs/proto-signing');
(async function() {
    const privateKeyBytes = Uint8Array.from('$private_key'.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
    const wallet = await DirectSecp256k1Wallet.fromKey(privateKeyBytes, 'nillion');
    const [{ address, pubkey }] = await wallet.getAccounts();
    console.log(address);
    console.log(Buffer.from(pubkey).toString('hex'));
})();
" > address_and_pubkey.txt

        wallet_address=$(sed -n '1p' address_and_pubkey.txt)
        pub_key=$(sed -n '2p' address_and_pubkey.txt)

        show "地址：$wallet_address"
        show "公钥：$pub_key"

        cat <<EOF > $credentials_path
{
  "priv_key": "$private_key",
  "pub_key": "$pub_key",
  "address": "$wallet_address"
}
EOF
        rm address_and_pubkey.txt
    elif [[ "$wallet_choice" == "1" ]]; then
        show "正在创建新的 verifier 节点..." "progress"
        docker run -v "$(pwd)/nillion/verifier:/var/tmp" nillion/verifier:v1.0.1 initialise

        echo
        echo "现在访问：https://verifier.nillion.com/verifier"
        echo "连接一个新的 Keplr 钱包。"
        echo "请求 faucet 到 nillion 地址：https://faucet.testnet.nillion.com"
        echo

        read -p "您是否已请求 faucet？ (y/n)： " faucet_requested
        if [[ ! "$faucet_requested" =~ ^[yY]$ ]]; then
            show "请请求 faucet 后再试。" "error"
            exit 1
        fi

        echo
        echo "在网站 https://verifier.nillion.com/verifier 上输入以下信息："
        echo -e "地址：${GREEN}$(jq -r '.address' $credentials_path)${NORMAL}"
        echo -e "公钥：${GREEN}$(jq -r '.pub_key' $credentials_path)${NORMAL}"
        echo

        read -p "您是否已在网站上输入地址和公钥？ (y/n)： " info_inputted
        if [[ ! "$info_inputted" =~ ^[yY]$ ]]; then
            show "请输入信息后再试。" "error"
            exit 1
        fi
    else
        show "无效的选择。请选择 1 或 2。" "error"
        return
    fi

    show "正在启动 verifier 节点..." "progress"
    docker run -d --name nillion -v "$(pwd)/nillion/verifier:/var/tmp" nillion/verifier:v1.0.1 verify --rpc-endpoint "https://nillion-testnet-rpc.polkachu.com"
    show "nillion 验证节点启动成功。"

    show "正在显示 nillion 容器日志..." "progress"
    docker logs nillion -fn 50
}

# 删除节点
delete_node() {
    local credentials_path="nillion/verifier/credentials.json"
    
    show "正在将 credentials.json 备份到 nillion-backup.json..." "progress"
    if [[ -f $credentials_path ]]; then
        mv $credentials_path nillion-backup.json
        show "备份成功。"
    else
        show "未找到 credentials.json 进行备份。" "error"
    fi

    show "正在停止并删除 Nillion Docker 容器..." "progress"
    docker ps -a | grep nillion/verifier | awk '{print $1}' | xargs -r docker stop
    docker ps -a | grep nillion/verifier | awk '{print $1}' | xargs -r docker rm

    show "正在删除 verifier 节点..." "progress"
    rm -rf nillion/verifier
    show "verifier 节点已成功删除。"
}

# 主程序
main_menu() {
    rainbow_box
    while true; do
        echo
        echo -e "${CYAN}${BOLD}请选择一个选项：${NORMAL}"
        echo -e "${GREEN}1. 安装 verifier 节点${NORMAL}"
        echo -e "${RED}2. 删除 verifier 节点${NORMAL}"
        echo -e "${YELLOW}3. 退出${NORMAL}"
        echo
        read -p "输入选项 [1-3]: " option
        case $option in
            1) 
                install_package curl "curl"
                install_package docker "docker"
                install_package npm "npm"
                install_node 
                ;;
            2) delete_node ;;
            3) exit 0 ;;
            *) show "无效的选项。请重试。" "error" ;;
        esac
    done
}

# 运行主程序
main_menu
