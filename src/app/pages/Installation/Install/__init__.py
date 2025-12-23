from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class Install(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("这是页面 4")
        label.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)
