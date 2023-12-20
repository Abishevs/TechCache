from dataclasses import dataclass
from typing import Tuple

@dataclass
class AppConfig:
    table_headers: Tuple = ("SKU", "Name", "Category", "Quantity", "Specification")
