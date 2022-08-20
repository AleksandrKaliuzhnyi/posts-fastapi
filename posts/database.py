from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from posts.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:" \
                          f"{settings.database_password}@{settings.database_hostname}:" \
                          f"{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi-posts',
#                             user='postgres', password='12345', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
# except Exception as error:
#     print(f"Connecting to db failed with error {error}")