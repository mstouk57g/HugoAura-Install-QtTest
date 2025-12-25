from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from .agreement import agreementPage
from .showSeewoPath import showSeewoPath
from gui.pages.Loading import LoadingPage
from utils.signals import global_signals

class InstallationPrepare(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.stack = QStackedWidget()

        self.agreement_page = agreementPage()
        self.show_seewo_path_page = showSeewoPath(ifFind=True, findPath="C:\\Program Files (x86)\\Seewo\\SeewoService\\SeewoService_1.5.4.3828\\SeewoServiceAssistant", seewoVersion="1.5.4.3828")
        self.LoadingPage = LoadingPage()

        self.stack.addWidget(self.agreement_page)
        self.stack.addWidget(self.show_seewo_path_page)
        self.stack.addWidget(self.LoadingPage)
        self.v_layout.addWidget(self.stack)

        global_signals.agreement_agreed.connect(self.switch_to_seewo_path)

    def switch_to_seewo_path(self):
        """切换到showSeewoPath页面"""
        self.stack.setCurrentWidget(self.show_seewo_path_page)

    def showLoading(self):
        """显示加载页面"""
        self.stack.setCurrentWidget(self.LoadingPage)

    def resizeEvent(self, event):
        super().resizeEvent(event)