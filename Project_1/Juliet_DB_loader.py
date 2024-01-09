from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    folder_name = Column(String)

    subfolders = relationship('SubFolder', backref='folder', cascade='all, delete-orphan')

class SubFolder(Base):
    __tablename__ = 'subfolders'

    id = Column(Integer, primary_key=True)
    parent_folder_id = Column(Integer, ForeignKey('folders.id'))
    folder_name = Column(String)

    test_cases = relationship('TestCase', backref='subfolder', cascade='all, delete-orphan')

class TestCase(Base):
    __tablename__ = 'test_cases'

    id = Column(Integer, primary_key=True)
    subfolder_id = Column(Integer, ForeignKey('subfolders.id'))  # This is the foreign key
    file_name = Column(String)
    file_extension = Column(String)
    file_content = Column(Text)
    cwe = Column(String)
    vulnerability_location = Column(String)

engine = create_engine('sqlite:///C:\\Users\\Andrew\\Desktop\\Juliet.db', echo=False, connect_args={'check_same_thread': False})

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base.metadata.create_all(engine)

    

