from src.DB.database import Base, engine
from src.DB.models import Create_User

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
