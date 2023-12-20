from typing import Any, List
from datetime import datetime
from uuid import uuid4

class Item:
    """Represents rows in tableview """
    def __init__(self, **kwargs): 
        self.id:str = str(kwargs.get('id', uuid4())) # for in database  data integrity
        self._name:str = kwargs.get('name', "")
        self.category:str = kwargs.get('category', "")
        self._quantity:int = kwargs.get('quantity', 0)
        self.sku:str = kwargs.get('sku', "") # TODO: Gen SKU
        self.specification:str = kwargs.get('specification', "")
        self.created_at:str = kwargs.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.updated_at:str = kwargs.get('updated_at',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def name(self):
        """The name property."""
        return self._name

    @name.setter
    def name(self, value):
        if value == "":
            raise ValueError("Mandatory name field can't be empty")
        self._name = value

    @property
    def quantity(self):
        """The quantity property."""
        return self._quantity

    @quantity.setter
    def quantity(self, value:int):
        if not isinstance(value, int):
            raise ValueError("Quantity must be an integer")

        if value < 0:
            raise ValueError("Quantity cannot be negative")

        self._quantity = value

    def get_fields(self) -> List[Any]:
        """Item fields to display"""
        fields = []
        fields.append(self.sku)
        fields.append(self.name)
        fields.append(self.category)
        fields.append(self.quantity)
        fields.append(self.specification)
        return fields

    def __getitem__(self, column_index):
        if column_index == 0:
            return self.sku
        elif column_index == 1:
            return self.name
        elif column_index == 2:
            return self.category
        elif column_index == 3:
            return self.quantity
        elif column_index == 4:
            return self.specification
        else:
            raise IndexError("Invalid column index")

        
