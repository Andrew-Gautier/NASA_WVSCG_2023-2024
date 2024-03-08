import rcmpy
from Juliet_DB_loader import TestCase, sessionmaker, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, create_engine, event
# Create sessions for Juliet1.0 and 2.0
Session1 = sessionmaker(bind=engine)
Juliet1 = Session1()

engine2 = create_engine('sqlite:///C:\\Users\\Andrew\\Desktop\\Juliet2.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()

Session2 = sessionmaker(bind=engine2)
Juliet2 = Session2()
# Create new schema 

class Cases(Base):
    __tablename__ = 'Cases'
    
    model_id = Column(Integer, primary_key =True)
    file_name = Column(String, primary_key=True)
    file_content = Column(Text)
    cwe = Column(String)
    vulnerability_location = Column(String)

Base.metadata.create_all(engine2)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()



# Helper Functions

# Split into train, test, validate, supplemental, and other 
def assign_id(file_count, split=[60, 20, 10, 10]):
    total_percentage = sum(split)
    if total_percentage != 100:
        raise ValueError("Invalid split percentages. The total must be 100.")

    current_id = 0
    assigned_ids = []

    for percentage in split:
        num_files = int(file_count * (percentage / 100))
        assigned_ids.extend([current_id] * num_files)
        current_id += 1

    return assigned_ids


# Pull values from old database, clean then, and insert into new database. 
cases = Juliet1.query(TestCase).all()
model_ids = assign_id(len(cases))

for model_id, case in zip(model_ids, cases):
    # Clean the code
    code = rcmpy.keep_newlines(case.file_content)
    # Insert into the new database
    Juliet2.add(Cases(
        model_id=model_id,
        file_name=case.file_name,
        vulnerability_location=case.vulnerability_location,
        cwe=case.cwe,
        file_content=code
    ))

# Commit the changes to the new database
Juliet2.commit()



