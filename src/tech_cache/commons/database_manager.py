from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from tech_cache.models.item import Base, Item

class DatabaseManager:
    """Handles database connection and data persitance
    Idea is that an instance of this class is passed to
    models, so that views can then interpret and draw
    data.
    """
    def __init__(self, db_url="sqlite:///test.db"):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine) 
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def get_item(self, item_id:int) -> (Item | None):
        with self.get_session() as session:
            item = session.query(Item).filter(Item.id == item_id).one_or_none()
            return item if item else None

    def add_item(self, item: Item) -> bool:
        with self.get_session() as session:
            try:
                session.add(item)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error: {e}")
                return False

    def update_item(self, item:Item) -> bool:
        with self.get_session() as session:
            try:
                session.merge(item)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error: {e}")
                return False

    
    def delete_item(self, item:Item) -> bool:
        with self.get_session() as session:
            try:
                session.delete(item)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error: {e}")
                return False
    

    def get_all_items(self) -> List[Item]:
        with self.get_session() as session:
            items = session.query(Item).all()
            for item in items:
                item.is_checked = False
            return items
