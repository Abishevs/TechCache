from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer

def show_yes_no_dialog(parent, 
                       title:str, 
                       message:str="You have unsaved changes. Are you sure you want to discard them?"):
            reply = QtWidgets.QMessageBox.question(parent,
                                                   title,
                                                   message,
                                                   QtWidgets.QMessageBox.StandardButton.Yes 
                                                   | QtWidgets.QMessageBox.StandardButton.No,
                                                   QtWidgets.QMessageBox.StandardButton.No)
            return reply == QtWidgets.QMessageBox.StandardButton.Yes

class NotificationWidget(QWidget):
    def __init__(self, message, duration=2000):
        super().__init__()
        self.initUI(message, duration)

    def initUI(self, message, duration):
        self.label = QLabel(message)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Set the position and size
        self.setGeometry(700, 30, 200, 50)  # Adjust these values as needed

        # Set a QTimer to hide the notification after 'duration' milliseconds
        QTimer.singleShot(duration, self.hide)
