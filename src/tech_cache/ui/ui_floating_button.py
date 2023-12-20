class FloatingButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Set button properties (size, icon, etc.)
        self.setFixedSize(50, 50)
        self.setText("+")  # Example, you can set an icon instead
        self.setStyleSheet("QPushButton { border-radius: 25px; }")  # Example styling

    def updatePosition(self):
        if self.parent():
            parent_size = self.parent().size()
            x = parent_size.width() - self.width() - 20  # 20 is the margin
            y = parent_siz
