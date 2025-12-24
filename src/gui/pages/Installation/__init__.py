from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from pages.Installation.InstallationPrepare import InstallationPrepare
from pages.Installation.VersionChoose import VersionChoose
from pages.Installation.ResourceDownload import ResourceDownload
from pages.Installation.Install import Install
from pages.Installation.Finish import Finish
from utils.signals import global_signals

from widgets.navbar import NavBar

class Installation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(50, 0, 50, 20)
        self.v_layout.setSpacing(0)
        self.setLayout(self.v_layout)

        # ---------- 导航栏 ----------
        self.nav_items = ["准备安装", "选择版本", "下载资源", "安装资源", "完成安装"]
        self.nav_bar = NavBar(self.nav_items, current_index=0)
        self.nav_bar.setContentsMargins(0, 0, 0, 0)
        self.v_layout.addWidget(self.nav_bar)

        # ---------- 页面堆叠区 ----------
        self.stack = QStackedWidget()
        self.stack.setContentsMargins(20, 10, 20, 20)

        self.v_layout.addWidget(self.stack)

        self.InstallationPrepare = InstallationPrepare()
        self.VersionChoose = VersionChoose()
        self.ResourceDownload = ResourceDownload()
        self.Install = Install()
        self.Finish = Finish()

        global_signals.showSeewoPath_nextStepSignal.connect(self.switchVersionChoose)

        self.addPages([self.InstallationPrepare, self.VersionChoose, self.ResourceDownload, self.Install, self.Finish])

    def resizeEvent(self, event):
        super().resizeEvent(event)

    # ---------- 设置当前页面索引 ----------
    def setCurrentIndex(self, index):
        self.stack.setCurrentIndex(index)
        self.nav_bar.setCurrentIndex(index)

    def switchVersionChoose(self):
        self.setCurrentIndex(1)

    # ---------- 添加页面 ----------
    def addPages(self, pages):
        for page in pages:
            self.stack.addWidget(page)
