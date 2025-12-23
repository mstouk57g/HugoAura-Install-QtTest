from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPixmap, QFontMetrics
from PyQt5.QtCore import Qt, QPoint, QRect
import math

class HexButton(QWidget):
    def __init__(self, text="", font_size=14, icon_path=None,
                 style=1, h_padding=15, v_padding=12, parent=None):
        super().__init__(parent)
        self.text = text
        self.font_size = font_size
        self.icon_path = icon_path
        self.style = style  # 1: 白80%背景+蓝字, 2: 白20%背景+白字, 3: 透明背景白字+三角白边
        self.h_padding = h_padding
        self.v_padding = v_padding

        self.pressed = False
        self.hovered = False

        self.update_size()
        self.setMouseTracking(True)

    def update_size(self):
        font = self.font()
        font.setPointSize(self.font_size)
        self.setFont(font)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self.text)
        text_height = fm.height()

        self.triangle_h = text_height
        self.height_base = text_height + 2 * self.v_padding

        # 图标大小
        if self.icon_path:
            self.icon_size = self.height_base - 2 * self.v_padding
        else:
            self.icon_size = 0

        # 内容宽度 = 文字 + (图标 + h_padding if 有图标)
        content_width = text_width
        if self.icon_path:
            content_width += self.icon_size + self.h_padding

        # 总宽度 = 左三角 + h_padding + 内容宽度 + h_padding + 右三角
        self.width_base = self.triangle_h + self.h_padding + content_width + self.h_padding + self.triangle_h

        self.setFixedSize(self.width_base, self.height_base)

    def setText(self, text):
        self.text = text
        self.update_size()
        self.update()

    def setStyle(self, style):
        self.style = style
        self.update()

    # ---------------- 鼠标事件 ----------------
    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.update()

    def mouseReleaseEvent(self, event):
        if self.pressed:
            self.pressed = False
            self.update()
            if self.rect().contains(event.pos()):
                self.clicked()

    def clicked(self):
        # 点击事件，可被外部重写
        print(f"HexButton clicked: {self.text}")

    # ---------------- 绘制 ----------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        tri_h = self.triangle_h
        tri_base = int(tri_h * math.sqrt(3) / 2)

        # ---------------- 背景颜色 ----------------
        if self.style == 1:
            base_color = QColor(255, 255, 255, int(0.8 * 255))
            text_color = QColor(89, 179, 255)
        elif self.style == 2:
            base_color = QColor(255, 255, 255, int(0.2 * 255))
            text_color = QColor(255, 255, 255)
        elif self.style == 3:  # style 3
            base_color = QColor(255, 255, 255, 0)
            text_color = QColor(255, 255, 255)

        # 悬停效果
        if self.hovered:
            if self.style in [1, 2]:
                base_color = QColor(base_color.lighter(150).red(),
                                    base_color.lighter(150).green(),
                                    base_color.lighter(150).blue(),
                                    min(255, int(base_color.alpha() * 1.2)))
            elif self.style == 3:
                base_color = QColor(255, 255, 255, int(0.4 * 255))  # 悬停变40%白色

        # 按下效果
        if self.pressed and self.style != 3:
            base_color = base_color.darker(120)

        painter.setBrush(base_color)
        painter.setPen(Qt.NoPen)

        # ---------------- 六边形路径 ----------------
        poly = QPolygon([
            QPoint(tri_base, 0),
            QPoint(w - tri_base, 0),
            QPoint(w, h // 2),
            QPoint(w - tri_base, h),
            QPoint(tri_base, h),
            QPoint(0, h // 2)
        ])
        painter.drawPolygon(poly)

        # ---------------- 样式3特殊绘制 ----------------
        if self.style == 3:
            painter.setPen(QColor(255, 255, 255))
            painter.drawLine(QPoint(0, h // 2), QPoint(tri_base, 0))
            painter.drawLine(QPoint(tri_base, h), QPoint(0, h // 2))
            painter.drawLine(QPoint(w - tri_base, 0), QPoint(w, h // 2))
            painter.drawLine(QPoint(w, h // 2), QPoint(w - tri_base, h))
            painter.setPen(Qt.NoPen)

        # ---------------- 文字 + 图标 居中 ----------------
        font = painter.font()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        fm = QFontMetrics(font)

        text_width = fm.horizontalAdvance(self.text)
        content_width = text_width
        if self.icon_path:
            content_width += self.icon_size + self.h_padding

        start_x = (w - content_width) // 2

        # 绘制文字
        text_rect = QRect(start_x, self.v_padding, text_width, h - 2 * self.v_padding)
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text)

        # 绘制图标
        if self.icon_path:
            icon = QPixmap(self.icon_path)
            icon = icon.scaled(self.icon_size, self.icon_size,
                               Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_x = start_x + text_width + self.h_padding
            icon_y = (h - self.icon_size) // 2
            icon_rect = QRect(icon_x, icon_y, self.icon_size, self.icon_size)
            painter.drawPixmap(icon_rect, icon)

class ImageTextButton(HexButton):
    def __init__(self, text="", font_size=14, icon_path=None, h_padding=15, v_padding=12, canclick=True, style=5, parent=None):
        super().__init__(text, font_size, icon_path, style, h_padding, v_padding, parent)
        self.canclick = canclick
        self.style = style  # 4: 白色背景的左图右文 5: 左图右文 (默认), 6: 上图下文

    def update_size(self):
        font = self.font()
        font.setPointSize(self.font_size)
        self.setFont(font)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self.text)
        text_height = fm.height()

        # 图标大小
        if self.icon_path:
            self.icon_size = text_height  # 图片高度与文字高度相同
        else:
            self.icon_size = 0
        if self.style == 5 or self.style == 4:
            # 原有样式：左图右文
            self.height_base = text_height + 2 * self.v_padding

            # 内容宽度 = 文字 + (图标 + h_padding if 有图标)
            content_width = text_width
            if self.icon_path:
                content_width += self.icon_size + self.h_padding

            # 总宽度 = h_padding + 内容宽度 + h_padding
            self.width_base = self.h_padding + content_width + self.h_padding
        elif self.style == 6:
            # 计算图片缩放后的宽度（等比例缩放）
            if self.icon_path:
                original_icon = QPixmap(self.icon_path)
                if not original_icon.isNull():
                    scaled_width = int(self.icon_size * original_icon.width() / original_icon.height())
                    self.height_base = self.icon_size + text_height + 3 * self.v_padding
                else:
                    scaled_width = 0
                    self.height_base = self.icon_size + text_height + 2 * self.v_padding
            else:
                scaled_width = 0
                self.height_base = self.icon_size + text_height + 2 * self.v_padding

            # 宽度 = 内容宽度 + 左右内边距
            content_width = max(text_width, scaled_width)
            self.width_base = content_width + 2 * self.h_padding

        # 设置固定大小，自适应内容
        self.setFixedSize(self.width_base, self.height_base)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        base_color = QColor(255, 255, 255, 0)
        text_color = QColor(255, 255, 255)

        if self.style == 4:
            base_color = QColor(255, 255, 255, int(0.8 * 255))  # 白色80%背景
            text_color = QColor(89, 179, 255)  # 蓝色文字

        # 悬停效果
        if self.hovered:
            if self.canclick:
                if self.style == 4:
                    # style4的悬停：背景变亮1.5倍
                    base_color = QColor(base_color.lighter(150).red(),
                                        base_color.lighter(150).green(),
                                        base_color.lighter(150).blue(),
                                        base_color.alpha())
                else:
                    base_color = QColor(255, 255, 255, int(0.2 * 255))  # 其他样式的悬停

        # 按下效果
        if self.pressed and self.canclick:
            base_color = base_color.darker(120)

        painter.setBrush(base_color)
        painter.setPen(Qt.NoPen)

        # 绘制矩形背景
        painter.drawRect(0, 0, w, h)

        # ---------------- 文字 + 图标 绘制 ----------------
        font = painter.font()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        fm = QFontMetrics(font)

        text_width = fm.horizontalAdvance(self.text)
        text_height = fm.height()

        if self.style == 5 or self.style == 4:  # style=4和5都使用左图右文布局
            content_width = text_width
            if self.icon_path:
                content_width += self.icon_size + self.h_padding

            start_x = (w - content_width) // 2

            # 绘制图标
            if self.icon_path:
                icon = QPixmap(self.icon_path)
                icon = icon.scaled(self.icon_size, self.icon_size,
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_x = start_x  # 图标从起始位置开始
                icon_y = (h - self.icon_size) // 2
                icon_rect = QRect(icon_x, icon_y, self.icon_size, self.icon_size)
                painter.drawPixmap(icon_rect, icon)
                # 更新文字起始位置（图标右侧）
                start_x += self.icon_size + self.h_padding

            # 绘制文字
            text_rect = QRect(start_x, self.v_padding, text_width, h - 2 * self.v_padding)
            painter.setPen(text_color)
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text)
        elif self.style == 6:
            # style=6：上图下文
            # 绘制图标（居中）
            text_y = self.v_padding + self.icon_size
            if self.icon_path:
                icon = QPixmap(self.icon_path)
                # 等比例缩放，高度固定为文字高度
                scaled_icon = icon.scaledToHeight(self.icon_size, Qt.SmoothTransformation)
                icon_width = scaled_icon.width()
                icon_x = (w - icon_width) // 2
                icon_y = self.v_padding
                icon_rect = QRect(icon_x, icon_y, icon_width, self.icon_size)
                painter.drawPixmap(icon_rect, scaled_icon)
                text_y += self.v_padding

            # 绘制文字（居中）
            text_x = (w - text_width) // 2
            text_rect = QRect(text_x, text_y, text_width, text_height)
            painter.setPen(text_color)
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text)