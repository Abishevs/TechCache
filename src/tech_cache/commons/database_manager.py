import sqlite3
from typing import List
from tech_cache.models.item import Item

class DatabaseManager:
    """Handles database connection and data persitance
    Idea is that an instance of this class is passed to
    models, so that views can then interpret and draw
    data.
    """
    def __init__(self):
        self.con: sqlite3.Connection
        self.cur: sqlite3.Cursor
        self.db_name = "test.db"
        self.connect()

    def connect(self):
        """Open db connection when you open application"""
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self.init_db()

    def close(self):
        """close db before closing application"""
        self.con.close()

    def init_db(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                name TEXT,
                category TEXT,
                quantity INTEGER,
                sku TEXT,
                specification TEXT,
                created_at TEXT,
                updated_at TEXT
        );
        """
        self.execute_query(create_table_query)

    def execute_query(self, query:str, data: tuple | None=None):
        with self.con:
            if data:
                self.cur.execute(query, data)
            else:
                self.cur.execute(query)

    def get_item(self, uid):
        query = """
        SELECT 
                id,
                name, 
                category,
                quantity,
                sku, 
                specification,
                created_at,
                updated_at
        FROM items
        WHERE id = ?;
        """
        self.execute_query(query, (uid,))
        db_item = self.cur.fetchone()
        new_item = Item(
                    id=db_item[0],
                    name=db_item[1],
                    category=db_item[2],
                    quantity=db_item[3],
                    sku=db_item[4],
                    specification=db_item[5],
                    created_at=db_item[6],
                    updated_at=db_item[7]
                        )
        return new_item

    def add_item(self, item: Item):
        query = """
        INSERT INTO items (
                id,
                name, 
                category,
                quantity,
                sku, 
                specification,
                created_at,
                updated_at
                ) 
        VALUES(?, ?, ?, ?, ?, ?, ?, ?);
        """
        data = (str(item.id),
                item.name,
                item.category,
                item.quantity,
                item.sku,
                item.specification,
                item.created_at,
                item.updated_at,
                )
        self.execute_query(query, data)

    def update_item(self, item: Item):
        query = """
        UPDATE items 
        SET name = ?,
            category = ?,
            quantity = ?,
            sku = ?, 
            specification = ?,
            updated_at = ?
        WHERE id = ?;
        """
        data = (item.name, 
                item.category, 
                item.quantity,
                item.sku,
                item.specification,
                item.updated_at,

                item.id)
        self.execute_query(query, data)
    
    def delete_item(self, uid:str):
        query = "DELETE FROM items WHERE id = ?;"
        self.execute_query(query, (uid,))
    
    def get_all_items(self) -> List[Item]:
        query = """
        SELECT 
                id,
                name, 
                category,
                quantity,
                sku, 
                specification,
                created_at,
                updated_at
        FROM items;
        """
        self.execute_query(query)
        db_items = self.cur.fetchall()
        items = []
        for row in db_items:
            # follows query parameter order
            new_item = Item(
                    id=row[0],
                    name=row[1],
                    category=row[2],
                    quantity=row[3],
                    sku=row[4],
                    specification=row[5],
                    created_at=row[6],
                    updated_at=row[7]
                        )
            items.append(new_item)
        return items

