from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from widgets.ItemListWithLogo import ItemListWithLogo
from widgets.ScrollColumn import ScrollColumn
from widgets.hex_button import HexButton
from utils.signals import global_signals

class VersionsView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel()
        title_label.setAlignment(Qt.AlignHCenter)
        title_label.setText("请选择组件及安装的版本")
        title_label.setStyleSheet("color: rgba(255, 255, 255, 1);")
        title_label.setFont(QFont("Microsoft YaHei", 17))
        main_layout.addWidget(title_label)

        list_container = QWidget()
        list_container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0);
                border-radius: 0px;
            }
        """)

        container_layout = QHBoxLayout(list_container)
        container_layout.setContentsMargins(15, 15, 5, 15)
        container_layout.setSpacing(0)

        # 创建可滚动的区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        # 创建滚动内容容器
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")

        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)  # 列表项间距

        HugoAura_Main_Version_ItemListWithLogo = ItemListWithLogo()
        HugoAura_Main_Version_ItemListWithLogo.set_icon("resources/aura.png")
        HugoAura_Main_Version_ItemListWithLogo.set_title("HugoAura-Main")
        HugoAura_Main_Version_ItemListWithLogo.title_label.setStyleSheet("color: #FFFFFF; font-family: Microsoft YaHei;")
        HugoAura_Main_Version_ItemListWithLogo.set_horizontal_expand(True)

        # 在中间区域添加说明文字
        #middle_label = QLabel("中间区域：这是操作说明")
        #middle_label.setWordWrap(True)
        #middle_label.setStyleSheet("color: #666; font-size: 12px;")
        #item2.set_left_widget(middle_label)
        HugoAura_Main_Version_ItemListWithLogo.set_square_color(QColor(255,255,255,int(0.2 * 255)))

        HugoAura_Main_Version_ItemListWithLogo_bottom_label = QLabel("Haven't selected, click to select...")
        HugoAura_Main_Version_ItemListWithLogo_bottom_label.setWordWrap(True)
        HugoAura_Main_Version_ItemListWithLogo_bottom_label.setStyleSheet("color: #ffffff; font-size: 15px; font-family: Microsoft YaHei;")
        HugoAura_Main_Version_ItemListWithLogo.set_right_widget(HugoAura_Main_Version_ItemListWithLogo_bottom_label)

        HugoAura_Main_Version_ItemListWithLogo.set_top_middle_spacing(8)
        HugoAura_Main_Version_ItemListWithLogo.set_middle_bottom_spacing(8)
        HugoAura_Main_Version_ItemListWithLogo.set_left_right_spacing(15)
        HugoAura_Main_Version_ItemListWithLogo.set_margins(10, 10, 10, 10)

        HugoAura_Main_Version_ItemListWithLogo.clicked.connect(lambda: global_signals.showVersionSelectorMainPage.emit())
        content_layout.addWidget(HugoAura_Main_Version_ItemListWithLogo)

        HugoAura_Aikari_Version_ItemListWithLogo = ItemListWithLogo()
        HugoAura_Aikari_Version_ItemListWithLogo.set_icon("resources/Aikari.png")
        HugoAura_Aikari_Version_ItemListWithLogo.set_title("HugoAura-Aikari")
        HugoAura_Aikari_Version_ItemListWithLogo.title_label.setStyleSheet("color: #FFFFFF; font-family: Microsoft YaHei;")
        HugoAura_Aikari_Version_ItemListWithLogo.set_horizontal_expand(True)

        # 在中间区域添加说明文字
        #middle_label = QLabel("中间区域：这是操作说明")
        #middle_label.setWordWrap(True)
        #middle_label.setStyleSheet("color: #666; font-size: 12px;")
        #item2.set_left_widget(middle_label)
        HugoAura_Aikari_Version_ItemListWithLogo.set_square_color(QColor(53,53,53,255))

        HugoAura_Aikari_Version_ItemListWithLogo_bottom_label = QLabel("Haven't selected, click to select...")
        HugoAura_Aikari_Version_ItemListWithLogo_bottom_label.setWordWrap(True)
        HugoAura_Aikari_Version_ItemListWithLogo_bottom_label.setStyleSheet("color: #ffffff; font-size: 15px; font-family: Microsoft YaHei;")
        HugoAura_Aikari_Version_ItemListWithLogo.set_right_widget(HugoAura_Aikari_Version_ItemListWithLogo_bottom_label)

        HugoAura_Aikari_Version_ItemListWithLogo.set_top_middle_spacing(8)
        HugoAura_Aikari_Version_ItemListWithLogo.set_middle_bottom_spacing(8)
        HugoAura_Aikari_Version_ItemListWithLogo.set_left_right_spacing(15)

        HugoAura_Aikari_Version_ItemListWithLogo.set_margins(10, 10, 10, 10)

        HugoAura_Aikari_Version_ItemListWithLogo.clicked.connect(lambda: global_signals.showVersionSelectorAikariPage.emit())
        content_layout.addWidget(HugoAura_Aikari_Version_ItemListWithLogo)

        content_layout.addStretch(1)
        scroll_area.setWidget(scroll_content)

        self.scroll_column = ScrollColumn(
            up_image="resources/next_white.png",
            down_image="resources/next_white.png",
            scrollbar_bg="rgba(255,255,255,20)",
            scrollbar_handle="rgba(255,255,255,255)"
        )

        # 创建一个隐藏的QTextEdit来绑定ScrollColumn
        self.scroll_controller = QTextEdit()
        self.scroll_controller.setVisible(False)
        self.scroll_column.bind_text_edit(self.scroll_controller)

        self.scroll_controller.verticalScrollBar().valueChanged.connect(
            self.on_scroll_changed
        )
        scroll_area.verticalScrollBar().valueChanged.connect(
            self.on_scrollarea_changed
        )

        container_layout.addWidget(scroll_area, 1)
        container_layout.addWidget(self.scroll_column, 0)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignHCenter)
        button_layout.setSpacing(40)  # 按钮之间间距

        self.back_btn = HexButton("    返回    ", icon_path="resources/CHA.png", font_size=10, style=2)
        self.back_btn.setFont(QFont("Microsoft YaHei", 10))
        self.next_btn = HexButton("   下一步   ", font_size=10, style=1, icon_path="resources/Next.png")
        self.next_btn.setFont(QFont("Microsoft Yahei", 12))
        self.back_btn.clicked = lambda: global_signals.showTagSourcePage.emit()

        main_layout.addWidget(list_container, 1)
        button_layout.addWidget(self.back_btn)
        button_layout.addWidget(self.next_btn)
        main_layout.addLayout(button_layout, 0)

        self.scroll_area = scroll_area
        self.scroll_content = scroll_content

    def on_scroll_changed(self, value):
        """当ScrollColumn滚动时，更新QScrollArea的位置"""
        # 解除信号循环
        self.scroll_area.verticalScrollBar().valueChanged.disconnect(
            self.on_scrollarea_changed
        )

        # 计算比例并设置QScrollArea的位置
        max_scrollbar = self.scroll_controller.verticalScrollBar().maximum()
        if max_scrollbar > 0:
            ratio = value / max_scrollbar
            scrollarea_max = self.scroll_area.verticalScrollBar().maximum()
            self.scroll_area.verticalScrollBar().setValue(int(ratio * scrollarea_max))

        # 重新连接信号
        self.scroll_area.verticalScrollBar().valueChanged.connect(
            self.on_scrollarea_changed
        )

    def on_scrollarea_changed(self, value):
        """当QScrollArea滚动时，更新ScrollColumn的位置"""
        # 解除信号循环
        self.scroll_controller.verticalScrollBar().valueChanged.disconnect(
            self.on_scroll_changed
        )

        # 计算比例并设置ScrollColumn的位置
        max_scrollarea = self.scroll_area.verticalScrollBar().maximum()
        if max_scrollarea > 0:
            ratio = value / max_scrollarea
            scrollbar_max = self.scroll_controller.verticalScrollBar().maximum()
            self.scroll_controller.verticalScrollBar().setValue(int(ratio * scrollbar_max))

        # 重新连接信号
        self.scroll_controller.verticalScrollBar().valueChanged.connect(
            self.on_scroll_changed
        )

    def resizeEvent(self, event):
        """窗口大小变化时更新滚动范围"""
        super().resizeEvent(event)
        # 更新滚动范围
        content_height = self.scroll_content.sizeHint().height()
        visible_height = self.scroll_area.height()

        if content_height > visible_height:
            max_value = content_height - visible_height
            self.scroll_area.verticalScrollBar().setRange(0, max_value)
            self.scroll_controller.verticalScrollBar().setRange(0, max_value)
        else:
            self.scroll_area.verticalScrollBar().setRange(0, 0)
            self.scroll_controller.verticalScrollBar().setRange(0, 0)

