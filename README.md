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


安装 Nillion Verifier
安装步骤如下：

拉取 Docker 镜像

bash
复制代码
docker pull nillion/verifier:v1.0.1
创建文件夹

bash
复制代码
mkdir -p nillion/verifier
初始化 Verifier

bash
复制代码
docker run -v $HOME/nillion/verifier:/var/tmp nillion/verifier:v1.0.1 initialise
此命令会输出注册 accuser 所需的详细信息，请务必保存：

account_id：accuser 的 Nillion 地址
public_key：accuser 的公钥
注意： accuser 的凭证会存储在 credentials.json 文件中，请妥善保存此文件，否则您将无法访问 accuser 的密钥或地址。

检查 credentials.json 文件内容

bash
复制代码
cat $HOME/nillion/verifier/credentials.json
向 Verifier 的 accuser 地址发送一些 $NIL 或通过水龙头获取测试币

启动 Verifier
使用以下命令启动 Nillion Verifier：

bash
复制代码
docker run -d -v $HOME/nillion/verifier:/var/tmp nillion/verifier:v1.0.1 verify --rpc-endpoint "https://testnet-nillion-rpc.lavenderfive.com"
在控制面板中验证节点
前往 Verifier 控制面板。
点击 Linux setup 以查看 Verifier 安装文档，在步骤 5 中添加您的节点凭证以验证您的节点。
检查节点状态
1. 查看 Docker 容器列表

bash
复制代码
docker ps
复制 nillion/retailtoken-accuser:latest 容器的 ID。
2. 查看已验证的最新密钥（将 CONTAINER_ID 替换为您的 ID）

bash
复制代码
docker logs -f -n 100 CONTAINER_ID
数量必须在增加
Registered 状态必须为 true
备份节点
备份 nillion/verifier/credentials.json 文件。
或将整个 nillion 文件夹保存到您的计算机中。
在 Verifier 上质押 ETH（反 Sybil 攻击）
您必须在 Verifier 上质押至少 0.05 ETH，以支持反 Sybil 机制。
官方声明此操作非强制，但建议进行质押。

常用命令：如果在运行 Verifier 时遇到任何错误
重启容器

bash
复制代码
docker restart CONTAINER_ID
停止并移除容器

bash
复制代码
docker stop CONTAINER_ID && docker rm CONTAINER_ID
然后使用“启动 Verifier”命令重新运行 Verifier。

更新 Nillion Verifier
查看 Docker 容器列表
复制 nillion/verifier 的容器 ID

bash
复制代码
docker ps
停止当前 Verifier
将 CONTAINER_ID 替换为实际 ID

bash
复制代码
docker stop CONTAINER_ID
docker rm CONTAINER_ID
转移 Accuser 内容到 Verifier
bash
复制代码
cd $HOME
mkdir -p nillion/verifier
cp -r nillion/accuser/* nillion/verifier/
重启 Verifier
bash
复制代码
docker run -d -v $HOME/nillion/verifier:/var/tmp nillion/verifier:v1.0.1 verify --rpc-endpoint "https://testnet-nillion-rpc.lavenderfive.com"
更新后，Verifier 将进入一个 10 分钟的热身期。在此期间，如果网络不需要验证，您的节点状态将显示“Verifying: False”。一旦开始工作，状态将显示“Verifying: true”。

以上步骤完成后，您的 Nillion Verifier 节点应该已成功配置并在验证网络中正常工作。确保定期检查节点状态和备份重要文件。

go
复制代码

将以上内容复制到 `README.md` 文件中后，您将拥有一个包含完整指南的文档，便于用户设置和管理 Nillion Verifier 节点。





