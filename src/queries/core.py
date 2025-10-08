from database import async_engine, sync_engine
from sqlalchemy import text, insert
from models import metadata_obj, workers_table

# async def async_get_db():
#     async with async_engine.connect() as conn:
#         res = await conn.execute(text("SELECT VERSION()"))
#         print(f"{res.first()=}")


def sync_get_db():
    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.first()=}")


def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True


def insert_data():
    with sync_engine.connect() as conn:
        # stmt = """INSERT INTO workers (username) VALUES
        # ('Bobr'),
        # ('Wolf');
        # """
        stmt = insert(workers_table).values(
            [
                {"username": "Bobr"},
                {"username": "Wolf"},
            ]
        )
        conn.execute(stmt)
        conn.commit()












