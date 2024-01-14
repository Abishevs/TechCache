from dataclasses import dataclass
from typing import Tuple

@dataclass
class AppConfig:
    table_headers: Tuple = ("Checkbox", "SKU", "Name", "Category", "Quantity", "Specification")
