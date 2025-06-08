from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os




load_dotenv()

#retrive the postgres credentials from .env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

#database URL
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

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