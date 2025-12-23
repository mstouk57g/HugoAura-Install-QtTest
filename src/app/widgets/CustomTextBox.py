from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QTextCursor, QTextBlockFormat, QFont, QPainter, QPolygonF, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal
from widgets.ScrollColumn import ScrollColumn

class CustomTextBox(QWidget):
    """

    文本框，显示agreement的那个

    """
    def __init__(self, parent=None, scroll_width=5, scrollbar_width=5, cut=10, markdown_enabled=False):
        super().__init__(parent)

        # Markdown 支持属性
        self._markdown_enabled = markdown_enabled

        # 超链接颜色设置（但好像没有用）
        self._link_color = "#0000FF"  # 一般默认蓝色
        self._link_visited_color = "#800080"  # 访问后默认紫色
        self._link_hover_color = "#FF0000"  # 悬停默认红色

        # 文本框
        self.text_edit = QTextEdit(self)
        self._update_text_edit_style()

        # 滚动列
        self.scroll_col = ScrollColumn(self, scroll_width=scroll_width, btn_size=20, scrollbar_width=scrollbar_width)
        self.scroll_col.bind_text_edit(self.text_edit)

        # 布局
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.text_edit, 1)
        layout.addWidget(self.scroll_col, 0)

        # 切角背景
        self.cut = cut

        # 行距属性
        self._line_spacing_value = None
        self._line_spacing_mode = "fixed"

    # ========== 超链接颜色设置 ==========
    def set_link_color(self, color):
        """设置超链接颜色

        Args:
            color: 颜色名称字符串或十六进制颜色字符串
                例如: "#FF5722", "red", "rgb(255, 87, 34)"
        """
        self._link_color = color
        self._update_text_edit_style()

    def set_visited_link_color(self, color):
        """设置访问过的超链接颜色"""
        self._link_visited_color = color
        self._update_text_edit_style()

    def set_link_hover_color(self, color):
        """设置鼠标悬停时的超链接颜色"""
        self._link_hover_color = color
        self._update_text_edit_style()

    def get_link_color(self):
        """获取当前超链接颜色"""
        return self._link_color

    def get_visited_link_color(self):
        """获取当前访问过的链接颜色"""
        return self._link_visited_color

    def get_link_hover_color(self):
        """获取当前悬停链接颜色"""
        return self._link_hover_color

    def _update_text_edit_style(self):
        """更新文本框的样式，包含超链接颜色设置"""
        base_style = "background: transparent; border: none;"

        # 添加超链接样式
        link_style = f"""
        a {{
            color: {self._link_color};
            text-decoration: underline;
        }}
        a:visited {{
            color: {self._link_visited_color};
            text-decoration: underline;
        }}
        a:hover {{
            color: {self._link_hover_color};
            text-decoration: underline;
        }}
        """

        self.text_edit.setStyleSheet(base_style + link_style)

    # ========== Markdown 支持 ==========
    def set_markdown_enabled(self, enabled: bool):
        """设置是否启用 Markdown 解析"""
        self._markdown_enabled = enabled

    def is_markdown_enabled(self) -> bool:
        """获取当前是否启用 Markdown 解析"""
        return self._markdown_enabled

    def set_markdown_text(self, text: str):
        """设置 Markdown 格式的文本（自动启用 Markdown）"""
        self._markdown_enabled = True
        self._set_text_with_markdown(text)

    # ========== 文本接口 ==========
    def set_editable(self, editable: bool):
        self.text_edit.setReadOnly(not editable)

    def set_font(self, font_name="Microsoft YaHei", size=12):
        font = QFont(font_name, size)
        self.text_edit.setFont(font)
        if self._line_spacing_value is not None:
            self.apply_line_spacing()

    def set_text_color(self, color: str):
        """设置文本颜色，同时保留超链接样式"""
        base_style = f"color: {color}; background: transparent; border: none;"

        # 超链接样式
        link_style = f"""
        a {{
            color: {self._link_color};
            text-decoration: underline;
        }}
        a:visited {{
            color: {self._link_visited_color};
            text-decoration: underline;
        }}
        a:hover {{
            color: {self._link_hover_color};
            text-decoration: underline;
        }}
        """

        self.text_edit.setStyleSheet(base_style + link_style)

    def set_text(self, text: str):
        """设置文本内容，根据 Markdown 设置决定是否解析"""
        if self._markdown_enabled:
            self._set_text_with_markdown(text)
        else:
            self._set_plain_text(text)

    def _set_plain_text(self, text: str):
        """设置纯文本"""
        self.text_edit.setPlainText(text)
        if self._line_spacing_value is not None:
            self.apply_line_spacing()

    def _set_text_with_markdown(self, text: str):
        """设置并解析 Markdown 文本"""
        try:
            self._update_text_edit_style()

            # 使用 Qt 内置的 Markdown 支持
            self.text_edit.setMarkdown(text)
        except AttributeError:
            # 如果 Qt 版本不支持 setMarkdown，回退到纯文本
            self.text_edit.setPlainText(text)

        if self._line_spacing_value is not None:
            self.apply_line_spacing()

    # ========== 行距 ==========
    def set_line_spacing(self, value: float, mode="fixed"):
        self._line_spacing_value = value
        self._line_spacing_mode = mode
        self.apply_line_spacing()

    def apply_line_spacing(self):
        if self._line_spacing_value is None:
            return
        doc = self.text_edit.document()
        block = doc.firstBlock()
        while block.isValid():
            cursor = QTextCursor(block)
            cursor.setPosition(block.position())
            block_fmt = cursor.blockFormat()
            if self._line_spacing_mode == "fixed":
                block_fmt.setLineHeight(int(self._line_spacing_value), QTextBlockFormat.FixedHeight)
            else:
                block_fmt.setLineHeight(int(self._line_spacing_value * 100), QTextBlockFormat.ProportionalHeight)
            cursor.setBlockFormat(block_fmt)
            block = block.next()

    # ========== 滚动列属性接口 ==========
    def set_scroll_width(self, width: int):
        self.scroll_col.set_scroll_width(width)

    def set_button_size(self, size: int):
        self.scroll_col.set_button_size(size)

    def set_scroll_column_images(self, up_path, down_path):
        self.scroll_col.set_button_images(up_path, down_path)

    def set_scroll_column_colors(self, bg_color, handle_color):
        self.scroll_col.set_scrollbar_colors(bg_color, handle_color)

    # ========== 切角背景 ==========
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        cut = self.cut
        path = QPolygonF([
            QPointF(rect.left() + cut, rect.top()),
            QPointF(rect.right(), rect.top()),
            QPointF(rect.right(), rect.bottom() - cut),
            QPointF(rect.right() - cut, rect.bottom()),
            QPointF(rect.left(), rect.bottom()),
            QPointF(rect.left(), rect.top() + cut)
        ])
        painter.setBrush(QColor(255, 255, 255, 204))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(path)

    # ========== 动态按钮大小 ==========
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 按钮大小 = 控件宽度的 1/15，最小 10px
        dynamic_btn_size = max(10, int(self.width() / 30))
        self.scroll_col.set_button_size(dynamic_btn_size)


class GradientTextBox(QWidget):
    """渐变透明文本框组件"""

    # 定义信号：当文本到达底部时触发
    reached_bottom = pyqtSignal()

    def __init__(self, parent=None, markdown_enabled=False):
        super().__init__(parent)

        # Markdown 支持属性
        self._markdown_enabled = markdown_enabled

        # 超链接颜色设置
        self._link_color = "#0000FF"  # 默认蓝色
        self._link_visited_color = "#800080"  # 访问后紫色
        self._link_hover_color = "#FF0000"  # 悬停红色

        # 渐变设置
        self._gradient_enabled = True  # 是否启用渐变
        self._gradient_height = 30  # 渐变区域高度
        self._gradient_color = QColor(43, 43, 43)  # 渐变起始颜色（暗色主题背景）

        # 滑动控制
        self._scrollable = True  # 是否允许滑动
        self._is_at_bottom = False  # 是否在底部

        # 创建文本框
        self.text_edit = self._create_text_edit()

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.text_edit)

        # 连接滚动信号
        self.text_edit.verticalScrollBar().valueChanged.connect(self._check_scroll_position)

    def _create_text_edit(self):
        """创建并配置文本框"""
        text_edit = QTextEdit(self)
        text_edit.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                color: white;
            }
        """)

        # 设置视口背景透明
        text_edit.setAttribute(Qt.WA_TranslucentBackground)

        # 隐藏滚动条
        text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 设置文档边距
        text_edit.document().setDocumentMargin(10)

        return text_edit

    # ========== 渐变设置 ==========
    def set_gradient_enabled(self, enabled: bool):
        """设置是否启用底部渐变透明效果"""
        self._gradient_enabled = enabled
        self.update()

    def set_gradient_height(self, height: int):
        """设置渐变区域的高度（像素）"""
        self._gradient_height = max(10, min(height, 100))  # 限制在10-100像素
        self.update()

    def set_gradient_color(self, color):
        """设置渐变的起始颜色"""
        if isinstance(color, str):
            self._gradient_color = QColor(color)
        elif isinstance(color, QColor):
            self._gradient_color = color
        else:
            self._gradient_color = QColor(color)
        self.update()

    # ========== 滑动控制 ==========
    def set_scrollable(self, enabled: bool):
        """设置是否允许滑动"""
        self._scrollable = enabled
        if not enabled:
            # 锁定滚动位置
            scrollbar = self.text_edit.verticalScrollBar()
            scrollbar.setValue(0)
        self.update()

    # ========== 超链接颜色设置 ==========
    def set_link_color(self, color):
        """设置超链接颜色"""
        self._link_color = color
        self._update_text_edit_style()

    def set_visited_link_color(self, color):
        """设置访问过的超链接颜色"""
        self._link_visited_color = color
        self._update_text_edit_style()

    def set_link_hover_color(self, color):
        """设置鼠标悬停时的超链接颜色"""
        self._link_hover_color = color
        self._update_text_edit_style()

    def _update_text_edit_style(self):
        """更新文本框的样式，包含超链接颜色设置"""
        style = f"""
            QTextEdit {{
                background: transparent;
                border: none;
            }}
            a {{
                color: {self._link_color};
                text-decoration: underline;
            }}
            a:visited {{
                color: {self._link_visited_color};
                text-decoration: underline;
            }}
            a:hover {{
                color: {self._link_hover_color};
                text-decoration: underline;
            }}
        """
        self.text_edit.setStyleSheet(style)

    # ========== Markdown 支持 ==========
    def set_markdown_enabled(self, enabled: bool):
        """设置是否启用 Markdown 解析"""
        self._markdown_enabled = enabled

    def is_markdown_enabled(self) -> bool:
        """获取当前是否启用 Markdown 解析"""
        return self._markdown_enabled

    def set_markdown_text(self, text: str):
        """设置 Markdown 格式的文本（自动启用 Markdown）"""
        self._markdown_enabled = True
        self._set_text_with_markdown(text)

    # ========== 文本接口 ==========
    def set_editable(self, editable: bool):
        """设置是否可编辑"""
        self.text_edit.setReadOnly(not editable)

    def set_font(self, font_name="Microsoft YaHei", size=12):
        """设置字体"""
        font = QFont(font_name, size)
        self.text_edit.setFont(font)
        if hasattr(self, '_line_spacing_value') and self._line_spacing_value is not None:
            self.apply_line_spacing()
        self.update()

    def set_text_color(self, color: str):
        """设置文本颜色"""
        style = f"""
            QTextEdit {{
                color: {color};
                background: transparent;
                border: none;
            }}
            a {{
                color: {self._link_color};
                text-decoration: underline;
            }}
            a:visited {{
                color: {self._link_visited_color};
                text-decoration: underline;
            }}
            a:hover {{
                color: {self._link_hover_color};
                text-decoration: underline;
            }}
        """
        self.text_edit.setStyleSheet(style)
        self.update()

    def set_text(self, text: str):
        """设置文本内容，根据 Markdown 设置决定是否解析"""
        if self._markdown_enabled:
            self._set_text_with_markdown(text)
        else:
            self._set_plain_text(text)
        self._check_scroll_position()

    def _set_plain_text(self, text: str):
        """设置纯文本"""
        self.text_edit.setPlainText(text)
        if hasattr(self, '_line_spacing_value') and self._line_spacing_value is not None:
            self.apply_line_spacing()
        self.update()

    def _set_text_with_markdown(self, text: str):
        """设置并解析 Markdown 文本"""
        try:
            self.text_edit.setMarkdown(text)
        except:
            # 如果失败，使用纯文本
            self.text_edit.setPlainText(text)

        if hasattr(self, '_line_spacing_value') and self._line_spacing_value is not None:
            self.apply_line_spacing()
        self.update()

    def get_text(self) -> str:
        """获取文本内容"""
        if self._markdown_enabled:
            return self.text_edit.toMarkdown()
        else:
            return self.text_edit.toPlainText()

    # ========== 行距设置 ==========
    def set_line_spacing(self, value: float, mode="fixed"):
        """设置行距"""
        self._line_spacing_value = value
        self._line_spacing_mode = mode
        self.apply_line_spacing()

    def apply_line_spacing(self):
        """应用行距设置"""
        if not hasattr(self, '_line_spacing_value') or self._line_spacing_value is None:
            return

        doc = self.text_edit.document()
        block = doc.firstBlock()

        while block.isValid():
            cursor = QTextCursor(block)
            cursor.setPosition(block.position())
            block_fmt = cursor.blockFormat()

            if self._line_spacing_mode == "fixed":
                block_fmt.setLineHeight(int(self._line_spacing_value), QTextBlockFormat.FixedHeight)
            else:
                block_fmt.setLineHeight(int(self._line_spacing_value * 100), QTextBlockFormat.ProportionalHeight)

            cursor.setBlockFormat(block_fmt)
            block = block.next()

        self.update()

    # ========== 滚动位置检查 ==========
    def _check_scroll_position(self):
        """检查滚动位置，判断是否到达底部"""
        scrollbar = self.text_edit.verticalScrollBar()

        # 获取最大值和当前值
        max_value = scrollbar.maximum()
        current_value = scrollbar.value()

        # 检查是否到达底部（容差为5像素）
        is_now_at_bottom = current_value >= max_value - 5
        if is_now_at_bottom != self._is_at_bottom: # 如果状态改变
            self._is_at_bottom = is_now_at_bottom
            if is_now_at_bottom:
                self.reached_bottom.emit()

        self.update()

    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        self.update()

    # ========== 绘制渐变 ==========
    def paintEvent(self, event):
        """绘制组件，包括渐变效果"""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 获取整个组件的矩形
        widget_rect = self.rect()

        # 1. 绘制背景（暗色）
        painter.fillRect(widget_rect, QColor(43, 43, 43))

        # 2. 绘制文本框背景区域
        text_edit_rect = self.text_edit.geometry()
        painter.fillRect(text_edit_rect, QColor(60, 60, 60, 200))

        # 3. 绘制渐变效果
        if self._gradient_enabled and not self._is_at_bottom:
            # 计算渐变区域
            gradient_rect = QRectF(
                text_edit_rect.left(),
                text_edit_rect.bottom() - self._gradient_height,
                text_edit_rect.width(),
                self._gradient_height
            )

            gradient = QLinearGradient(
                QPointF(gradient_rect.left(), gradient_rect.top()),
                QPointF(gradient_rect.left(), gradient_rect.bottom())
            )

            # 从完全透明到背景色
            end_color = self._gradient_color
            gradient.setColorAt(0.0, QColor(end_color.red(), end_color.green(), end_color.blue(), 0))
            gradient.setColorAt(1.0, end_color)

            # 绘制渐变
            painter.fillRect(gradient_rect, gradient)

        # 4. 绘制边框
        painter.setPen(QColor(100, 100, 100))
        painter.drawRect(text_edit_rect.adjusted(0, 0, -1, -1))

    # ========== 事件处理 ==========
    def wheelEvent(self, event):
        """处理鼠标滚轮事件"""
        if self._scrollable:
            # 允许滑动：传递给文本框处理
            self.text_edit.wheelEvent(event)
        else:
            # 不允许滑动：忽略事件
            event.ignore()

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if self._scrollable:
            # 允许滑动：传递给文本框
            self.text_edit.mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if self._scrollable:
            self.text_edit.mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if self._scrollable:
            self.text_edit.mouseReleaseEvent(event)
        else:
            super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        """处理大小改变事件"""
        super().resizeEvent(event)
        self.update()