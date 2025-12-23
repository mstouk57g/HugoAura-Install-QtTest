from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGraphicsOpacityEffect, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .hex_button import ImageTextButton

class CustomSection(QWidget):
    """

    部分页面底部的操作栏
    比如是“没有联网或没有GithubAPI之类的

    """
    def __init__(self, text="", icon_path=None, parent=None, font_size=12):
        super().__init__(parent)

        self.text = text
        self.icon_path = icon_path

        # 整体竖直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignCenter)  # 整体居中

        # ---------------- 第一层（就是标题） ----------------
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)

        # 左横线
        self.left_line = QFrame()
        self.left_line.setFrameShape(QFrame.HLine)
        self.left_line.setFrameShadow(QFrame.Plain)
        self.left_line.setStyleSheet("color: white; background-color: white;")
        self.left_line.setFixedHeight(2)
        top_layout.addWidget(self.left_line, alignment=Qt.AlignVCenter)

        # 中间按钮
        self.center_button = ImageTextButton(text=self.text, icon_path=self.icon_path, style=6, v_padding=8, h_padding=8, canclick=False, font_size=font_size)
        top_layout.addWidget(self.center_button, alignment=Qt.AlignVCenter)
        self.center_button.setFont(QFont("Microsoft Yahei", font_size))

        # 右横线
        self.right_line = QFrame()
        self.right_line.setFrameShape(QFrame.HLine)
        self.right_line.setFrameShadow(QFrame.Plain)
        self.right_line.setStyleSheet("color: white; background-color: white;")
        self.right_line.setFixedHeight(2)
        top_layout.addWidget(self.right_line, alignment=Qt.AlignVCenter)

        main_layout.addLayout(top_layout)

        # ---------------- 第二层（放各种功能按钮的那个） ----------------
        self.bottom_container = QWidget()
        self.bottom_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.bottom_layout = QHBoxLayout(self.bottom_container)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(10)
        self.bottom_layout.setAlignment(Qt.AlignCenter)  # 第二层内容居中

        # 设置透明度
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.6)
        self.bottom_container.setGraphicsEffect(opacity_effect)

        main_layout.addWidget(self.bottom_container, alignment=Qt.AlignCenter)  # 第二层居中

        self.setLayout(main_layout)

    def resizeEvent(self, event):
        """动态调整横线长度 = 页面（顶层窗口）宽度的 1/5，整体布局保持紧凑"""
        if self.window():
            total_width = self.window().width()
            line_width = total_width // 5  # 按1/5计算

            self.left_line.setFixedWidth(line_width)
            self.right_line.setFixedWidth(line_width)

            self.adjustSize()

        super().resizeEvent(event)

    def addWidget(self, widget):
        """外部调用，往下层添加控件"""
        widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.bottom_layout.addWidget(widget, alignment=Qt.AlignCenter)

        # 添加控件后调整大小保持紧凑
        self.bottom_container.adjustSize()
        self.adjustSize()