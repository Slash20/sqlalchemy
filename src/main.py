import os
import sys
from queries.orm import SyncORM

# sys.path.insert(1, os.path.join(sys.path[0], '..'))

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
