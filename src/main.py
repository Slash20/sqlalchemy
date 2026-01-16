from queries.orm import SyncORM
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

SyncORM.create_tables()
SyncORM.insert_workers()
SyncORM.insert_resumes()
SyncORM.select_workers()
SyncORM.update_workers()
SyncORM.avg_salary()
SyncORM.select_workers_lazy_relationship()
SyncORM.select_workers_joined_relationship()
SyncORM.select_workers_selectin_relationship()
SyncORM.select_workers_with_condition_relationship()

def create_fastapi_app():

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/workers")
    async def get_workers():
        workers = SyncORM.convert_workers_to_dto()
        return workers

    return app

app = create_fastapi_app()