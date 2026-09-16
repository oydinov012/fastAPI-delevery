from click import pass_obj
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

db_owner = 'ilyos'
password = 1234
db_name = 'fastapi'
engine = create_engine(f"postgresl://{db_owner}:{password}@localhost/{db_name}",echo=True)



Base = declarative_base()

Session = sessionmaker()