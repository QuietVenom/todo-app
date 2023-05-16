from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:virgia@127.0.0.1:3306/todoapp"
SQLALCHEMY_DATABASE_URL = "postgresql://gmlnfzhu:FJpxZv4ZxENGiKgR0JgbtLOLdg56S8gQ@mahmud.db.elephantsql.com/gmlnfzhu"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL  # [sqlite], connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
