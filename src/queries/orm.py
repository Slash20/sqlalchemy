from database import async_engine, sync_engine, session_factory, Base
from models import WorkersORM


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        sync_engine.echo = True
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        worker_bobr = WorkersORM(username="Bobr")
        worker_wolf = WorkersORM(username="Wolf")
        with session_factory() as session:
            session.add_all([worker_bobr, worker_wolf])
            session.commit()