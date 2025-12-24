from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QSizePolicy
from PyQt5.QtCore import Qt
from utils.signals import global_signals
from PyQt5.QtGui import QPixmap, QFont, QColor

from widgets.TransparentLineEdit import TransparentLineEdit
from widgets.hex_button import ImageTextButton, HexButton
from widgets.BottomSection import CustomSection
from utils.globe import openHelpLink

class showSeewoPath(QWidget):
    def __init__(self, ifFind=False, findPath=None, seewoVersion=None):
        super().__init__()
        if ifFind and findPath:
            self.showText = "希沃管家安装目录匹配成功"
            self.findPath = findPath
            self.showPic = "resources/FileOk.png"
            self.seewoVersion = "希沃管家版本：" + str(seewoVersion)
            self.nextAvilable = True
        else:
            self.showText = "未找到希沃管家安装目录"
            self.findPath = None
            self.showPic = "resources/FileNo.png"
            self.seewoVersion = None
            self.nextAvilable = False
        self.initUI()

    def initUI(self):
        # 主垂直布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(40, 30, 40, 30)

        # 第一层
        first_layer = QHBoxLayout()
        first_layer.setSpacing(30)

        # 左侧图片容器
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.original_pixmap = QPixmap(self.showPic)
        self.image_label.setPixmap(self.original_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)

        left_layout.addStretch()
        left_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        left_layout.addStretch()

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # 成功提示文字
        success_label = QLabel(self.showText)
        success_label.setStyleSheet("color: rgba(255, 255, 255, 1);")
        success_label.setFont(QFont("Microsoft YaHei", 25))
        success_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # 安装目录提示文字
        dir_label = QLabel("安装目录：")
        dir_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        dir_label.setFont(QFont("Microsoft YaHei", 15))
        dir_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # 目录文本框
        self.text_edit = TransparentLineEdit()
        self.text_edit.setPlaceholderText("请输入希沃管家安装目录...")
        self.text_edit.setText(self.findPath)
        self.text_edit.setTextColor(QColor(255, 255, 255))
        self.text_edit.setTextOpacity(200)
        self.text_edit.setCursorPosition(0)
        self.text_edit.setFont(QFont("Microsoft YaHei", 12))
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 手动选择按钮
        self.pathChoose = ImageTextButton("手动选择", icon_path="resources/FileCh.png",
                                         font_size=10, v_padding=8, canclick=True, h_padding=8)
        self.pathChoose.setFont(QFont("Microsoft YaHei", 10))
        self.pathChoose.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pathChoose.clicked = self.openDirectoryDialog

        # 添加到布局
        right_layout.addStretch()
        right_layout.addWidget(success_label)
        right_layout.addWidget(dir_label)
        right_layout.addWidget(self.text_edit)
        right_layout.addWidget(self.pathChoose, alignment=Qt.AlignLeft)
        right_layout.addStretch()

        # 添加到第一层
        first_layer.addWidget(left_container, 1)  # 左侧占1份
        first_layer.addWidget(right_widget, 2)    # 右侧占2份

        # 第二层 - 版本信息
        version_label = QLabel(self.seewoVersion)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        version_label.setFont(QFont("Microsoft YaHei", 9))
        version_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # 第三层 - 按钮容器
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)  # 设置按钮间距

        # 下一步按钮
        self.btn_next = HexButton("   下一步   ", icon_path="resources/next.png",
                                  font_size=10, style=1)
        self.btn_next.setFont(QFont("Microsoft YaHei", 10))
        self.btn_next.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_next.setVisible(self.nextAvilable)
        self.btn_next.clicked = self.nextStep

        # 添加动作按钮
        self.InstallPathHelp = ImageTextButton("获取帮助", icon_path="resources/help.png",
                                                    font_size=10, v_padding=8, canclick=True, h_padding=8, style=5)
        self.InstallPathHelp.setFont(QFont("Microsoft YaHei", 10))
        self.InstallPathHelp.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.InstallPathHelp.clicked = openHelpLink

        self.bottomSection = CustomSection("输入安装目录以继续")
        self.bottomSection.setFont(QFont("Microsoft YaHei", 12))
        self.bottomSection.addWidget(self.InstallPathHelp)
        self.bottomSection.setVisible(not self.nextAvilable)

        # 将两个按钮添加到按钮布局中
        button_layout.addStretch()
        button_layout.addWidget(self.btn_next)
        button_layout.addWidget(self.bottomSection)
        button_layout.addStretch()

        # 添加到主布局
        main_layout.addLayout(first_layer)
        main_layout.addWidget(version_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def resizeEvent(self, event):
        if hasattr(self, 'original_pixmap') and not self.original_pixmap.isNull():
            # 获取右侧内容的高度
            right_widget = self.findChild(QWidget)
            if right_widget:
                right_height = right_widget.height()-60

                # 计算等比例缩放后的尺寸
                original_size = self.original_pixmap.size()
                original_width = original_size.width()
                original_height = original_size.height()

                # 根据高度计算宽度
                scaled_width = int(original_width * right_height / original_height)

                # 设置缩放后的图片
                scaled_pixmap = self.original_pixmap.scaled(
                    scaled_width, right_height,
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setFixedSize(scaled_width, right_height)

        super().resizeEvent(event)

    def openDirectoryDialog(self):
        """打开目录选择对话框"""
        # 打开目录选择对话框
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择希沃管家安装目录（SeewoServiceAssistant文件夹）",  # 对话框标题
            "C:\\Program Files (x86)\\Seewo\\SeewoService",  # 初始目录
            QFileDialog.ShowDirsOnly
        )

        # 如果用户选择了目录
        if directory:
            self.text_edit.setText(directory)
            self.text_edit.setCursorPosition(0)

    def nextStep(self):
        global_signals.showSeewoPath_nextStepSignal.emit()
