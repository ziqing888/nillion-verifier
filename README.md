# Nillion Verifier 节点指南

本指南涵盖了在 Ubuntu 系统上安装、配置和管理 Nillion Verifier 节点的所有步骤。

---

### 官方控制面板
访问控制面板以查看您的节点状态：[https://verifier.nillion.com/verifier](https://verifier.nillion.com/verifier)

### 水龙头
在您的 [Keplr](https://chromewebstore.google.com/detail/keplr/dmkamcknogkgcdfhhbddcghachkejeap) 钱包中创建一个 Nillion 地址，然后访问 [水龙头](https://faucet.testnet.nillion.com/) 获取测试币。

---

## 安装 Docker
使用以下命令来安装 Docker 和相关依赖：

```bash
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

# 检查 Docker 版本
docker --version
