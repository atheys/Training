"""DWH engine module"""

# module imports
from code.utils.params import *
from sqlalchemy import create_engine, event

# connection
connection = f"{SQL}+{PACKAGE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?driver={DRIVER}"
# DWH engine
dwh_engine = create_engine(connection)


@event.listens_for(dwh_engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True
