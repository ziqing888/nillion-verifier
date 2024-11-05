# Nillion 验证节点设置指南


该指南为您提供有关如何使用 Bash 脚本安装和管理 Nillion 验证节点的详细步骤。

### 脚本功能概述

该脚本包含以下主要功能：

1. **安装和配置环境**：检查并安装所需的软件包，如 `npm`、`docker` 等。
2. **安装和配置验证节点**：可以选择创建新的钱包或使用已有钱包来运行验证节点。
3. **删除验证节点**：备份节点凭据并安全删除节点容器。

### 一键脚本运行步骤

您可以通过以下一键命令来下载、授予权限并运行该脚本：

```sh
[ -f "nillion.sh" ] && rm nillion.sh; wget -q -O nillion.sh https://raw.githubusercontent.com/ziqing888/nillion-verifier/refs/heads/main/nillion.sh && chmod +x nillion.sh && ./nillion.sh

```

运行脚本后，脚本会提供以下三个选项：
- **安装 verifier 节点**：输入 `1` 进行安装。
- **删除 verifier 节点**：输入 `2` 删除现有节点。
- **退出**：输入 `3` 退出脚本。

### 功能详解

#### 1. 安装所需的软件包

在运行脚本的过程中，脚本会自动检查系统中是否安装了 `jq`、`npm` 和 `docker`，并在缺少这些工具时安装它们。
- **npm**：用于安装 Node.js 相关依赖。
- **Docker**：用于部署和运行 Nillion 验证节点。

#### 2. 安装验证节点

- **使用已有钱包**：
  - 选择输入 `2`，您需要提供已有钱包的私钥。
  - 脚本会自动生成公钥和钱包地址，并将这些信息保存到 `credentials.json` 文件中。
- **创建新钱包**：
  - 选择输入 `1`，脚本会运行 Docker 容器来初始化一个新的钱包。
  - 随后，您需要访问 [https://verifier.nillion.com/verifier](https://verifier.nillion.com/verifier) 并连接一个新的 Keplr 钱包。
  - 请求测试币水龙头到生成的钱包地址，地址为 [https://faucet.testnet.nillion.com](https://faucet.testnet.nillion.com)。

#### 3. 删除验证节点

- 脚本会备份现有的 `credentials.json` 文件，以防止数据丢失。
- 停止并删除与验证节点相关的 Docker 容器。
- 删除验证节点的数据文件夹。

### 常见问题及解决办法

1. **Docker 未安装或未正确配置**
   - 如果您在脚本运行时看到 Docker 相关错误，请确保 Docker 已正确安装并配置。
   - 可以通过以下命令来检查 Docker 的状态：
     ```sh
     sudo systemctl status docker
     ```

2. **凭据备份**
   - 安装新节点前，脚本会询问您是否备份已有的 `credentials.json` 文件。请确保进行备份，以避免因文件丢失而失去对节点的访问权限。

3. **网络连接问题**
   - 如果验证节点无法正常启动，请确保您的网络可以访问 Nillion 的 RPC 端点。

### 注意事项

- 该脚本需要管理员权限来安装 Docker 和其他依赖项。在运行期间可能会要求输入管理员密码。
- 在脚本运行时，请确保具有稳定的网络连接，以便成功下载 Docker 镜像和其他依赖。
- 请确保 `credentials.json` 文件的备份和保存位置安全，以防止数据丢失。

通过此指南，您应该能够顺利安装和管理 Nillion 验证节点。如果在运行过程中遇到任何问题，请随时寻求帮助。



## 联系与支持
- 如需进一步帮助，请随时加入我们的 Telegram 频道：[https://t.me/ksqxszq](https://t.me/ksqxszq)。



