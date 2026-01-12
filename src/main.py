import os
import sys
from queries.orm import SyncORM
from queries.core import SyncCore
sys.path.insert(1, os.path.join(sys.path[0], '..'))

SyncORM.create_tables()
SyncORM.insert_workers()
SyncORM.insert_resumes()
SyncORM.select_workers()
SyncORM.update_workers()
