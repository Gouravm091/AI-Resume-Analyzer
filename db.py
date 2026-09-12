from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("TIDB_USERNAME")
password = os.getenv("TIDB_PASSWORD")
host = os.getenv("TIDB_HOST")

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:4000/test"


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ca": r"C:\Users\HP\Downloads\isrgrootx1.pem"
        }
    }
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()