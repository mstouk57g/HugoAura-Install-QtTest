import sys
from PyQt5.QtWidgets import QApplication
from window import ImageWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
                            QWidget {
                            background-color: transparent;
                            }

                            QPushButton#closeButton {
                                background-color: transparent;
                                color: white;
                                border: none;
                                font: bold 20px;
                            }

                            QPushButton#closeButton:hover {
                                color: red;
                            }
                            """)

    window = ImageWindow(background_path="resources/background.png", title_image_path="resources/title.png", install_image_path="resources/install.jpg", icon_path="resources/aura_black.png")

    window.Installation_page.setCurrentIndex(0)

    current_size = window.size()
    window.setFixedSize(current_size)
    window.show()
    sys.exit(app.exec_())
