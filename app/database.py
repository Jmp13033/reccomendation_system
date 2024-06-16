from sqlalchemy import create_engine, Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# db url 
DATABASE_URL = "postgresql://postgres:postgres@localhost:5434/books"

# orm 
Base = declarative_base()
# create the db engine 
engine = create_engine(DATABASE_URL)

# Local Session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# set up model to interact with Database
class User(Base):
 __tablename__ = "users"
 id = Column(Integer, primary_key=True, index=True, autoincrement=True)
 name = Column(String, index=True)
 email = Column(String, unique=True, index=True)
 is_active = Column(Boolean, default=True)
Base.metadata.create_all(bind=engine)




# pg_dump -h <hostname> -U <username> -d <database_name> -t <table_name> -Fc -f <output_file>
# pg_dump -h localhost -U postgres -d books -p 5434 -t book -Fc -f book.sql

