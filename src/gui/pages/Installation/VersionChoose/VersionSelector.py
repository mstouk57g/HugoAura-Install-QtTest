from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui.widgets.ItemList import SelectableListWidget

class VersionSelector(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.selectable_list = SelectableListWidget()

        sample_items = [
            {
                'tag': 'v1.0',
                'name': '[Rel] v1.0.0-release',
                'size': '45.6 MB',
                'time': '2024-01-01',
                'newest': True,
                'unavailable': False
            },
            {
                'tag': 'v0.9',
                'name': '[Dev] v0.9.5-dev',
                'size': '42.1 MB',
                'time': '2023-12-15',
                'newest': False,
                'unavailable': False
            },
            {
                'tag': 'v0.8',
                'name': '[Old] v0.8.2',
                'size': '40.3 MB',
                'time': '2023-11-30',
                'newest': False,
                'unavailable': True
            },
            {
                'tag': 'v0.11',
                'name': '[Old] v0.8.2',
                'size': '40.3 MB',
                'time': '2023-11-30',
                'newest': False,
                'unavailable': True
            },
            {
                'tag': 'v0.12',
                'name': '[Old] v0.8.2',
                'size': '40.3 MB',
                'time': '2023-11-30',
                'newest': False,
                'unavailable': True
            },
            {
                'tag': 'v0.83',
                'name': '[Old] v0.8.2',
                'size': '40.3 MB',
                'time': '2023-11-30',
                'newest': False,
                'unavailable': True
            },
            {
                'tag': 'v0.84',
                'name': '[Old] v0.8.2',
                'size': '40.3 MB',
                'time': '2023-11-30',
                'newest': False,
                'unavailable': True
            },
            {
                'tag': 'v0.5',
                'name': '[Old] v0.8.2',
                'size': '40.3 MB',
                'time': '2023-11-30',
                'newest': False,
                'unavailable': True
            }
        ]

        self.selectable_list.setItems(sample_items)
        self.selectable_list.selectionChanged.connect(self.onSelectionChanged)
        if sample_items:
            self.selectable_list.setSelectedItem(sample_items[0])
        main_layout.addWidget(self.selectable_list)

    def onSelectionChanged(self, item_data):
        """选择改变时的处理"""
        print(f"选中了: {item_data.get('name')}")

    def getSelectedVersion(self):
        """获取当前选中的版本"""
        return self.selectable_list.getSelectedItem()

    def setSelectedVersion(self, item_data):
        """设置选中的版本"""
        self.selectable_list.setSelectedItem(item_data)

    def setVersionItems(self, items):
        """设置版本项目列表"""
        self.selectable_list.setItems(items)