from typing import Any
from typing import List
from typing import Optional
from datetime import datetime
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column()
    specification: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, 
                 name:str = "",
                 sku:str = "",
                 category:str = "",
                 quantity:int = 0,
                 specification:str = "",
                 is_checked = False,
                 ):

        self.name = name
        self.sku = sku
        self.category = category
        self.quantity = quantity
        self.specification = specification
        self.is_checked = is_checked

    def __repr__(self) -> str:
        return f"Item(name={self.name!r}, category={self.category!r}, quantity={self.quantity!r})"

    def __getitem__(self, column_index):
        if column_index == 0:
            return self.is_checked
        elif column_index == 1:
            return self.sku
        elif column_index == 2:
            return self.name
        elif column_index == 3:
            return self.category
        elif column_index == 4:
            return self.quantity
        elif column_index == 5:
            return self.specification
        else:
            raise IndexError("Invalid column index")

    def get_fields(self) -> List[Any]:
        """Item fields to display"""
        fields = []
        fields.append(self.is_checked)
        fields.append(self.sku)
        fields.append(self.name)
        fields.append(self.category)
        fields.append(self.quantity)
        fields.append(self.specification)
        return fields
