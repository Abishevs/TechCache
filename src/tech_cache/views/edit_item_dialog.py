import logging
from PyQt6 import QtWidgets, QtGui
from tech_cache.models.item import Item
from tech_cache.ui.ui_edit_item_dialog import Ui_edit_item_dialog
from tech_cache.utils.logger_conf import LoggerConfig
from tech_cache.utils.notifify import show_yes_no_dialog


class BaseItemDialog(QtWidgets.QDialog, Ui_edit_item_dialog):
    def __init__(self, item: Item | None = None, parent=None):
        super().__init__(parent)
        self.error_logger = logging.getLogger(LoggerConfig.ERROR_LOGGER)
        self.action_logger = logging.getLogger(LoggerConfig.ACTION_LOGGER)
        self.debug_logger = logging.getLogger(LoggerConfig.DEBUG_LOGGER)

        # setup
        self.setupUi(self)
        self.setup_listeners()
        self.button_signals()
        self.item = item if item else Item()

        # state variables
        self.unsaved_changes = False # state variable

        # shortcuts
        self.setup_apply_shortcut()


    def setup_apply_shortcut(self):
        apply_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        apply_shortcut.activated.connect(self.apply_changes)

    def button_signals(self):
        """
        Creates buttons and adds signlas and on click listeners for them
        """
        # get buttons
        reset_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Reset)
        save_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        discard_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Discard)
        apply_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Apply)

        # add signals to each button
        reset_button.clicked.connect(self.reset_fields)
        save_button.clicked.connect(self.save_changes)
        discard_button.clicked.connect(self.discard_changes)
        apply_button.clicked.connect(self.apply_changes)

    def populate_fields(self):
        self.nameInput.insert(self.item.name)
        self.categoryInput.insert(self.item.category)
        self.skuInput.insert(self.item.sku)
        self.quantitySpinBox.setMinimum(0)
        self.quantitySpinBox.setMaximum(100000)
        self.quantitySpinBox.setValue(self.item.quantity)
        self.specificationInput.insertPlainText(self.item.specification)

    def setup_listeners(self):
        # field listeners for changes
        self.nameInput.textChanged.connect(self.on_input_changed)
        self.skuInput.textChanged.connect(self.on_input_changed)
        self.categoryInput.textChanged.connect(self.on_input_changed)
        self.quantitySpinBox.textChanged.connect(self.on_input_changed)
        self.specificationInput.textChanged.connect(self.on_input_changed)

    def on_input_changed(self):
        """sets state to true, if user changed field"""
        self.unsaved_changes = True

    def closeEvent(self, event):
        """
        Check to ensure that changes are saved if not ask user to
        confirm discarding or cancle closing
        """
        if self.unsaved_changes:
            if show_yes_no_dialog(self,
                                  title='Unsaved changes',
                                  message="You have unsaved changes. Are you sure you want to close?"):
                event.accept()  # Discard changes and close 
            else:
                event.ignore()  # Cancel closing
        else:
            event.accept()  # No unsaved changes, so just close

    def validate_fields(self):
        self.debug_logger.debug("validating...")
        if self.nameInput.text() == "" or self.item.name == "":
                self.debug_logger.debug("empty name field")
                QtWidgets.QMessageBox.warning(self,
                                              "Mandatory Field", 
                                              "Name field can't be empty")
                return False
        return True

    def save_changes(self):
        if self.validate_fields():
            self.debug_logger.debug("Saving...", exc_info=True)
            self.apply_changes()
            self.accept()
        else:
            # don't close dialog, keep it open
            self.debug_logger.debug("Failed valdation...", exc_info=True)
            # pass
            return

    def apply_changes(self):
        """Gets and Applies changes to item object
        """
        self.debug_logger.debug("applying changes...", exc_info=True)

        new_name = self.nameInput.text()
        new_category = self.categoryInput.text()
        new_sku = self.skuInput.text()
        new_quantity = self.quantitySpinBox.value()
        new_specification = self.specificationInput.toPlainText()

        # checks if fields value is diffrent than item.field value
        if new_sku != self.item.sku:
            self.item.sku = new_sku
        
        if new_name != self.item.name:
            self.item.name = new_name

        if new_category != self.item.category:
            self.item.category = new_category
        
        if new_quantity != self.item.quantity:
            self.item.quantity = new_quantity

        if new_specification != self.item.specification:
            self.item.specification = new_specification

        # Change to saved
        self.unsaved_changes = False

    def reset_fields(self):
        self.nameInput.clear()
        self.skuInput.clear()
        self.quantitySpinBox.clear()
        self.specificationInput.clear()
        self.categoryInput.clear()
        self.populate_fields()

    def discard_changes(self):
        self.debug_logger.debug("discarding changes...")

        if self.unsaved_changes:
            if show_yes_no_dialog(self,
                                  title='discard changes',
                                  ):

                self.reject()  # Discard changes and close
        else:
            self.reject()  # No unsaved changes, just close the dialog

class EditItemDialog(BaseItemDialog):
    def __init__(self, item: Item, parent=None):
        super().__init__(item, parent)
        self.populate_fields()
        self.setWindowTitle(f"Editing item: {item.name}")

class AddItemDialog(BaseItemDialog):
    def __init__(self, item: None = None, parent=None):
        super().__init__(item, parent)
        self.setWindowTitle("Add new item")

    def get_new_item(self):
        if self.result() == QtWidgets.QDialog.DialogCode.Accepted:
            return self.item 
        else: 
            return None


