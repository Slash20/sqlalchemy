from database import async_engine, sync_engine, session_factory
from models import metadata_obj, WorkersORM


def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True


def insert_data():
    worker_bobr = WorkersORM(username="Bobr")
    worker_wolf = WorkersORM(username="Wolf")
    with session_factory() as session:
        session.add_all([worker_bobr, worker_wolf])
        session.commit()