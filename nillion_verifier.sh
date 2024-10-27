#!/bin/bash

# 菜单函数
function show_menu() {
    echo "=================================="
    echo "        Nillion Verifier 节点      "
    echo "=================================="
    echo "1. 安装 Docker"
    echo "2. 安装 Nillion Verifier"
    echo "3. 启动 Nillion Verifier"
    echo "4. 更新 Nillion Verifier"
    echo "5. 查看节点状态"
    echo "6. 备份节点"
    echo "7. 退出"
    echo "=================================="
    read -p "请选择一个选项: " choice
    return $choice
}

# 安装 Docker
function install_docker() {
    echo "正在安装 Docker..."
    sudo apt update -y && sudo apt upgrade -y
    for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done

    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt update -y && sudo apt upgrade -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    docker --version
    echo "Docker 安装完成。"
}

# 安装 Nillion Verifier
function install_verifier() {
    echo "正在安装 Nillion Verifier..."
    docker pull nillion/verifier:v1.0.1
    mkdir -p $HOME/nillion/verifier
    docker run -v $HOME/nillion/verifier:/var/tmp nillion/verifier:v1.0.1 initialise
    echo "Nillion Verifier 安装完成。"
    echo "请保存生成的 accuser 信息并在 [https://verifier.nillion.com/verifier] 注册您的节点。"
}

# 启动 Nillion Verifier
function start_verifier() {
    echo "正在启动 Nillion Verifier..."
    docker run -d -v $HOME/nillion/verifier:/var/tmp nillion/verifier:v1.0.1 verify --rpc-endpoint "https://testnet-nillion-rpc.lavenderfive.com"
    echo "Nillion Verifier 已启动。"
}

# 更新 Nillion Verifier
function update_verifier() {
    echo "正在更新 Nillion Verifier..."
    container_id=$(docker ps -q -f ancestor=nillion/verifier:v1.0.1)
    if [ -n "$container_id" ]; then
        docker stop $container_id && docker rm $container_id
    fi
    mkdir -p $HOME/nillion/verifier
    cp -r $HOME/nillion/accuser/* $HOME/nillion/verifier/
    docker run -d -v $HOME/nillion/verifier:/var/tmp nillion/verifier:v1.0.1 verify --rpc-endpoint "https://testnet-nillion-rpc.lavenderfive.com"
    echo "Nillion Verifier 已更新，正在进入热身状态（10分钟）。"
}

# 查看节点状态
function check_status() {
    echo "正在检查节点状态..."
    docker ps
    read -p "请输入 Nillion Verifier 容器 ID: " container_id
    docker logs -f -n 100 $container_id
}

# 备份节点
function backup_node() {
    echo "正在备份节点..."
    tar -czvf nillion_backup_$(date +%Y%m%d).tar.gz -C $HOME nillion
    echo "备份完成，已保存为 nillion_backup_$(date +%Y%m%d).tar.gz"
}

# 主程序循环
while true; do
    show_menu
    choice=$?
    case $choice in
        1) install_docker ;;
        2) install_verifier ;;
        3) start_verifier ;;
        4) update_verifier ;;
        5) check_status ;;
        6) backup_node ;;
        7) echo "退出程序。"; exit 0 ;;
        *) echo "无效选项，请重试。" ;;
    esac
done
