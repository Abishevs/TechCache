from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from tech_cache.models.item import Base, Item

# import sqlite3
from typing import List


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


    def get_item(self, item_id:int):
        with self.get_session() as session:
            return session.query(Item).filter(Item.id == item_id).one_or_none()

    def add_item(self, item: Item):
        session = self.get_session()
        try:
            session.add(item)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    def update_item(self, item_id: int):

        with self.get_session() as session:
            try:
                item = session.query(Item).filter(Item.id == item_id).one_or_none()
                
                if item:
                    session.delete(item)
                    session.commit()
                else:
                    print(f"Item with ID {item_id} not found.")
            except SQLAlchemyError as e:
                session.rollback()
                raise e
    
    def delete_item(self, item_id: int):
        session = self.get_session()
        with self.get_session() as session:
            try:
                item = session.query(Item).filter(Item.id == item_id).one_or_none()
                
                if item:
                    session.delete(item)
                    session.commit()
                else:
                    print(f"Item with ID {item_id} not found.")

            except SQLAlchemyError as e:
                session.rollback()
                raise e
    
    def get_all_items(self) -> List[Item]:
        with self.get_session() as session:
            return list(session.query(Item))
