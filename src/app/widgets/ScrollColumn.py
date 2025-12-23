from PyQt5.QtWidgets import QWidget, QScrollBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QTransform

class ImageButton(QWidget):
    """带旋转功能的图片按钮"""
    def __init__(self, img_path, rotate_angle=0, size=30, parent=None):
        super().__init__(parent)
        self.img_path = img_path
        self.img = QPixmap(img_path)
        self.angle = rotate_angle
        self.size = size
        self.setFixedSize(self.size, self.size)

    def set_size(self, size):
        self.size = size
        self.setFixedSize(self.size, self.size)
        self.update()

    def set_image(self, img_path):
        self.img_path = img_path
        self.img = QPixmap(img_path)
        self.update()

    def paintEvent(self, event):
        if self.img.isNull():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        transform = QTransform()
        transform.translate(w / 2, h / 2)
        transform.rotate(self.angle)
        transform.translate(-w / 2, -h / 2)
        rotated_pix = self.img.transformed(transform, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, w, h, rotated_pix)


class ScrollColumn(QWidget):
    """

    这是滚动列控件，上下按钮 + 自定义滚动条。用于TextEdit滚动

    注意：这个东西只能绑定到TextEdit上。所以需要把控件丢到TextEdit上

    """
    def __init__(self, parent=None, scroll_width=40, btn_size=30, scrollbar_width=5,
                 up_image="resources/next.png", down_image="resources/next.png",
                 scrollbar_bg="rgba(50,159,255,80)", scrollbar_handle="rgba(50,159,255,255)"):
        super().__init__(parent)
        self.scroll_width = scroll_width        # 滑动区域宽度
        self.btn_size = btn_size                # 按钮大小
        self.scrollbar_width = scrollbar_width  # 滚动条宽度

        # 图片路径属性
        self.up_btn_image_path = up_image
        self.down_btn_image_path = down_image

        # 颜色属性
        self.scrollbar_bg_color = scrollbar_bg
        self.scrollbar_handle_color = scrollbar_handle

        # 上下按钮
        self.up_button = ImageButton(self.up_btn_image_path, rotate_angle=-90, size=self.btn_size, parent=self)
        self.down_button = ImageButton(self.down_btn_image_path, rotate_angle=90, size=self.btn_size, parent=self)

        # 滚动条
        self.scrollbar = QScrollBar(Qt.Vertical, self)
        self.scrollbar.setFixedWidth(self.scrollbar_width)
        self.update_scrollbar_style()

        # 点击事件
        self.up_button.mousePressEvent = lambda e: self.scroll_up()
        self.down_button.mousePressEvent = lambda e: self.scroll_down()

        self.text_edit = None  # 用于绑定文本框

        # ScrollColumn 总宽度可由外部固定，不自动撑大
        self.setFixedWidth(max(self.scroll_width, self.scrollbar_width, self.btn_size))

    def bind_text_edit(self, text_edit):
        """绑定 QTextEdit

        Args:
            text_edit (QTextEdit): 对应的QTextEdit
        """
        self.text_edit = text_edit
        text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        te_scroll = text_edit.verticalScrollBar()

        te_scroll.valueChanged.connect(self.scrollbar.setValue)
        self.scrollbar.valueChanged.connect(te_scroll.setValue)
        te_scroll.rangeChanged.connect(lambda minv, maxv: self.scrollbar.setRange(minv, maxv))

    def scroll_up(self):
        if self.text_edit:
            self.scrollbar.setValue(self.scrollbar.value() - self.text_edit.fontMetrics().height())

    def scroll_down(self):
        if self.text_edit:
            self.scrollbar.setValue(self.scrollbar.value() + self.text_edit.fontMetrics().height())

    def set_scroll_width(self, width: int):
        """修改滑动区域宽度（固定，不影响按钮）"""
        self.scroll_width = width
        self.update()

    def set_button_size(self, size: int):
        """修改上下按钮大小（固定，不影响滑动区域）"""
        self.btn_size = size
        self.up_button.set_size(size)
        self.down_button.set_size(size)
        self.update()

    def set_button_images(self, up_path, down_path):
        """设置上下两个按钮的图片

        Args:
            up_path (string): 向上滑动按钮的图片
            down_path (string): 向下滑动按钮的图片
        """
        self.up_btn_image_path = up_path
        self.down_btn_image_path = down_path
        self.up_button.set_image(up_path)
        self.down_button.set_image(down_path)

    def set_scrollbar_colors(self, bg_color, handle_color):
        """设置ScrollBar的颜色

        Args:
            bg_color (string): 前景色
            handle_color (string): 背景色
        """
        self.scrollbar_bg_color = bg_color
        self.scrollbar_handle_color = handle_color
        self.update_scrollbar_style()

    def update_scrollbar_style(self):
        self.scrollbar.setStyleSheet(f"""
            QScrollBar:vertical {{
                background: {self.scrollbar_bg_color};
                width: {self.scrollbar_width}px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.scrollbar_handle_color};
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        total_h = self.height()
        scroll_h = max(1, total_h - self.btn_size * 2)

        center_x = self.width() / 2
        up_x = int(center_x - self.up_button.width() / 2)
        scroll_x = int(center_x - self.scrollbar.width() / 2)
        down_x = int(center_x - self.down_button.width() / 2)

        self.up_button.setGeometry(up_x, 0, self.up_button.width(), self.btn_size)
        self.scrollbar.setGeometry(scroll_x, self.btn_size, self.scrollbar.width(), scroll_h)
        self.down_button.setGeometry(down_x, self.btn_size + scroll_h, self.down_button.width(), self.btn_size)
