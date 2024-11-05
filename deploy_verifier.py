from installer import install_package, install_node
from utils import rainbow_box, show

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
            # Delete node function可以在installer.py中实现
            pass
        elif option == "3":
            break
        else:
            show("无效的选项。请重试。", "error")


