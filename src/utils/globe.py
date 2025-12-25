from PyQt5.QtCore import QObject
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from utils.signals import global_signals
import sys
from pathlib import Path

def openHelpLink():
    QDesktopServices.openUrl(QUrl("https://forum.aurax.cc/"))

def get_resource_file(filename):
    """
    获取资源文件的完整路径，兼容各种运行环境
    Args:
        filename: 资源文件名（如 "background.png"）
    Returns:
        Path: 资源的完整路径对象
    """
    if getattr(sys, 'frozen', False):
        # 打包后的可执行文件
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller 单文件模式
            base_path = Path(sys._MEIPASS)
        else:
            # Nuitka 或其他打包工具
            base_path = Path(sys.executable).parent
    else:
        # 开发环境
        base_path = Path(__file__).parent.parent

    file_path  =  base_path / "resources" / filename
    return Path(str(file_path.resolve())).as_posix()

class GlobalVars(QObject):
    def __init__(self):
        super().__init__()
        self._show_image_container = False

    def set_show_image_container(self, visible):
        """
        控制整个图片容器的可见性
        """
        if self._show_image_container != visible:
            self._show_image_container = visible
            global_signals.TitleImageVisibilityChanged.emit(visible)

    def get_show_image_container(self):
        return self._show_image_container

global_vars = GlobalVars()