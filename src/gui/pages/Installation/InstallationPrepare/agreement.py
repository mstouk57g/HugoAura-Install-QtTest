from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from gui.widgets.CustomTextBox import CustomTextBox
from gui.widgets.hex_button import HexButton, ImageTextButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from gui.utils.signals import global_signals

class agreementPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 0, 20, 0)

        top_button_layout = QHBoxLayout()
        top_button_layout.setAlignment(Qt.AlignHCenter)
        self.top_button = ImageTextButton("用户协议", icon_path="resources/agreement.png", font_size=12, v_padding=8, canclick=False)
        self.top_button.setFont(QFont("Microsoft YaHei", 12))
        top_button_layout.addWidget(self.top_button)
        main_layout.addLayout(top_button_layout)

        # 添加自定义文本框
        self.textbox = CustomTextBox(self, cut=20, markdown_enabled=True)
        self.textbox.set_font("Microsoft YaHei", 10)
        self.textbox.set_text_color("black")
        self.textbox.set_editable(False)
        self.textbox.setContentsMargins(0,20,0,20)
        self.textbox.set_link_color("369ffb")
        self.textbox.set_visited_link_color("369ffb")
        # 好像没用。。。

        # 从外部文件读取内容
        try:
            with open("resources/agreement.txt", "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            content = "未找到协议文件：resources/agreement.txt"

        self.textbox.set_text(content)
        self.textbox.set_line_spacing(25, mode="fixed")  # 行间距 25px

        main_layout.addWidget(self.textbox)

        # ========== 水平按钮行 ==========
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignHCenter)  # 水平居中
        button_layout.setSpacing(40)  # 按钮之间间距

        # 左边 style2，右边 style1
        self.btn_disagree = HexButton("    不同意    ", icon_path="resources/CHA.png", font_size=10, style=2)
        self.btn_disagree.setFont(QFont("Microsoft YaHei", 10))
        self.btn_agree = HexButton(" 同意并继续 ", icon_path="resources/GOU.png", font_size=10, style=1)
        self.btn_agree.setFont(QFont("Microsoft YaHei", 10))

        self.btn_disagree.clicked = self.on_disagree_clicked
        self.btn_agree.clicked = self.on_agree_clicked

        button_layout.addWidget(self.btn_disagree)
        button_layout.addWidget(self.btn_agree)
        button_layout.setContentsMargins(0,20,0,0)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def on_disagree_clicked(self):
        """不同意按钮点击事件"""
        global_signals.agreement_donotagree.emit()

    def on_agree_clicked(self):
        """同意并继续按钮点击事件"""
        global_signals.agreement_agreed.emit()