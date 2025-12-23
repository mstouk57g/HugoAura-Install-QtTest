from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from .TagSources import TagSources
from .VersionsView import VersionsView
from .VersionSelector import VersionSelector
from pages.Loading import LoadingPage
from utils.signals import global_signals

class VersionChoose(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.stack = QStackedWidget()

        self.TagSourcesPage = TagSources()
        self.VersionsViewPage = VersionsView()
        self.LoadingPage = LoadingPage()

        self.VersionSelectorMainPage = VersionSelector(mode="main")
        self.VersionSelectorAikariPage = VersionSelector(mode="aikari")

        self.stack.addWidget(self.TagSourcesPage)
        self.stack.addWidget(self.VersionsViewPage)
        self.stack.addWidget(self.VersionSelectorMainPage)
        self.stack.addWidget(self.VersionSelectorAikariPage)

        self.v_layout.addWidget(self.stack)
        global_signals.showVersionViewPage.connect(self.switchVersionChoose)
        global_signals.showTagSourcePage.connect(self.switchGitHubApi)
        global_signals.showVersionSelectorMainPage.connect(self.switchMainVersionChooser)
        global_signals.showVersionSelectorAikariPage.connect(self.switchAikariVersionChooser)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def switchVersionChoose(self):
        self.stack.setCurrentIndex(1)

    def switchGitHubApi(self):
        self.stack.setCurrentIndex(0)

    def switchMainVersionChooser(self):
        self.stack.setCurrentIndex(2)

    def switchAikariVersionChooser(self):
        self.stack.setCurrentIndex(3)