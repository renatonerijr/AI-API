from sqlmodel import SQLModel, Session, create_engine

DB_URL = "postgresql+psycopg2://postgres:postgres@db:5432/api_db"
engine = create_engine(DB_URL)

SQLModel.metadata.create_all(engine)

# Dependency
def get_session():
    with Session(engine) as session:
        yield session
