from PyQt6 import QtCore
from tech_cache.commons.database_manager import DatabaseManager
from tech_cache.config.app_config import AppConfig

class InventoryTableModel(QtCore.QAbstractTableModel):
    def __init__(self, db_manager: DatabaseManager, config: AppConfig):
        super(InventoryTableModel, self).__init__()
        self.db_manager = db_manager
        self.config = config
        self.items = self.db_manager.get_all_items()
        self.sortable_columns = {0, 1, 2, 3}

    def refresh_view(self):
        """gets latest database entries, notifies view and redraws tables fields"""
        self.items = self.db_manager.get_all_items()

        
        # TODO: use and row specifier and update only that item
        # instead of all of them!
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def get_item(self, index):
        if index.isValid():
            return self.items[index.row()]
        else:
            return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Builtin method
        Defines table view count of rows aka how many item rows to draw.
        """
        return len(self.items)

    def columnCount(self, parent=QtCore.QModelIndex()):
        """Builtin method
        Defines how many columns to draw.
        """
        return len(self.config.table_headers)

    def data(self, index, role):
        """populates each row and column with coresponding data field"""
        if not index.isValid():
            return None
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None

        item = self.items[index.row()]
        column = index.column()
        try:
            return item[column]
        except ValueError:
            return None

    def sort(self, column: int, order) -> None:
        """column sorting functionility"""
        if column in self.sortable_columns:
            self.layoutAboutToBeChanged.emit()

            self.items.sort(key=lambda item: item[column], 
                        reverse=(order == QtCore.Qt.SortOrder.DescendingOrder))

            self.layoutChanged.emit()

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int):
        """Sets header names for each column in the table view"""
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == QtCore.Qt.Orientation.Horizontal:
            headers = self.config.table_headers 
            if section <= len(headers) - 1:
                return headers[section]

        return None

