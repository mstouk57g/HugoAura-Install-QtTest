from PyQt5.QtCore import QObject
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from utils.signals import global_signals

def openHelpLink():
    QDesktopServices.openUrl(QUrl("https://forum.aurax.cc/"))

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