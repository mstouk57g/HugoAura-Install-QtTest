from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QFontMetrics, QPen, QBrush

class TransparentLineEdit(QLineEdit):
    """_summary_

    这是在获取希沃管家安装地址目录的那个横向的白色的一横行的文本LineEdit

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("border: none; background: transparent; color: transparent;")
        self.setFrame(False)

        # 默认属性
        self.text_color = QColor(255, 255, 255)  # 默认白色文字
        self.text_opacity = 255  # 默认完全不透明(0-255)
        self.line_color = QColor(255, 255, 255)  # 默认白色线条
        self.placeholder_opacity = 153  # 60% 不透明度 (255 * 0.6 = 153)

        # 选中文本的背景颜色
        self.selection_background = QColor(0, 120, 215, 180)  # 蓝色半透明
        self.selection_text_color = QColor(255, 255, 255)  # 白色文字

        # 监听文本变化、光标位置变化和选择变化
        self.textChanged.connect(self.update)
        self.cursorPositionChanged.connect(self.update)
        self.selectionChanged.connect(self.update)

    def setTextColor(self, color):
        """设置文字颜色"""
        self.text_color = color
        self.update()

    def setTextOpacity(self, opacity):
        """设置文字不透明度(0-255)"""
        self.text_opacity = max(0, min(255, opacity))
        self.update()

    def setLineColor(self, color):
        """设置线条颜色"""
        self.line_color = color
        self.update()

    def setPlaceholderOpacity(self, opacity):
        """设置占位符文本不透明度(0-255)"""
        self.placeholder_opacity = max(0, min(255, opacity))
        self.update()

    def setSelectionBackground(self, color):
        """设置选中文本的背景颜色"""
        self.selection_background = color
        self.update()

    def setSelectionTextColor(self, color):
        """设置选中文本的文字颜色"""
        self.selection_text_color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        fm = QFontMetrics(self.font())
        text_height = fm.height()

        line_rect = QRect(0, self.height()-2, self.width(), 2) # 绘制底部线条
        painter.fillRect(line_rect, self.line_color)

        text = self.text()
        has_selection = self.hasSelectedText() # 检查是否有选中文本或光标激活
        has_focus = self.hasFocus()

        if not text: # 如果没有文本
            placeholder_text = self.placeholderText()
            if placeholder_text:
                # 设置占位符文本颜色为60%不透明度的白色
                placeholder_color = QColor(255, 255, 255)
                placeholder_color.setAlpha(self.placeholder_opacity)
                painter.setPen(placeholder_color)
                painter.drawText(0, 0, self.width(), text_height, Qt.AlignLeft | Qt.AlignVCenter, placeholder_text)

            # 如果有焦点，则手动绘制光标
            if has_focus:
                cursor_rect = QRect(0, 0, 2, text_height)
                painter.fillRect(cursor_rect, QColor(255, 255, 255))
            return

        # 如果有选中文本或光标激活，调用父类绘制，显示选中效果和光标
        if has_selection or has_focus:
            original_style = self.styleSheet()
            self.setStyleSheet(f"border: none; background: transparent; color: {self.text_color.name()};")
            super().paintEvent(event)
            self.setStyleSheet(original_style)
            return

        # 设置文本颜色和不透明度
        text_color = QColor(self.text_color)
        text_color.setAlpha(self.text_opacity)

        # 正常情况下的文本绘制
        text_width = fm.width(text)

        # 如果文本宽度小于控件宽度，直接绘制文本
        if text_width <= self.width():
            painter.setPen(text_color)
            painter.drawText(0, 0, self.width(), text_height, Qt.AlignLeft | Qt.AlignVCenter, text)
            return

        # 检查文本是否在开头或结尾
        cursor_pos = self.cursorPosition()
        at_start = cursor_pos == 0
        at_end = cursor_pos == len(text)

        # 计算滚动文本偏移量
        scroll_offset = 0
        if text_width > self.width():
            # 计算文本滚动位置
            avg_char_width = text_width / len(text)
            visible_chars = self.width() / avg_char_width

            if cursor_pos > visible_chars / 2:
                scroll_offset = min(cursor_pos * avg_char_width - self.width() / 2,
                                  text_width - self.width())

        # 创建渐变区域
        gradient = QLinearGradient(0, 0, self.width(), 0)

        # 左侧渐变
        if at_start or scroll_offset <= 0:
            # 文本在开头，左侧不透明
            gradient.setColorAt(0, text_color)
            gradient.setColorAt(0.2, text_color)
        else:
            # 左侧渐变透明
            start_color = QColor(text_color)
            start_color.setAlpha(int(self.text_opacity * 0.05))
            gradient.setColorAt(0, start_color)
            gradient.setColorAt(0.2, text_color)

        # 中间部分
        gradient.setColorAt(0.2, text_color)
        gradient.setColorAt(0.8, text_color)

        # 右侧渐变
        if at_end or scroll_offset + self.width() >= text_width:
            # 文本在结尾，右侧不透明
            gradient.setColorAt(0.8, text_color)
            gradient.setColorAt(1, text_color)
        else:
            # 右侧渐变透明
            end_color = QColor(text_color)
            end_color.setAlpha(int(self.text_opacity * 0.05))
            gradient.setColorAt(0.8, text_color)
            gradient.setColorAt(1, end_color)

        pen = QPen()
        pen.setBrush(QBrush(gradient))
        painter.setPen(pen)

        text_rect = QRect(-scroll_offset, 0, text_width, text_height)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, text)

    def getText(self):
        """获取文本框内容"""
        return self.text()