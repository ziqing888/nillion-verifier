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
    print(f"""{RED_RAIN}║{RESET}  {CYAN_RAIN}{BOLD}🚀 nillion-验证器 🎮{RESET}                                       {RED_RAIN}║{RESET}""")
    print(f"""{ORANGE_RAIN}║{RESET}  {BLUE}脚本由子清编写 🌐 欢迎加入 电报频道：{YELLOW}https://t.me/ksqxszq{RESET} {ORANGE_RAIN}║{RESET}""")

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

