from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import typing

class ItemListWithLogo(QWidget):
    """自定义按钮控件，包含左侧图标和右侧文本/自定义区域。选择Aikari/Main那块的"""

    # 定义信号
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # 属性设置
        self._icon = None  # 图标
        self._icon_padding_ratio = 0.7  # 图标占正方形宽度的比例
        self._icon_square_size = 80  # 左侧正方形大小
        self._title = "标题"  # 标题文本
        self._title_font_size = 14  # 标题字体大小
        self._title_font_weight = QFont.Normal  # 标题字体粗细
        self._show_middle_area = True  # 是否显示中间区域
        self._left_widget = None  # 中间自定义部件
        self._right_widget = None  # 底部自定义部件
        self._left_layout = None  # 中间自定义布局
        self._right_layout = None  # 底部自定义布局
        self._horizontal_expand = False  # 是否横向扩展

        # 状态属性
        self._enabled = True  # 是否启用点击
        self._hovered = False  # 鼠标是否悬停
        self._pressed = False  # 是否按下

        # 间距设置
        self._left_margin = 15  # 左侧间距
        self._right_margin = 15  # 右侧间距
        self._top_margin = 10  # 顶部间距
        self._bottom_margin = 10  # 底部间距
        self._left_right_spacing = 10  # 左右两部分间距
        self._top_middle_spacing = 5   # 标题与中间区域间距
        self._middle_bottom_spacing = 5  # 中间与底部区域间距

        # 颜色设置
        self._square_color = QColor(200, 200, 200, 128)  # 半透明正方形颜色
        self._hover_opacity = 0.8  # 悬停时透明度
        self._normal_opacity = 1.0  # 正常时透明度
        self._pressed_opacity = 0.7  # 按下时透明度
        self._disabled_opacity = 0.5  # 禁用时透明度

        self.setMouseTracking(True)

        self.init_ui()

    def init_ui(self):
        """初始化UI布局"""
        # 主布局 - 使用水平布局，让左右两部分对齐
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(
            self._left_margin,
            self._top_margin,
            self._right_margin,
            self._bottom_margin
        )
        main_layout.setSpacing(self._left_right_spacing)

        # 左侧图标容器
        self.left_container = QWidget()
        self.left_container.setFixedWidth(self._icon_square_size)
        self.left_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # 右侧主容器 - 这个容器将包含右侧的所有内容
        self.right_main_container = QWidget()
        self.right_main_container.setSizePolicy(
            QSizePolicy.Expanding if self._horizontal_expand else QSizePolicy.Fixed,
            QSizePolicy.Expanding  # 改为Expanding，让容器可以扩展
        )

        # 右侧垂直布局 - 这个布局包含右侧的所有内容
        self.right_main_layout = QVBoxLayout(self.right_main_container)
        self.right_main_layout.setContentsMargins(0, 0, 0, 0)
        self.right_main_layout.setSpacing(0)

        # 创建一个包装容器，让右侧内容在垂直方向上居中
        self.right_content_wrapper = QWidget()
        self.right_content_wrapper.setSizePolicy(
            QSizePolicy.Expanding if self._horizontal_expand else QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        # 右侧内容布局 - 这个布局包含实际的内容（标题、中间、底部）
        self.right_content_layout = QVBoxLayout(self.right_content_wrapper)
        self.right_content_layout.setContentsMargins(0, 0, 0, 0)
        self.right_content_layout.setSpacing(0)

        # 标题标签
        self.title_label = QLabel(self._title)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setWordWrap(False)
        self.update_title_font()

        # 中间自定义区域容器
        self.middle_container = QWidget()
        self.middle_layout = QVBoxLayout(self.middle_container)
        self.middle_layout.setContentsMargins(0, 0, 0, 0)

        # 底部自定义区域容器
        self.bottom_container = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom_container)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        # 构建右侧内容
        self.build_right_content()

        # 将内容包装器添加到主布局中，并垂直居中
        self.right_main_layout.addWidget(self.right_content_wrapper)
        self.right_main_layout.setAlignment(Qt.AlignVCenter)

        # 添加到主布局
        main_layout.addWidget(self.left_container)
        main_layout.addWidget(self.right_main_container)
        self.update_size_policy()
        self.update_minimum_height()

    def update_minimum_height(self):
        """更新最小高度（基于右侧内容）"""
        # 计算右侧内容的最小高度
        min_height = self.title_label.minimumSizeHint().height()

        if self._show_middle_area:
            if self.middle_container.layout().count() > 0:
                min_height += self._top_middle_spacing
                min_height += self.middle_container.minimumSizeHint().height()
            min_height += self._middle_bottom_spacing
            if self.bottom_container.layout().count() > 0:
                min_height += self.bottom_container.minimumSizeHint().height()
        else:
            min_height += self._top_middle_spacing
            if self.bottom_container.layout().count() > 0:
                min_height += self.bottom_container.minimumSizeHint().height()

        # 加上上下边距
        min_height += self._top_margin + self._bottom_margin

        # 设置最小高度（不小于正方形高度）
        min_height = max(min_height, self._icon_square_size + self._top_margin + self._bottom_margin)
        self.setMinimumHeight(min_height)

    def update_size_policy(self):
        """更新控件的尺寸策略"""
        if self._horizontal_expand:
            # 横向扩展，纵向固定
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.right_main_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.right_content_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            # 横向固定，纵向固定
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.right_main_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.right_content_wrapper.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 更新子控件的尺寸
        self.update_child_widgets_size_policy()

    def update_child_widgets_size_policy(self):
        """更新子控件的尺寸策略"""
        # 更新中间区域的子控件
        if self._left_widget:
            if self._horizontal_expand:
                self._left_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            else:
                self._left_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 更新底部区域的子控件
        if self._right_widget:
            if self._horizontal_expand:
                self._right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            else:
                self._right_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 更新布局中的控件
        for layout in [self.middle_layout, self.bottom_layout]:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget():
                    if self._horizontal_expand:
                        item.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                    else:
                        item.widget().setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def build_right_content(self):
        """构建右侧内容（标题、中间、底部）"""
        # 清空右侧内容布局
        while self.right_content_layout.count():
            item = self.right_content_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # 添加标题
        self.right_content_layout.addWidget(self.title_label)

        # 根据中间区域显示状态添加部件
        if self._show_middle_area:
            self.right_content_layout.addSpacing(self._top_middle_spacing)
            self.right_content_layout.addWidget(self.middle_container)
            self.right_content_layout.addSpacing(self._middle_bottom_spacing)
            self.right_content_layout.addWidget(self.bottom_container)
        else:
            # 如果不显示中间区域，直接添加底部区域
            self.right_content_layout.addSpacing(self._top_middle_spacing)
            self.right_content_layout.addWidget(self.bottom_container)

        self.update_minimum_height()

    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 根据状态设置透明度
        if not self._enabled:
            painter.setOpacity(self._disabled_opacity)
        elif self._pressed:
            painter.setOpacity(self._pressed_opacity)
        elif self._hovered:
            painter.setOpacity(self._hover_opacity)
        else:
            painter.setOpacity(self._normal_opacity)

        # 绘制左侧正方形和图标
        self.draw_left_square_and_icon(painter)

    def draw_left_square_and_icon(self, painter):
        """绘制左侧正方形和图标"""
        # 获取左侧容器的几何信息
        left_rect = self.left_container.geometry()

        # 计算正方形大小（不超过预设大小，且不超过可用高度）
        available_height = left_rect.height()
        square_size = min(self._icon_square_size, available_height)

        # 计算正方形位置（在左侧容器中垂直居中）
        square_x = left_rect.x() + (left_rect.width() - square_size) // 2
        square_y = left_rect.y() + (left_rect.height() - square_size) // 2

        square_rect = QRect(
            square_x,
            square_y,
            square_size,
            square_size
        )

        # 绘制半透明正方形
        painter.setBrush(self._square_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(square_rect)

        # 如果有图标，绘制图标
        if self._icon and not self._icon.isNull():
            # 计算图标大小（正方形宽度的70%）
            icon_size = int(square_size * self._icon_padding_ratio)

            # 计算图标位置（居中于正方形）
            icon_x = square_rect.center().x() - icon_size // 2
            icon_y = square_rect.center().y() - icon_size // 2

            # 绘制图标
            painter.drawPixmap(
                icon_x, icon_y, icon_size, icon_size,
                self._icon.pixmap(icon_size, icon_size)
            )

    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        self.update()

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton and self._enabled:
            self._pressed = True
            self.update()
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton and self._enabled and self._pressed:
            self._pressed = False
            # 检查鼠标是否仍在控件内
            if self.rect().contains(event.pos()):
                self.clicked.emit()
            self.update()
            event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self._enabled:
            was_hovered = self._hovered
            self._hovered = True

            if was_hovered != self._hovered:
                self.update()

        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件"""
        if self._enabled:
            self._hovered = False
            self._pressed = False
            self.update()

        super().leaveEvent(event)

    def update_title_font(self):
        """更新标题字体"""
        font = QFont()
        font.setPointSize(self._title_font_size)
        font.setWeight(self._title_font_weight)
        self.title_label.setFont(font)

    # ============ 属性设置方法 ============

    def set_icon(self, icon: typing.Union[QIcon, str]):
        """设置图标"""
        if isinstance(icon, str):
            self._icon = QIcon(icon)
        else:
            self._icon = icon
        self.update()

    def set_icon_padding_ratio(self, ratio: float):
        """设置图标占正方形宽度的比例"""
        if 0.1 <= ratio <= 0.9:
            self._icon_padding_ratio = ratio
            self.update()

    def set_icon_square_size(self, size: int):
        """设置左侧正方形大小（最大尺寸）"""
        self._icon_square_size = size
        self.left_container.setFixedWidth(size)
        self.update_minimum_height()
        self.update()

    def set_title(self, title: str):
        """设置标题文本"""
        self._title = title
        self.title_label.setText(title)
        self.update_minimum_height()

    def set_title_font_size(self, size: int):
        """设置标题字体大小"""
        self._title_font_size = size
        self.update_title_font()
        self.update_minimum_height()

    def set_title_font_weight(self, weight: int):
        """设置标题字体粗细"""
        self._title_font_weight = weight
        self.update_title_font()

    def set_show_middle_area(self, show: bool):
        """设置是否显示中间区域"""
        self._show_middle_area = show
        self.build_right_content()

    def set_horizontal_expand(self, expand: bool):
        """设置是否横向扩展"""
        self._horizontal_expand = expand
        self.update_size_policy()
        self.build_right_content()

    def set_left_widget(self, widget: QWidget):
        """设置中间自定义部件"""
        # 清除原有部件
        while self.middle_layout.count():
            item = self.middle_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if widget:
            self.middle_layout.addWidget(widget)
            self._left_widget = widget
            self.update_child_widgets_size_policy()
            self.update_minimum_height()

    def set_left_layout(self, layout: QLayout):
        """设置中间自定义布局"""
        # 清除原有布局
        while self.middle_layout.count():
            item = self.middle_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if layout:
            self.middle_container.setLayout(layout)
            self._left_layout = layout
            self.update_size_policy()
            self.update_minimum_height()

    def set_right_widget(self, widget: QWidget):
        """设置底部自定义部件"""
        # 清除原有部件
        while self.bottom_layout.count():
            item = self.bottom_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if widget:
            self.bottom_layout.addWidget(widget)
            self._right_widget = widget
            self.update_child_widgets_size_policy()
            self.update_minimum_height()

    def set_right_layout(self, layout: QLayout):
        """设置底部自定义布局"""
        # 清除原有布局
        while self.bottom_layout.count():
            item = self.bottom_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if layout:
            self.bottom_container.setLayout(layout)
            self._right_layout = layout
            self.update_size_policy()
            self.update_minimum_height()

    # ============ 间距设置方法 ============

    def set_margins(self, left: int, right: int, top: int, bottom: int):
        """设置边距"""
        self._left_margin = left
        self._right_margin = right
        self._top_margin = top
        self._bottom_margin = bottom

        if self.layout():
            self.layout().setContentsMargins(left, top, right, bottom)

        self.update_minimum_height()

    def set_left_right_spacing(self, spacing: int):
        """设置左右两部分间距"""
        self._left_right_spacing = spacing
        if self.layout():
            self.layout().setSpacing(spacing)

    def set_top_middle_spacing(self, spacing: int):
        """设置标题与中间区域间距"""
        self._top_middle_spacing = spacing
        self.build_right_content()

    def set_middle_bottom_spacing(self, spacing: int):
        """设置中间与底部区域间距"""
        self._middle_bottom_spacing = spacing
        if self._show_middle_area:
            self.build_right_content()

    # ============ 外观设置方法 ============

    def set_square_color(self, color: typing.Union[QColor, str, tuple]):
        """设置正方形颜色"""
        if isinstance(color, str):
            self._square_color = QColor(color)
        elif isinstance(color, tuple) and len(color) >= 3:
            alpha = color[3] if len(color) > 3 else 128
            self._square_color = QColor(color[0], color[1], color[2], alpha)
        else:
            self._square_color = color
        self.update()

    def set_hover_opacity(self, opacity: float):
        """设置悬停时透明度"""
        self._hover_opacity = max(0.0, min(1.0, opacity))

    def set_pressed_opacity(self, opacity: float):
        """设置按下时透明度"""
        self._pressed_opacity = max(0.0, min(1.0, opacity))

    def set_enabled(self, enabled: bool):
        """设置是否启用点击"""
        self._enabled = enabled

        # 禁用时重置状态
        if not enabled:
            self._hovered = False
            self._pressed = False

        self.update()

    def is_enabled(self) -> bool:
        """获取是否启用点击"""
        return self._enabled