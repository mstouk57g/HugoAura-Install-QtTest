from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QTextEdit, QGraphicsOpacityEffect, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QColor, QPaintEvent, QFontMetrics, QFont
from typing import Optional

from widgets.hex_button import ImageTextButton
from widgets.ScrollColumn import ScrollColumn

class LCornerBorderWidget(QWidget):
    """
    L形四角边框控件
    """

    STYLE_ONE = 1  # 四角为背景色，其余部分透明
    STYLE_TWO = 2  # 四角为前景色，长边为背景色，宽边透明

    styleChanged = pyqtSignal(int)
    backgroundColorChanged = pyqtSignal(QColor)
    foregroundColorChanged = pyqtSignal(QColor)
    cornerLengthChanged = pyqtSignal(int)
    borderThicknessChanged = pyqtSignal(int)
    marginChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current_style = self.STYLE_ONE
        self._background_color = QColor(0, 120, 215)  # 默认蓝色
        self._foreground_color = QColor(255, 255, 255)  # 默认白色
        self._corner_length = -1  # -1表示使用默认计算方式
        self._border_thickness = 2  # 默认边框厚度
        self._margin = 10  # 默认内容边距
        self._content_widget = None

        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_StyledBackground, False)
        self._layout = QVBoxLayout(self)
        self._update_margins()

    def setContentWidget(self, widget: QWidget):
        """设置内容控件"""
        if self._content_widget:
            self._layout.removeWidget(self._content_widget)
            self._content_widget.setParent(None)

        self._content_widget = widget
        self._layout.addWidget(widget)

    def getContentWidget(self) -> Optional[QWidget]:
        """获取内容控件"""
        return self._content_widget

    def _update_margins(self):
        """更新边距，考虑边框厚度"""
        total_margin = self._margin + self._border_thickness
        self._layout.setContentsMargins(total_margin, total_margin,
                                       total_margin, total_margin)

    def paintEvent(self, event: QPaintEvent):
        """自定义绘制"""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 获取控件尺寸
        width = self.width()
        height = self.height()

        # 计算角长度
        corner_length = self._calculate_corner_length(width, height)
        thickness = self._border_thickness

        if self._current_style == self.STYLE_ONE:
            self._draw_style_one(painter, width, height, corner_length, thickness)
        else:
            self._draw_style_two(painter, width, height, corner_length, thickness)

    def _calculate_corner_length(self, width: int, height: int) -> int:
        """计算角长度"""
        if self._corner_length > 0:
            return self._corner_length

        # 使用短边的三分之一作为默认角长度
        short_side = min(width, height)
        return max(10, short_side // 3)  # 最小10像素

    def _draw_style_one(self, painter: QPainter, width: int, height: int, corner_length: int, thickness: int):
        """绘制样式一：四角为背景色，其余部分透明"""
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_color)

        # 绘制四个L形角

        # 左上角 - L形
        # 水平部分
        painter.drawRect(0, 0, corner_length, thickness)
        # 垂直部分
        painter.drawRect(0, 0, thickness, corner_length)

        # 右上角 - L形
        # 水平部分
        painter.drawRect(width - corner_length, 0, corner_length, thickness)
        # 垂直部分
        painter.drawRect(width - thickness, 0, thickness, corner_length)

        # 左下角 - L形
        # 水平部分
        painter.drawRect(0, height - thickness, corner_length, thickness)
        # 垂直部分
        painter.drawRect(0, height - corner_length, thickness, corner_length)

        # 右下角 - L形
        # 水平部分
        painter.drawRect(width - corner_length, height - thickness, corner_length, thickness)
        # 垂直部分
        painter.drawRect(width - thickness, height - corner_length, thickness, corner_length)

        # 样式一：其余部分完全透明，不绘制任何边框线

    def _draw_style_two(self, painter: QPainter, width: int, height: int, corner_length: int, thickness: int):
        """绘制样式二：四角为前景色，长边为背景色，宽边透明"""
        # 先绘制四个角的前景色
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._foreground_color)

        # 左上角 - L形
        painter.drawRect(0, 0, corner_length, thickness)
        painter.drawRect(0, 0, thickness, corner_length)

        # 右上角 - L形
        painter.drawRect(width - corner_length, 0, corner_length, thickness)
        painter.drawRect(width - thickness, 0, thickness, corner_length)

        # 左下角 - L形
        painter.drawRect(0, height - thickness, corner_length, thickness)
        painter.drawRect(0, height - corner_length, thickness, corner_length)

        # 右下角 - L形
        painter.drawRect(width - corner_length, height - thickness, corner_length, thickness)
        painter.drawRect(width - thickness, height - corner_length, thickness, corner_length)

        # 绘制长边的背景色（仅水平方向）
        painter.setBrush(self._background_color)

        # 上边长边（中间部分）
        painter.drawRect(corner_length, 0, width - 2 * corner_length, thickness)

        # 下边长边（中间部分）
        painter.drawRect(corner_length, height - thickness, width - 2 * corner_length, thickness)

        # 样式二：宽边（垂直方向）完全透明，不绘制任何内容

    def sizeHint(self):
        """建议大小"""
        from PyQt5.QtCore import QSize
        return QSize(300, 200)

    def minimumSizeHint(self):
        """最小大小"""
        from PyQt5.QtCore import QSize
        return QSize(150, 100)

    def setStyle(self, style: int):
        """设置样式"""
        if style not in (self.STYLE_ONE, self.STYLE_TWO):
            raise ValueError("样式必须是 STYLE_ONE(1) 或 STYLE_TWO(2)")

        if self._current_style != style:
            self._current_style = style
            self.update()
            self.styleChanged.emit(style)

    def getStyle(self) -> int:
        """获取当前样式"""
        return self._current_style

    def setBackgroundColor(self, color: QColor):
        """设置背景色"""
        if self._background_color != color:
            self._background_color = color
            self.update()
            self.backgroundColorChanged.emit(color)

    def getBackgroundColor(self) -> QColor:
        """获取背景色"""
        return self._background_color

    def setForegroundColor(self, color: QColor):
        """设置前景色"""
        if self._foreground_color != color:
            self._foreground_color = color
            self.update()
            self.foregroundColorChanged.emit(color)

    def getForegroundColor(self) -> QColor:
        """获取前景色"""
        return self._foreground_color

    def setCornerLength(self, length: int):
        """设置角长度（-1表示使用默认计算方式）"""
        if self._corner_length != length:
            self._corner_length = length
            self.update()
            self.cornerLengthChanged.emit(length)

    def getCornerLength(self) -> int:
        """获取角长度"""
        return self._corner_length

    def setBorderThickness(self, thickness: int):
        """设置边框厚度"""
        if self._border_thickness != thickness:
            self._border_thickness = max(1, thickness)  # 至少为1
            self._update_margins()
            self.update()
            self.borderThicknessChanged.emit(thickness)

    def getBorderThickness(self) -> int:
        """获取边框厚度"""
        return self._border_thickness

    def setMargin(self, margin: int):
        """设置内容边距"""
        if self._margin != margin:
            self._margin = margin
            self._update_margins()
            self.update()
            self.marginChanged.emit(margin)

    def getMargin(self) -> int:
        """获取内容边距"""
        return self._margin

    def toggleStyle(self):
        """切换样式"""
        new_style = self.STYLE_TWO if self._current_style == self.STYLE_ONE else self.STYLE_ONE
        self.setStyle(new_style)


class SelectableItemWidget(LCornerBorderWidget):
    """可选择的单个项目控件"""
    clicked = pyqtSignal(dict)  # 点击时发射对应的字典数据

    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.is_selected = False
        self.initUI()

    def initUI(self):
        """初始化UI - 完全按照你的样式"""
        # 设置默认样式为STYLE_ONE
        self.setStyle(LCornerBorderWidget.STYLE_ONE)
        self.setBackgroundColor(QColor(94, 181, 255))
        self.setForegroundColor(QColor(255, 255, 255))
        self.setBorderThickness(1)
        self.setCornerLength(30)
        self.setMargin(15)

        # 创建内部内容区域
        content_widget = self.createContentWidget()
        self.setContentWidget(content_widget)
        self.setFixedHeightByCalculation()
        self.createIncompatibleButton()

    def createContentWidget(self):
        """创建内部内容区域"""
        self.content_widget = QWidget()

        # 竖直布局
        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # 上下区域间距

        # 1. 上面的文本区域
        self.text_label = QLabel(self.item_data.get('name', '未知'))
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 设置文本样式
        font = self.text_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("color: white; font-family: Microsoft YaHei;")
        self.text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 2. 下面的按钮区域
        self.button_area = QWidget()
        self.button_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 透明度效果
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.6)
        self.button_area.setGraphicsEffect(opacity_effect)

        button_layout = QHBoxLayout(self.button_area)
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # 底部显示信息的按钮，使用item_data中的tag和size
        tag_text = self.item_data.get('tag', '')
        size_text = self.item_data.get('size', '')

        self.tag_button = ImageTextButton(tag_text, font_size=10, v_padding=8,
                                         canclick=False, h_padding=8, style=5)
        self.size_button = ImageTextButton(size_text, font_size=10, v_padding=8,
                                          canclick=False, h_padding=8, style=5)

        # 添加按钮到布局 - 左对齐
        button_layout.addWidget(self.tag_button)
        button_layout.addWidget(self.size_button)
        button_layout.addStretch()

        # 添加所有控件到主布局
        layout.addWidget(self.text_label)
        layout.addWidget(self.button_area)

        return self.content_widget

    def createIncompatibleButton(self):
        """创建右上角的不兼容按钮"""
        # 检查是否不兼容
        if self.item_data.get('unavailable', False):
            # 创建不兼容按钮
            self.incompatible_button = ImageTextButton(
                "不兼容",
                font_size=10,
                v_padding=5,
                h_padding=8,
                canclick=False,
                style=4
            )

            self.incompatible_button.setParent(self)
            self.incompatible_button.show()
            self.adjustIncompatibleButtonPosition()
        else:
            self.incompatible_button = None

    def adjustIncompatibleButtonPosition(self):
        """调整不兼容按钮位置到右上角"""
        if self.incompatible_button and self.incompatible_button.isVisible():
            # 获取按钮的实际大小
            button_width = self.incompatible_button.width()
            button_height = self.incompatible_button.height()

            # 从右边减去按钮宽度，顶部对齐
            # 15像素边距
            margin = 15

            # 计算新位置
            new_x = self.width() - button_width - margin
            new_y = margin
            self.incompatible_button.move(new_x, new_y)
            self.incompatible_button.raise_()

    def setFixedHeightByCalculation(self):
        """计算并设置固定高度"""
        # 1. 计算文本高度
        text_font = QFont()
        text_font.setPointSize(18)
        text_font.setBold(True)
        fm = QFontMetrics(text_font)
        text_height = fm.height() + 10  # 字体高度 + 一些padding

        # 2. 计算按钮高度
        button_font = QFont()
        button_font.setPointSize(10)
        fm_button = QFontMetrics(button_font)
        button_text_height = fm_button.height()
        button_area_height = button_text_height + 10  # 10px上下padding

        # 3. 计算总高度
        content_spacing = 10  # 上下区域间距
        border_margin = 15  # 边框内边距
        border_thickness = 1  # 边框厚度

        # 总高度 = 上边框厚度 + 上内边距 + 文本高度 + 间距 + 按钮区域高度 + 下内边距 + 下边框厚度
        total_height = (border_thickness * 2) + (border_margin * 2) + text_height + content_spacing + button_area_height

        self.setFixedHeight(total_height)

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.item_data)
        super().mousePressEvent(event)

    def setSelected(self, selected):
        """设置选中状态"""
        self.is_selected = selected
        if selected:
            self.setStyle(LCornerBorderWidget.STYLE_TWO)
        else:
            self.setStyle(LCornerBorderWidget.STYLE_ONE)
        self.update()

    def updateItem(self, item_data):
        """更新项目数据"""
        self.item_data = item_data

        # 更新文本和按钮
        self.text_label.setText(item_data.get('name', '未知'))
        self.tag_button.setText(item_data.get('tag', ''))
        self.size_button.setText(item_data.get('size', ''))

        # 移除旧的不兼容按钮
        if self.incompatible_button:
            self.incompatible_button.deleteLater()
            self.incompatible_button = None

        # 重新创建不兼容按钮
        self.createIncompatibleButton()

        self.update()

    def resizeEvent(self, event):
        """重写resizeEvent来调整不兼容按钮位置"""
        super().resizeEvent(event)

        # 窗口大小变化时重新调整按钮位置
        self.adjustIncompatibleButtonPosition()

    def showEvent(self, event):
        """显示事件"""
        super().showEvent(event)

        # 显示时调整按钮位置
        QTimer.singleShot(10, self.adjustIncompatibleButtonPosition)

class SelectableListWidget(QWidget):
    """可选择列表控件"""
    selectionChanged = pyqtSignal(dict)  # 选择改变时发射

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []  # 原始数据
        self.item_widgets = []  # 项目控件
        self.selected_item = None  # 当前选中的项目数据
        self.selected_widget = None  # 当前选中的控件

        self.initUI()

    def initUI(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建内容容器
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        # 创建内容容器
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(20)  # 项目之间的间距
        self.content_layout.setAlignment(Qt.AlignTop)

        # 设置滚动区域的内容
        self.scroll_area.setWidget(self.content_widget)

        # 创建自定义滚动列
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

        # 连接滚动信号
        self.scroll_controller.verticalScrollBar().valueChanged.connect(
            self.on_scroll_changed
        )
        self.scroll_area.verticalScrollBar().valueChanged.connect(
            self.on_scrollarea_changed
        )

        # 将滚动区域和滚动条添加到容器
        container_layout.addWidget(self.scroll_area, 1)
        container_layout.addWidget(self.scroll_column, 0)

        main_layout.addWidget(container)

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
        self.update_scroll_range()

    def setItems(self, items):
        """设置项目列表"""
        # 清空现有项目
        self.clearItems()
        self.items = items

        # 创建项目控件
        for item_data in items:
            item_widget = SelectableItemWidget(item_data)
            item_widget.clicked.connect(self.onItemClicked)
            self.item_widgets.append(item_widget)
            self.content_layout.addWidget(item_widget)

        # 更新滚动范围
        self.update_scroll_range()

    def clearItems(self):
        """清空所有项目"""
        for widget in self.item_widgets:
            self.content_layout.removeWidget(widget)
            widget.deleteLater()
        self.item_widgets.clear()
        self.selected_item = None
        self.selected_widget = None

    def update_scroll_range(self):
        """更新滚动范围"""
        content_height = self.content_widget.sizeHint().height()
        visible_height = self.scroll_area.height()

        if content_height > visible_height:
            max_value = content_height - visible_height
            self.scroll_area.verticalScrollBar().setRange(0, max_value)
            self.scroll_controller.verticalScrollBar().setRange(0, max_value)
        else:
            self.scroll_area.verticalScrollBar().setRange(0, 0)
            self.scroll_controller.verticalScrollBar().setRange(0, 0)

    def onItemClicked(self, item_data):
        """项目被点击时的处理"""
        # 找到对应的控件
        clicked_widget = None
        for widget in self.item_widgets:
            if widget.item_data == item_data:
                clicked_widget = widget
                break

        if clicked_widget and clicked_widget != self.selected_widget:
            # 取消之前的选择
            if self.selected_widget:
                self.selected_widget.setSelected(False)

            # 设置新的选择
            clicked_widget.setSelected(True)
            self.selected_item = item_data
            self.selected_widget = clicked_widget

            self.selectionChanged.emit(item_data)

    def getSelectedItem(self):
        """获取当前选中的项目"""
        return self.selected_item

    def setSelectedItem(self, item_data):
        """设置选中的项目"""
        if item_data is None:
            # 清除选择
            if self.selected_widget:
                self.selected_widget.setSelected(False)
                self.selected_item = None
                self.selected_widget = None
            return

        # 查找对应的控件
        target_widget = None
        for widget in self.item_widgets:
            if widget.item_data == item_data:
                target_widget = widget
                break

        if target_widget and target_widget != self.selected_widget:
            # 取消之前的选择
            if self.selected_widget:
                self.selected_widget.setSelected(False)

            # 设置新的选择
            target_widget.setSelected(True)
            self.selected_item = item_data
            self.selected_widget = target_widget

            # 滚动到选中的项目
            self.scrollToItem(target_widget)

    def scrollToItem(self, item_widget):
        """滚动到指定项目"""
        # 计算项目的位置
        y_pos = item_widget.pos().y()
        widget_height = item_widget.height()
        area_height = self.scroll_area.height()

        # 计算滚动位置
        current_value = self.scroll_area.verticalScrollBar().value()

        if y_pos < current_value:
            # 项目在上方，滚动到顶部
            self.scroll_area.verticalScrollBar().setValue(y_pos)
        elif y_pos + widget_height > current_value + area_height:
            # 项目在下方，滚动到底部
            self.scroll_area.verticalScrollBar().setValue(
                y_pos + widget_height - area_height
            )

    def updateItem(self, old_item, new_item):
        """更新项目数据"""
        for widget in self.item_widgets:
            if widget.item_data == old_item:
                widget.updateItem(new_item)
                # 如果是选中的项目，更新选中数据
                if widget == self.selected_widget:
                    self.selected_item = new_item
                break