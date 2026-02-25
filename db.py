from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase



class Base(DeclarativeBase):
    pass

engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/p3")

session = sessionmaker(autoflush=False, bind= engine)

def get_db():
    db = session()
    try: 
        yield db
    finally:
        db.close()