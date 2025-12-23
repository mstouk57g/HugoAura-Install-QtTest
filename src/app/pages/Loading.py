import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QLinearGradient, QPalette

class LoadingPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口背景为深色渐变
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor(30, 30, 50))
        gradient.setColorAt(1, QColor(10, 10, 20))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建标签显示加载文本
        self.loading_label = QLabel("请稍后…")
        self.loading_label.setAlignment(Qt.AlignCenter)
        font = QFont("Microsoft YaHei", 20)
        self.loading_label.setFont(font)
        self.loading_label.setStyleSheet("color: white;")
        layout.addWidget(self.loading_label)

        # 添加一个简单的动画效果
        self.dot_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_text)
        self.timer.start(500)  # 每500毫秒更新一次

    def animate_text(self):
        # 在文本后添加动态的点
        dots = "." * (self.dot_count % 4)
        self.loading_label.setText(f"请稍后{dots}")
        self.dot_count += 1
