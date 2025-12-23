from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPen, QFont
from PyQt5.QtCore import Qt, QPoint, QRect

class NavItem(QWidget):
    """

    顶部的横向导航的每个导航项类

    """
    def __init__(self, text, state="pending", is_current=False,
                 diamond_size=20, triangle_size=8, text_margin=25, parent=None):
        super().__init__(parent)
        self.text = text
        self.state = state
        self.is_current = is_current
        self.diamond_size = diamond_size
        self.triangle_size = triangle_size
        self.text_margin = text_margin

        self.setMinimumWidth(max(80, diamond_size + 20))
        self.setMinimumHeight(self.text_margin + diamond_size + triangle_size + 10)

    def setState(self, state, is_current=False):
        """设置状态

        Args:
            state (string): 类似于pending？
            is_current (bool, optional): 是否选中这一个？ Defaults to False.
        """
        self.state = state
        self.is_current = is_current
        self.update()

    def getDiamondCenter(self):
        parent_pos = self.mapToParent(QPoint(0, 0))
        x_center = parent_pos.x() + self.width() // 2
        y_center = parent_pos.y() + self.text_margin + self.diamond_size // 2
        return x_center, y_center

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        alpha = 255 if self.state in ("done", "current") else 128
        color = QColor(255, 255, 255, alpha)

        # 文字
        painter.setPen(QColor(255, 255, 255, alpha))
        painter.setFont(QFont("Microsoft YaHei", 10))
        text_rect = QRect(0, 0, self.width(), self.text_margin)
        painter.drawText(text_rect, Qt.AlignHCenter | Qt.AlignVCenter, self.text)

        # 菱形
        x_center = self.width() // 2
        y_center = self.text_margin + self.diamond_size // 2
        half = self.diamond_size // 2
        diamond = QPolygon([
            QPoint(x_center, y_center - half),
            QPoint(x_center + half, y_center),
            QPoint(x_center, y_center + half),
            QPoint(x_center - half, y_center)
        ])
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(diamond)

        # 选中项底部三角箭头
        if self.is_current:
            tri_size = int(self.diamond_size * 0.8)
            h = int(tri_size * (3 ** 0.5) / 2)       # 等边三角高度
            gap = 12  # 三角与菱形间距
            tri_top = y_center + half + gap
            tri = QPolygon([
                QPoint(x_center, tri_top),                      # 顶尖
                QPoint(x_center - tri_size // 2, tri_top + h),  # 左下
                QPoint(x_center + tri_size // 2, tri_top + h)   # 右下
            ])
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(tri)



class NavBar(QWidget):
    """

    顶部的导航栏

    """
    def __init__(self, items, current_index=0,
                 diamond_size=20, triangle_size=8, spacing=60, parent=None):
        super().__init__(parent)
        self.items_text = items
        self.current_index = current_index
        self.diamond_size = diamond_size
        self.triangle_size = triangle_size
        self.spacing = spacing
        self.nav_items = []

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(spacing)
        self.setLayout(self.layout)

        for i, text in enumerate(items):
            state = "done" if i < current_index else "current" if i == current_index else "pending"
            is_current = i == current_index
            nav_item = NavItem(text, state=state, is_current=is_current,
                               diamond_size=diamond_size, triangle_size=triangle_size)
            self.nav_items.append(nav_item)
            self.layout.addWidget(nav_item)

    def setCurrentIndex(self, index):
        self.current_index = index
        for i, nav_item in enumerate(self.nav_items):
            state = "done" if i < index else "current" if i == index else "pending"
            nav_item.setState(state, is_current=(i == index))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 连接线
        for i in range(len(self.nav_items) - 1):
            item1 = self.nav_items[i]
            item2 = self.nav_items[i+1]

            alpha = 255 if i < self.current_index else 128
            pen_style = Qt.SolidLine if i < self.current_index else Qt.DashLine
            color = QColor(255, 255, 255, alpha)
            pen = QPen(color, 2, pen_style)
            painter.setPen(pen)

            x1, y1 = item1.getDiamondCenter()
            x2, y2 = item2.getDiamondCenter()
            painter.drawLine(x1 + item1.diamond_size // 2, y1, x2 - item2.diamond_size // 2, y2)
