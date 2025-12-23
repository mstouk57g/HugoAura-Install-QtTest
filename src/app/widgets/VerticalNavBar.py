from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPainter, QFontMetrics

class VerticalNavBar(QWidget):
    """

    这是选择版本时不同版本类型的纵向导航

    """
    itemClicked = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_items = []  # 存储导航项文本
        self.nav_widgets = []  # 存储导航项容器widget
        self.nav_labels = []  # 存储导航项QLabel
        self.current_index = -1  # 当前选中索引
        self.font_size = 12  # 字体大小
        self.text_color = QColor(255, 255, 255)  # 文字颜色
        self.line_width = 3  # 竖线宽度
        self.line_spacing = 10  # 竖线与导航的间距
        self.padding = 20  # 左右内边距
        self.height_scale = 1.5  # 高度缩放系数（字体高度的倍数）
        self.normal_opacity = 0.7  # 未选中时的透明度
        self.selected_opacity = 1.0  # 选中时的透明度

        self.initUI()

    def initUI(self):
        """初始化UI"""
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent;")

        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 5, 0, 5)
        self.main_layout.setAlignment(Qt.AlignTop)

    def calculateTextSize(self):
        """计算文字尺寸"""
        font = QFont("Microsoft YaHei", self.font_size)
        font_metrics = QFontMetrics(font)

        # 计算文字高度（包括上行和下行）
        text_height = font_metrics.height()

        # 计算最大文字宽度
        max_width = 0
        for item_text in self.nav_items:
            text_width = font_metrics.horizontalAdvance(item_text)
            if text_width > max_width:
                max_width = text_width

        return text_height, max_width

    def calculateItemHeight(self):
        """根据字体大小计算导航项高度"""
        text_height, _ = self.calculateTextSize()
        return int(text_height * self.height_scale)

    def calculateNavWidth(self):
        """计算导航栏宽度"""
        _, max_text_width = self.calculateTextSize()
        return max_text_width + self.padding * 2 + self.line_width + self.line_spacing

    def setItems(self, items):
        """设置导航项"""
        self.clearItems()

        self.nav_items = items
        if not items:
            return

        # 计算并设置导航栏尺寸
        item_height = self.calculateItemHeight()
        nav_width = self.calculateNavWidth()

        self.setFixedWidth(nav_width)

        for i, item_text in enumerate(items):
            main_widget = QWidget()
            main_widget.setFixedHeight(item_height)
            main_widget.setFixedWidth(nav_width)
            main_layout = QHBoxLayout(main_widget)
            main_layout.setContentsMargins(self.padding, 0, self.line_spacing + self.padding, 0)
            main_layout.setSpacing(0)
            main_layout.addStretch()

            label = QLabel(item_text)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label.setFixedHeight(item_height)

            font = QFont("Microsoft YaHei", self.font_size)
            label.setFont(font)
            main_layout.addWidget(label)

            main_widget.setStyleSheet("background: transparent;")

            # 点击事件
            main_widget.mousePressEvent = lambda event, idx=i: self.onItemClicked(idx)
            label.mousePressEvent = lambda event, idx=i: self.onItemClicked(idx)

            self.nav_widgets.append(main_widget)
            self.nav_labels.append(label)
            self.main_layout.addWidget(main_widget)

        # 默认选中第一项
        self.setCurrentIndex(0)

    def updateLabelOpacity(self, index, is_selected):
        """更新标签透明度"""
        if index < 0 or index >= len(self.nav_labels):
            return

        label = self.nav_labels[index]
        opacity = self.selected_opacity if is_selected else self.normal_opacity

        label.setStyleSheet(f"""
            QLabel {{
                color: rgba({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()}, {int(self.text_color.alpha() * opacity)});
                background: transparent;
                padding: 0px;
                margin: 0px;
            }}
        """)

    def setCurrentIndex(self, index):
        """设置当前选中项"""
        if index < 0 or index >= len(self.nav_widgets) or index == self.current_index:
            return

        if self.current_index != -1:
            self.updateLabelOpacity(self.current_index, False)

        self.current_index = index
        self.updateLabelOpacity(index, True)
        self.update()
        self.itemClicked.emit(index, self.nav_items[index]) # 发出选中信号

    def paintEvent(self, event):
        """重写绘制竖线paintEvent"""
        super().paintEvent(event)

        if self.current_index >= 0 and self.current_index < len(self.nav_widgets):
            nav_widget = self.nav_widgets[self.current_index]

            nav_pos = nav_widget.pos()
            nav_height = nav_widget.height()

            line_x = self.width() - self.line_width
            line_y = nav_pos.y()
            line_height = nav_height

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.text_color))
            painter.drawRect(line_x, line_y, self.line_width, line_height)

    def onItemClicked(self, index):
        """项点击事件"""
        self.setCurrentIndex(index)

    def setFontSize(self, size):
        """设置字体大小"""
        self.font_size = size

        if self.nav_items:
            item_height = self.calculateItemHeight()
            nav_width = self.calculateNavWidth()

            self.setFixedWidth(nav_width)

            font = QFont("Microsoft YaHei", self.font_size)
            for i, label in enumerate(self.nav_labels):
                label.setFont(font)
                label.setFixedHeight(item_height)

            for widget in self.nav_widgets:
                widget.setFixedHeight(item_height)
                widget.setFixedWidth(nav_width)

            for i in range(len(self.nav_labels)):
                self.updateLabelOpacity(i, i == self.current_index)

            self.update()

    def setHeightScale(self, scale):
        """设置高度缩放系数"""
        self.height_scale = scale

        if self.nav_items:
            item_height = self.calculateItemHeight()

            for label in self.nav_labels:
                label.setFixedHeight(item_height)

            for widget in self.nav_widgets:
                widget.setFixedHeight(item_height)

            self.update()

    def setTextColor(self, color):
        """设置文字和竖线颜色"""
        if isinstance(color, tuple) and len(color) == 3:
            self.text_color = QColor(color[0], color[1], color[2])
        elif isinstance(color, QColor):
            self.text_color = color
        else:
            self.text_color = QColor(255, 255, 255)  # 默认

        # 更新所有文字颜色和透明度
        for i in range(len(self.nav_labels)):
            self.updateLabelOpacity(i, i == self.current_index)

        self.update()

    def setNormalOpacity(self, opacity):
        """设置未选中时的透明度（0.0 - 1.0）"""
        self.normal_opacity = max(0.0, min(1.0, opacity))

        # 更新所有未选中项的透明度
        if self.nav_items:
            for i in range(len(self.nav_labels)):
                if i != self.current_index:
                    self.updateLabelOpacity(i, False)

    def setSelectedOpacity(self, opacity):
        """设置选中时的透明度（0.0 - 1.0）"""
        self.selected_opacity = max(0.0, min(1.0, opacity))

        # 更新当前选中项的透明度
        if self.current_index != -1:
            self.updateLabelOpacity(self.current_index, True)

    def setLineWidth(self, width):
        """设置竖线宽度"""
        self.line_width = width
        # 重新计算宽度并更新布局
        if self.nav_items:
            nav_width = self.calculateNavWidth()
            self.setFixedWidth(nav_width)
            for widget in self.nav_widgets:
                widget.setFixedWidth(nav_width)
        self.update()

    def setLineSpacing(self, spacing):
        """设置竖线与导航的间距"""
        self.line_spacing = spacing
        # 更新所有导航项的右边距
        for widget in self.nav_widgets:
            layout = widget.layout()
            if layout:
                layout.setContentsMargins(self.padding, 0, spacing + self.padding, 0)

        if self.nav_items:
            nav_width = self.calculateNavWidth()
            self.setFixedWidth(nav_width)
            for widget in self.nav_widgets:
                widget.setFixedWidth(nav_width)
        self.update()

    def setPadding(self, padding):
        """设置内边距"""
        self.padding = padding
        # 更新所有导航项的边距
        for widget in self.nav_widgets:
            layout = widget.layout()
            if layout:
                layout.setContentsMargins(padding, 0, self.line_spacing + padding, 0)

        if self.nav_items:
            nav_width = self.calculateNavWidth()
            self.setFixedWidth(nav_width)
            for widget in self.nav_widgets:
                widget.setFixedWidth(nav_width)
        self.update()

    def clearItems(self):
        """清空所有导航项"""
        for widget in self.nav_widgets:
            self.main_layout.removeWidget(widget)
            widget.deleteLater()

        self.nav_items.clear()
        self.nav_widgets.clear()
        self.nav_labels.clear()
        self.current_index = -1

        # 清空后重置宽度
        self.setFixedWidth(0)

    def currentIndex(self):
        """获取当前选中索引"""
        return self.current_index

    def currentText(self):
        """获取当前选中文本"""
        if self.current_index >= 0 and self.current_index < len(self.nav_items):
            return self.nav_items[self.current_index]
        return ""