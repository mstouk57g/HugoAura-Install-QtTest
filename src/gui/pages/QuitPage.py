from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from gui.widgets.CustomTextBox import CustomTextBox
from gui.widgets.hex_button import HexButton


class QuitPage(QWidget):
    def __init__(self, ErrorMsg):
        super().__init__()
        self.ErrorMsg = ErrorMsg
        self.initUI()

    def initUI(self):
        # 主布局
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 10, 50, 30)

        # 悲伤表情文字（窗口高度的1/10）
        sad_face = QLabel(": (")
        sad_face.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        sad_face.setStyleSheet("color: #ffffff;")

        # 失败提示文字
        failure_text = QLabel("安装失败，原因如下：")
        failure_text.setAlignment(Qt.AlignLeft)
        failure_text.setFont(QFont("Microsoft YaHei", 14))
        failure_text.setStyleSheet("color: #ffffff;")

        # 添加自定义文本框
        self.textbox = CustomTextBox(self, cut=20)
        self.textbox.set_font("Microsoft YaHei", 10)
        self.textbox.set_text_color("black")
        self.textbox.set_editable(False)
        self.textbox.setContentsMargins(0, 20, 0, 20)
        self.textbox.set_text(self.ErrorMsg)
        self.textbox.set_line_spacing(25, mode="fixed")

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = HexButton(" 关闭安装程序 ", font_size=10, style=2)
        close_button.setFont(QFont("Microsoft YaHei", 10))
        close_button.clicked = self.close_application
        button_layout.addWidget(close_button)

        # 将控件添加到主布局
        layout.addWidget(sad_face)
        layout.addWidget(failure_text)
        layout.addWidget(self.textbox)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # 根据窗口高度设置悲伤表情的字体大小
        self.set_sad_face_font(sad_face)

    def set_sad_face_font(self, label):
        # 根据窗口高度计算字体大小（高度的1/10）
        font_size = max(20, int(self.height() / 10))  # 设置最小字体大小
        font = QFont()
        font.setPointSize(font_size)
        label.setFont(font)

    def resizeEvent(self, event):
        # 窗口大小改变时更新字体大小
        super().resizeEvent(event)
        sad_face = self.findChild(QLabel)
        if sad_face:
            self.set_sad_face_font(sad_face)

    def close_application(self):
        QApplication.quit()
