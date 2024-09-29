import os
import sqlalchemy
import databases
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
