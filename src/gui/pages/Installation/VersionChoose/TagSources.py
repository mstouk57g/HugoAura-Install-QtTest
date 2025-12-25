from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QSizePolicy, QFrame, QSpacerItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from gui.widgets.TransparentLineEdit import TransparentLineEdit
from gui.widgets.hex_button import ImageTextButton, HexButton
from gui.widgets.BottomSection import CustomSection
from gui.utils.signals import global_signals

class TagSources(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        top_container = QFrame()
        top_container_layout = QVBoxLayout(top_container)
        top_container_layout.setContentsMargins(0, 0, 0, 0)
        top_container_layout.setSpacing(15)

        title = QLabel('获取版本列表')
        title.setAlignment(Qt.AlignHCenter)
        title.setFont(QFont("Microsoft YaHei", 18))
        title.setStyleSheet("QLabel{color:rgb(255,255,255);}")

        # GitHub API输入行
        api_row = QHBoxLayout()
        api_label = QLabel('Github API：')
        api_label.setFont(QFont("Microsoft YaHei", 12))
        api_label.setStyleSheet("QLabel{color:rgb(255,255,255);}")

        self.api_input = TransparentLineEdit()
        self.api_input.setPlaceholderText("请输入Github API地址")
        self.api_input.setText("https://api.github.com")
        self.api_input.setTextColor(QColor(255, 255, 255))
        self.api_input.setTextOpacity(200)
        self.api_input.setCursorPosition(0)
        self.api_input.setFont(QFont("Microsoft YaHei", 12))
        self.api_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.use_default_btn = ImageTextButton("使用默认值", font_size=12, v_padding=8, canclick=True, h_padding=8, style=5)
        self.use_default_btn.setFont(QFont("Microsoft Yahei", 12))

        api_row.addWidget(api_label)
        api_row.addWidget(self.api_input)
        api_row.addWidget(self.use_default_btn)

        top_container_layout.addWidget(title)
        top_container_layout.addLayout(api_row)

        middle_container = QFrame()
        middle_container_layout = QVBoxLayout(middle_container)
        middle_container_layout.setContentsMargins(0, 0, 0, 0)
        middle_container_layout.setAlignment(Qt.AlignCenter)

        self.stacked_widget = QStackedWidget()
        self.button_page = ButtonGroupWidget()
        self.stacked_widget.addWidget(self.button_page)
        middle_container_layout.addWidget(self.stacked_widget)

        bottom_container = QFrame()
        bottom_container_layout = QVBoxLayout(bottom_container)
        bottom_container_layout.setContentsMargins(0, 0, 0, 0)
        bottom_container_layout.setAlignment(Qt.AlignBottom)

        self.select_tag_btn = ImageTextButton("手动选择版本", font_size=10, v_padding=8, canclick=True, h_padding=8, style=5)
        self.select_tag_btn.setFont(QFont("Microsoft YaHei", 10))
        self.select_tag_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.local_file_btn = ImageTextButton("使用本地文件", font_size=10, v_padding=8, canclick=True, h_padding=8, style=5)
        self.local_file_btn.setFont(QFont("Microsoft YaHei", 10))
        self.local_file_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.bottom_section = CustomSection("没有联网或无法连接至GithubAPI？")
        self.bottom_section.setFont(QFont("Microsoft YaHei", 12))
        self.bottom_section.addWidget(self.select_tag_btn)
        self.bottom_section.addWidget(self.local_file_btn)

        bottom_container_layout.addWidget(self.bottom_section)
        bottom_container_layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        main_layout.addWidget(top_container)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(middle_container, 0, Qt.AlignBottom)
        main_layout.addWidget(bottom_container, 0, Qt.AlignBottom)

        self.setLayout(main_layout)

    def on_use_default_clicked(self):
        """使用默认值按钮点击事件"""
        self.api_input.setText("https://api.github.com")
        self.api_input.setCursorPosition(0)

    def on_get_version_clicked(self):
        """获取版本列表按钮点击事件"""
        api_url = self.api_input.text()
        if api_url:
            self.stacked_widget.setCurrentIndex(1)
            self.result_text.append(f"正在获取 {api_url} 的版本列表...")
        else:
            self.result_text.append("请输入GitHub API地址")


class ButtonGroupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        self.get_version_btn = HexButton("   下一步   ", font_size=10, style=1, icon_path="resources/Next.png")
        self.get_version_btn.setFont(QFont("Microsoft Yahei", 12))
        self.get_version_btn.clicked = lambda: global_signals.showVersionViewPage.emit()

        layout.addWidget(self.get_version_btn)
        self.setLayout(layout)