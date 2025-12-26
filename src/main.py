"""
HugoAura-Install GUI 启动器
"""

import sys
import ctypes
from pathlib import Path
from loguru import logger
import time
import argparse
from utils import uac
from version import __appVer__
import funcs.installer as installer
from config import config

def parse_arguments():
    """
    解析命令行参数

    返回:
        argparse.Namespace: 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description=f"{config.APP_NAME} 管理工具")

    # 版本选择参数组 (互斥)
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument(
        "-v", "--version", help="指定要安装的版本标签, 例如 v1.0.0", type=str
    )
    version_group.add_argument(
        "-p", "--path", help="指定本地安装文件路径 (.asar 文件)", type=str
    )
    version_group.add_argument(
        "-l", "--latest", help="安装最新的稳定版本", action="store_true"
    )
    version_group.add_argument(
        "--pre", help="安装最新的预发行版本", action="store_true"
    )
    version_group.add_argument(
        "--ci", help="安装最新的 CI 版本", action="store_true"
    )

    parser.add_argument("-d", "--dir", help="指定希沃管家安装目录", type=str)
    parser.add_argument(
        "-y", "--yes", help="非交互模式, 自动确认所有操作", action="store_true"
    )
    parser.add_argument(
        "--dry-run", help="不进行实际安装操作, 仅执行下载流程", action="store_true"
    )
    parser.add_argument(
        "--list-exit-codes", help="显示所有退出代码及其释义", action="store_true"
    )
    parser.add_argument(
        "--cli", help="以 CLI 模式启动", action="store_true"
    )

    return parser.parse_args()


def print_exit_codes():
    """
    打印所有退出代码及其释义
    """
    print("退出代码释义:")
    for code, desc in config.EXIT_CODES.items():
        print(f"  {code}: {desc}")


def cli_main():
    """
    主函数, 处理命令行参数并执行提权安装流程
    """
    args = parse_arguments()

    if args.list_exit_codes:
        print_exit_codes()
        sys.exit(0)

    logger.info(f"--- 启动 {config.APP_NAME} 管理工具 ---")
    logger.info(f"管理工具版本: {__appVer__}")
    logger.info(f"EXEC: {sys.executable}")
    logger.info(f"Arg: {sys.argv}")

    has_version_args = args.version or args.path or args.pre or args.latest
    is_double_click = len(sys.argv) == 1

    if not has_version_args and not is_double_click and not args.dry_run:
        args.latest = True

    if not uac.is_admin():
        logger.warning("管理工具需要管理员权限, 准备提权...")
        if not uac.run_as_admin():
            logger.error("提权失败, 请尝试手动使用管理员权限运行")
            if not args.yes:
                logger.info("按回车键退出...")
                input()
            sys.exit(2)  # 权限不足
    else:
        logger.info("管理工具正以管理员权限运行, 即将启动安装流程...")
        success = False
        try:
            success = installer.run_installation(args)
        except Exception as e:
            logger.exception(f"执行安装流程时发生意外错误: {e}")
            success = False
        finally:
            time.sleep(1.0)
            if not args.yes:
                print("\n按回车键退出...")
                input()

            sys.exit(0 if success else 1)

def gui_main():
    from PyQt5.QtWidgets import QApplication
    from gui.window import ImageWindow
    from utils.globe import get_resource_file

    print(get_resource_file("background.png"))

    app = QApplication(sys.argv)
    app.setStyleSheet("""
                                    QWidget {
                                    background-color: transparent;
                                    }

                                    QPushButton#closeButton {
                                        background-color: transparent;
                                        color: white;
                                        border: none;
                                        font: bold 20px;
                                    }

                                    QPushButton#closeButton:hover {
                                        color: red;
                                    }
                                    """)

    window = ImageWindow(background_path=get_resource_file("background.png"), title_image_path=get_resource_file("title.png"), install_image_path=get_resource_file("install.jpg"), icon_path=get_resource_file("aura_black.png"))

    window.Installation_page.setCurrentIndex(0)

    current_size = window.size()
    window.setFixedSize(current_size)
    window.show()
    sys.exit(app.exec_())


# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 在PyInstaller环境中, 需要特殊处理导入
try:
    from logger.initLogger import setup_logger
except ImportError as e:
    print(f"导入logger失败: {e}")
    # 创建一个简单的fallback logger
    def setup_logger():
        print("使用简单日志输出")
        return None

def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """以管理员权限重新运行程序"""
    if is_admin():
        return True

    try:
        # 以管理员权限重新运行程序
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            f'"{__file__}"',
            None,
            1
        )
        return False  # 需要退出当前进程
    except Exception as e:
        print(f"提升权限失败: {e}")
        return False


def show_error_dialog(message):
    """显示错误对话框"""

    try:
        ctypes.windll.user32.MessageBoxW(0, message, "AuraInstaller 错误", 0x10)
    except:
        print(f"错误: {message}")


def main():
    """应用程序入口"""
    try:
        # 检查并提升管理员权限
        if not is_admin():
            print("AuraInstaller 需要管理员权限才能正常工作")
            print("正在请求管理员权限...")
            if not run_as_admin():
                sys.exit(0)  # 已启动新的管理员进程, 退出当前进程

        # 初始化日志系统
        try:
            setup_logger()
        except Exception as e:
            print(f"日志初始化失败: {e}")
            # 继续执行, 不让日志问题阻止程序运行

        if "--cli" in sys.argv:
            # 以 CLI 模式启动
            app = cli_main()
        else:
            # 创建并启动主控制器
            app = gui_main()

    except ImportError as e:
        error_msg = f"模块导入失败: {e}\n\n请确保所有依赖都已正确安装:\n- ttkbootstrap\n- pillow\n- loguru\n- requests"
        show_error_dialog(error_msg)
        print(e)
        sys.exit(1)
    except Exception as e:
        error_msg = f"启动GUI应用失败: {e}"
        logger.error(f"{e}")
        show_error_dialog(error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
    #gui_main() # 单独调试GUI界面时使用