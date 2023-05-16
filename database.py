from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:virgia@127.0.0.1:3306/todoapp"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:virgia@localhost:5433/TodoAppDatabase"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL #[sqlite], connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()
