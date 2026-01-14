from database import async_engine, sync_engine, session_factory, Base
from models import WorkersORM, ResumeORM, Workload
from sqlalchemy import select, func, Integer, and_
from sqlalchemy.orm import joinedload, selectinload


class SyncORM:

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        # sync_engine.echo = True
        Base.metadata.create_all(sync_engine)
        # sync_engine.echo = True


    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_bobr = WorkersORM(username="Jack")
            worker_wolf = WorkersORM(username="Wolf")
            session.add_all([worker_bobr, worker_wolf])
            session.flush()
            session.commit()


    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkersORM)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")


    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkersORM, worker_id)
            worker_michael.username = new_username
            session.refresh(worker_michael)
            session.commit()


    @staticmethod
    def insert_resumes():
        with session_factory() as session:

            resume1 = ResumeORM(
                title="Python Developer", compensation=50000, workload=Workload.fulltime, worker_id=1
            )
            resume2 = ResumeORM(
                title="Java Developer", compensation=80000, workload=Workload.fulltime, worker_id=2
            )

            session.add_all([resume1, resume2])
            session.commit()

    @staticmethod
    def avg_salary(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_comp
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload;
        """
        with session_factory() as session:
            query = (
                select(
                    ResumeORM.workload,
                    func.avg(ResumeORM.compensation).cast(Integer).label("avg_comp"),
                )
                .select_from(ResumeORM)
                .filter(and_(
                    ResumeORM.title.contains(like_language),
                    ResumeORM.compensation > 40000,
                ))
                .group_by(ResumeORM.workload)
                .having(func.avg(ResumeORM.compensation) > 40000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)


    @staticmethod
    def select_workers_lazy_relationship():
        """
        Такой код будет плохим, если мы обращаемся ко ВСЕМ работникам и у КАЖДОГО забираем резюме.
        И тут возникает т.н. проблема N+1
        """
        with session_factory() as session:
            query = (
                select(WorkersORM)
            )

            res = session.execute(query)
            result = res.scalars().all()

            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)

    @staticmethod
    def select_workers_joined_relationship():
        """
        В данном случае будет создаваться big запрос с возможным повторением PK,
        поэтому надо вызывать unique (это чисто питновская штука, отсеивает повторяющиеся PK)
        Но такой запрос не подходит для связи 1-M, но подходит для M-1, 1-1
        """
        with session_factory() as session:
            query = (
                select(WorkersORM)
                .options(joinedload(WorkersORM.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)

    @staticmethod
    def select_workers_selectin_relationship():
        """
        Этот запрос работает для 1-M, M-M
        """
        with session_factory() as session:
            query = (
                select(WorkersORM)
                .options(selectinload(WorkersORM.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)