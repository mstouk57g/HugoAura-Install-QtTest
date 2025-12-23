from PyQt5.QtCore import QObject, pyqtSignal

class GlobalSignals(QObject):
    showSeewoPath_nextStepSignal = pyqtSignal()
    agreement_agreed = pyqtSignal()
    agreement_donotagree = pyqtSignal()
    InstallationPrepare_showErrorSignal = pyqtSignal()
    Home_InstallationClicked = pyqtSignal()
    TitleImageVisibilityChanged = pyqtSignal(bool)

    showVersionViewPage = pyqtSignal()
    showTagSourcePage = pyqtSignal()
    showVersionSelectorMainPage = pyqtSignal()
    showVersionSelectorAikariPage = pyqtSignal()

global_signals = GlobalSignals()