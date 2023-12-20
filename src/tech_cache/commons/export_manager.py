
import csv
from tech_cache.commons.database_manager import DatabaseManager
from tech_cache.models.item import Item

class ExportManager:
    def __init__(self, db_manager: DatabaseManager) -> None:
        # parent type Any to remove annoying warnings, as parent can be any...
        self.db_manager = db_manager

    def export_as(self, file_name):
        if file_name:
            self.save_data_as_csv(file_name)

    def save_data_as_csv(self, file_name):
        with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            # write headers
            writer.writerow(['SKU',
                             'Name', 
                             'Category',
                             'Quantity',
                             'specification',
                             ])
            # write row, from all fields
            for item in self.db_manager.get_all_items():
                writer.writerow(item.get_fields())

    def import_as_csv(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            headers = [header.lower() for header in next(csv.reader(file))]

            reader = csv.DictReader(file, fieldnames=headers)
            for row in reader:
                new_item = Item(sku = row.get('sku'),
                                name = row.get('name'),
                                category = row.get('category'),
                                quantity = row.get('quantity'),
                                specification = row.get('specification')
                                )
                self.db_manager.add_item(new_item)

        # raise NotImplementedError("Import doesn't yet work!")
