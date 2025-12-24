from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from widgets.hex_button import HexButton
from utils.signals import global_signals

class Home(QWidget): # 点击开始安装按钮的信号

    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------- 整体水平布局 ----------
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(50, 30, 50, 30)
        h_layout.setSpacing(0)
        self.setLayout(h_layout)

        # 左右空白
        left_blank = QWidget()
        right_blank = QWidget()
        left_blank.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_blank.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 中间纵列
        center_widget = QWidget()
        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(10)
        center_widget.setLayout(v_layout)
        center_widget.setMaximumWidth(600)
        center_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 顶部 stretch
        v_layout.addStretch(1)

        # logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/aura.png")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        v_layout.addWidget(logo_label, 4)

        def resize_logo():
            w = logo_label.width()
            h = logo_label.height()
            min_side = min(w, h)
            if not logo_pixmap.isNull():
                scaled = logo_pixmap.scaled(min_side, min_side, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled)
        logo_label.resizeEvent = lambda event: resize_logo()

        # welcome
        welcome_label = QLabel("WELCOME TO")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Microsoft YaHei", 16))
        welcome_label.setStyleSheet("color: rgba(255,255,255,128);")
        v_layout.addWidget(welcome_label, 2)

    # ---------- title 图片 ----------
        title_label = QLabel()
        title_pixmap = QPixmap("resources/title.png")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        v_layout.addWidget(title_label)

        # title 按控件宽度缩放
        def resize_title():
            w = title_label.width()
            if not title_pixmap.isNull():
                scaled = title_pixmap.scaledToWidth(w, Qt.SmoothTransformation)
                title_label.setPixmap(scaled)

        title_label.resizeEvent = lambda event: resize_title()

        # 4️⃣ 描述文字
        desc_label = QLabel("下一代希沃管家注入式修改方案")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setFont(QFont("Microsoft YaHei", 10))
        desc_label.setStyleSheet("color: rgba(255,255,255,230);")
        v_layout.addWidget(desc_label, 1)

        # 开始安装按钮
        button = HexButton(text="开始安装", font_size=12, icon_path="resources/Next.png", style=1, h_padding=25)
        button.setMaximumHeight(60)
        button.setFont(QFont("Microsoft YaHei", 16))
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        v_layout.addSpacing(30)
        v_layout.addWidget(button, 0, Qt.AlignHCenter)

        # 点击按钮发射信号
        button.clicked = lambda: global_signals.Home_InstallationClicked.emit()

        # 底部 stretch
        v_layout.addStretch(1)

        # 添加到水平布局
        h_layout.addWidget(left_blank, 11)
        h_layout.addWidget(center_widget, 10)
        h_layout.addWidget(right_blank, 11)
