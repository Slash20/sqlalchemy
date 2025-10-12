import os
import sys
from queries.orm import SyncORM
from queries.core import SyncCore
sys.path.insert(1, os.path.join(sys.path[0], '..'))

SyncORM.create_tables()
SyncORM.insert_data()
SyncCore.select_workers()
SyncCore.update_workers()
