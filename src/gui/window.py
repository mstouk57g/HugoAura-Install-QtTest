from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt, QPoint, QRect
from gui.pages.Home import Home
from gui.pages.Installation import Installation
from utils.globe import global_vars
from utils.signals import global_signals
from gui.pages.QuitPage import QuitPage

class ImageWindow(QWidget):
    def __init__(self, background_path, title_image_path=None, install_image_path=None, icon_path=None, parent=None):
        super().__init__(parent)

        # 背景、标题图、安装图和图标
        self.pixmap = QPixmap(background_path)
        self.title_pixmap = QPixmap(title_image_path) if title_image_path else None
        self.install_pixmap = QPixmap(install_image_path) if install_image_path else None
        self.icon_pixmap = QPixmap(icon_path) if icon_path else None

        # 设置窗口图标和标题（显示在任务栏）
        if self.icon_pixmap and not self.icon_pixmap.isNull():
            self.setWindowIcon(QIcon(self.icon_pixmap))
        self.setWindowTitle("HugoAura Install")

        # 固定窗口宽度为屏幕宽度的4/7，高度由背景图片等比例缩放决定
        screen = self.screen().availableGeometry()
        win_width = screen.width() * 4 // 7

        if not self.pixmap.isNull():
            pixmap_ratio = self.pixmap.height() / self.pixmap.width()
            win_height = int(win_width * pixmap_ratio)
        else:
            win_height = win_width * 3 // 4

        self.resize(win_width, win_height)
        self.move((screen.width() - win_width)//2, (screen.height() - win_height)//2)

        self.setWindowFlags(Qt.FramelessWindowHint)

        # ---------- 主布局 ----------
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0,0,0,0)
        self.v_layout.setSpacing(0)
        self.setLayout(self.v_layout)

        # ---------- 自定义标题栏 ----------
        self.title_bar = QWidget()
        title_bar_height = self.height() // 10
        self.title_bar.setFixedHeight(title_bar_height)
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0,0,0,0)
        self.title_layout.setSpacing(0)
        self.title_bar.setLayout(self.title_layout)

        # 添加标题图片和安装图片到标题栏左边
        self.title_margin = 20
        if (self.title_pixmap and not self.title_pixmap.isNull()) or (self.install_pixmap and not self.install_pixmap.isNull()):
            # 创建容器widget来添加间距
            self.image_container = QWidget()
            self.image_container_layout = QHBoxLayout()
            self.image_container_layout.setContentsMargins(0, self.title_margin, 0, self.title_margin)
            self.image_container_layout.setSpacing(10)
            self.image_container.setLayout(self.image_container_layout)

            # 添加标题图片
            if self.title_pixmap and not self.title_pixmap.isNull():
                self.title_image_label = QLabel()
                available_height = title_bar_height - 2 * self.title_margin
                scaled_title_pixmap = self.title_pixmap.scaledToHeight(
                    available_height, Qt.SmoothTransformation
                )
                self.title_image_label.setPixmap(scaled_title_pixmap)
                self.title_image_label.setFixedSize(scaled_title_pixmap.size())
                self.image_container_layout.addWidget(self.title_image_label)

            # 添加安装图片
            if self.install_pixmap and not self.install_pixmap.isNull():
                self.install_image_label = QLabel()
                available_height = title_bar_height - 2 * self.title_margin
                scaled_install_pixmap = self.install_pixmap.scaledToHeight(
                    available_height, Qt.SmoothTransformation
                )
                self.install_image_label.setPixmap(scaled_install_pixmap)
                self.install_image_label.setFixedSize(scaled_install_pixmap.size())
                self.image_container_layout.addWidget(self.install_image_label)

            # 根据全局变量设置整个图片容器的初始可见性
            self.image_container.setVisible(global_vars.get_show_image_container())

            self.title_layout.addWidget(self.image_container)
        else:
            self.title_layout.addSpacing(0)

        self.title_layout.setContentsMargins(self.title_margin, 0, self.title_margin, 0)
        self.title_layout.addStretch()

        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setFixedSize(40, title_bar_height)
        self.close_btn.clicked.connect(self.close)
        self.title_layout.addWidget(self.close_btn)
        self.v_layout.addWidget(self.title_bar)

        # ---------- 页面容器 ----------
        self.frame_container = QWidget()
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setContentsMargins(0,0,0,0)
        self.frame_layout.setSpacing(0)
        self.frame_container.setLayout(self.frame_layout)
        self.v_layout.addWidget(self.frame_container)

        # 添加页面
        self.Home = Home()
        self.frame_layout.addWidget(self.Home)

        self.Installation_page = Installation()
        self.Installation_page.hide()
        self.frame_layout.addWidget(self.Installation_page)

        global_signals.Home_InstallationClicked.connect(self.showInstallation)

        # 连接全局变量信号
        global_signals.TitleImageVisibilityChanged.connect(self.on_TitleImageVisibilityChanged)
        global_signals.agreement_donotagree.connect(self.showDonotagreeErrorPage)

        # ---------- 拖动控制 ----------
        self.dragging = False
        self.drag_position = QPoint()

    def on_TitleImageVisibilityChanged(self, visible):
        """当全局变量改变时更新整个图片容器的可见性"""
        if hasattr(self, 'image_container'):
            self.image_container.setVisible(visible)

    def showInstallation(self):
        self.Home.hide()
        global_vars.set_show_image_container(True)
        self.Installation_page.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(QRect(0,0,self.width(),self.height()), scaled_pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() <= self.title_bar.height():
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def closeEvent(self, event):
        # 断开信号连接，避免内存泄漏
        try:
            global_signals.TitleImageVisibilityChanged.disconnect(self.on_TitleImageVisibilityChanged)
        except:
            pass
        super().closeEvent(event)


    def showDonotagreeErrorPage(self):
        self.showErrorPage("您不同意用户协议，安装程序将关闭。")

    def showErrorPage(self, ErrorMsg):
        self.Home.hide()
        self.Installation_page.hide()
        self.error_page = QuitPage(ErrorMsg)
        self.frame_layout.addWidget(self.error_page)
        self.error_page.show()