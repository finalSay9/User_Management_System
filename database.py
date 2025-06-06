from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker



#database URL
DATABASE_URL = "postgresql://postgres:evan1234@localhost:5432/evan1"

#create sqlalchemy engine
engine = create_engine(DATABASE_URL, echo=True)

#Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#db base
Base = declarative_base()

#dependency to get a db session
def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creating all tables in database
Base.metadata.create_all(bind=engine)