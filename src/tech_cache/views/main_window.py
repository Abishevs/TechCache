import logging
from PyQt6 import QtWidgets, QtCore, QtGui

from tech_cache.config.app_config import AppConfig
from tech_cache.models.inventory_table_model import InventoryTableModel
from tech_cache.commons.database_manager import DatabaseManager
from tech_cache.commons.export_manager import ExportManager
from tech_cache.ui.ui_main_window import Ui_MainWindow
from tech_cache.utils.logger_conf import LoggerConfig
from tech_cache.views.edit_item_dialog import AddItemDialog, EditItemDialog
from tech_cache.themes.styles import stylesheet_template, colors

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Entry point of the application

    Initilises all componenets and listens to signals
    Executes user signals.
    """
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # setup loggers
        self.error_logger = logging.getLogger(LoggerConfig.ERROR_LOGGER)
        self.action_logger = logging.getLogger(LoggerConfig.ACTION_LOGGER)

        # setup
        self.init_add_item_button()         
        self.setupUi(self)                  
        self.setWindowTitle('Tech Cache')   
        self.showFullScreen()
        self.apply_stylesheet()

        # init componenents, config, db etc
        self.init_components()

        # setup filtering proxy for tableview
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(-1) # search all columns

        # set views
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # self.tableView.setModel(self.model)
        self.tableView.setModel(self.filter_proxy_model)
        self.tableView.setSortingEnabled(True)

        # set signals and slots
        self.action_export_as.triggered.connect(self.handle_export_action)
        self.action_import.triggered.connect(self.handle_import_action)
        self.tableView.doubleClicked.connect(self.onRowDoubleClicked)
        self.add_item_button.clicked.connect(self.on_add_button_clicked)
        self.search_input.textChanged.connect(self.filter_proxy_model.setFilterRegularExpression)
        
        # update positons
        self.update_button_position()

    def init_components(self):
        """
        Creates config
        Connects to database
        creates model for item table view
        creates export managaer
        """
        self.config = AppConfig()
        self.database = DatabaseManager()
        self.model = InventoryTableModel(self.database, self.config)
        self.export_manager = ExportManager(self.database)

    def apply_stylesheet(self):
        """Retrieves stylesheet and populates entries with current colors"""
        stylesheet = stylesheet_template.format(**colors)
        self.setStyleSheet(stylesheet)
    
    def init_add_item_button(self):
        """Creates floating add item button"""
        button_size = 40
        self.add_item_button = QtWidgets.QPushButton(self)
        self.add_item_button.setObjectName("addItemButton")
        self.add_item_button.setFixedSize(button_size, button_size)
        self.add_item_button.setStyleSheet(
                f"border-radius: {button_size // 2}px;"
                )
        self.add_item_button.setText("+")
        self.add_item_button.setCursor(QtGui.QCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
            ))
        self.add_item_button.show()

    def update_button_position(self):
        """
        Updates floating buttons position 
        called on self.resizeEvent(self)
        """
        button_size = self.add_item_button.size()
        margin = 40 

        # calculate the new position
        x = self.width() - button_size.width() - margin
        y = self.height() - button_size.height() - margin - 20

        # position the button and set it on top of other elements
        self.add_item_button.setGeometry(QtCore.QRect(
            x, 
            y, 
            button_size.width(), 
            button_size.height()
            ))
        self.add_item_button.raise_()

    def on_add_button_clicked(self):
        """
        Signal to open add item dialog. 

        When widget returns positive. New item obj is extracted and
        created and then added to the database.

        Else changes are aborted
        """
        add_dialog = AddItemDialog(parent=self)
        if add_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_item = add_dialog.get_new_item()
            if new_item:
                self.database.add_item(new_item)
                self.model.refresh_view()

    def resizeEvent(self, event):
        """Builtin method

        Listener for window resizing. Floating button is updated here to
        ensure it's relative position.
        """

        self.update_button_position()
        super().resizeEvent(event)

    def onRowDoubleClicked(self, index):
        """
        Signal to open an Edit item dialog.

        Retrieves index of row item that was double clicked. Item is
        then retrieved from model by it's index to populate fields
        within edit item dialog.
        """

        proxy_index = self.filter_proxy_model.mapToSource(index)
        item = self.model.get_item(proxy_index)
        if item:
            edit_dialog = EditItemDialog(item, self)
            edit_dialog.setModal(True)
            if edit_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.database.update_item(item)
                self.model.refresh_view()
                self.action_logger.info(f"Edited item with id: {item.id}")
        else:
            # TODO: THROW an error which shouldnt even happen lol
            self.error_logger.error("Can't find clicked item")

    def closeEvent(self, event):
        """Builtin method 

        Acts as bridge to open "are you sure?" dialog before closing the
        application to save changes, close db connection. Or if that was an
        accident to be able to not close the window.
        """

        reply = QtWidgets.QMessageBox.question(
                self, 
                'Message',
                "Are you sure to quit?", 
                QtWidgets.QMessageBox.StandardButton.Yes 
                | QtWidgets.QMessageBox.StandardButton.No, 
                QtWidgets.QMessageBox.StandardButton.No
                )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            # TODO: clean up
            event.accept()
        else:
            event.ignore()

    
    def handle_export_action(self):
        """Signal to open export as view dialog.

        Retrieve the name of the file, if file name was provided prepare
        csv file and save it with state of the current model.
        """
        file_name = self.export_as_view()
        if file_name:
            try:
                self.export_manager.save_data_as_csv(file_name)
                self.action_logger.info(f"Exported db with filename{file_name}")
            except Exception as e:
                self.error_logger.error(f"Error exporting {e}") 

    def export_as_view(self) -> str|None:
        """Opens export as dialog

        Returns: filename(str) or None
        """

        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            "Save File",
                                                            "",
                                                            "CSV Files (*.csv)"
                                                            )

        return file_name

    def handle_import_action(self):
        file_name = self.import_view()
        if file_name:
            try:

                self.model.layoutAboutToBeChanged.emit()
                self.action_logger.info("Importing items")
                self.export_manager.import_as_csv(file_name)
                self.model.layoutChanged.emit()
                self.model.refresh_view()
            
            except Exception as e:
                self.error_logger.error("Failed importing items")
                QtWidgets.QMessageBox.critical(self,
                                              "Mandatory Field", 
                                              str(e))

    def import_view(self) -> str|None:
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                             "Import items",  # Dialog title
                                                             "",           
                                                             "CSV Files (*.csv)") 
        if file_name:
            return file_name 
        return None
