from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
class Folder(Base):
    __tablename__ = 'folder'

    id = Column(Integer, primary_key=True)
    parent_folder_id = Column(Integer, ForeignKey('folder.id'))
    folder_name = Column(String)

    files = relationship('SourceCodeFile', backref='folder', cascade='all, delete-orphan')

class SourceCodeFile(Base):
    __tablename__ = 'source_code_file'

    file_id = Column(Integer, primary_key=True)
    folder_id = Column(Integer, ForeignKey('folder.id'))
    file_name = Column(String)
    file_extension = Column(String)
    file_content = Column(Text)

    manifests = relationship('Manifest', backref='source_code_file', cascade='all, delete-orphan')

class Manifest(Base):
    __tablename__ = 'manifest'

    manifest_id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('source_code_file.file_id'))
    sarif_content = Column(Text)

    vulnerabilities = relationship('Vulnerability', backref='manifest', cascade='all, delete-orphan')

class Vulnerability(Base):
    __tablename__ = 'vulnerability'

    vulnerability_id = Column(Integer, primary_key=True)
    manifest_id = Column(Integer, ForeignKey('manifest.manifest_id'))
    line_number = Column(Integer)
    vulnerability_type = Column(String)

engine = create_engine('sqlite:///C:\\Users\\Andrew\\Desktop\\code_analysis.db', echo=False, connect_args={'check_same_thread': False})

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base.metadata.create_all(engine)

