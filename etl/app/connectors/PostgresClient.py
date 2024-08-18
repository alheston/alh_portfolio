from sqlalchemy import create_engine, Table, MetaData, text
from sqlalchemy.engine import URL, CursorResult
from sqlalchemy.dialects import postgresql
from sqlalchemy import func
import pandas as pd



class PostgresClient:
    """

    A client for interacting with postgres 16

    """

    def __init__(
            self,
            host_name: str,
            database_name: str,
            username: str,
            password: str,
            port: str
    ):
        self.host_name = host_name,
        self.database_name = database_name,
        self.username = username,
        self.password = password,
        self.port = port

        connection_url = URL.create(
            drivername = "postgresql+pg8000",
            username = username,
            password = password,
            host = host_name,
            port = port,
            database = database_name


        )
        print(connection_url)

        self.engine = create_engine(connection_url)

    def insert(self, data: list[dict], table: Table, metadata: MetaData) -> None:
        metadata.create_all(self.engine)
        insert_statement = postgresql.insert(table).values(data)
        with self.engine.connect() as conn:
            conn.execute(insert_statement)
            conn.commit()
        # self.engine.execute(insert_statement)
    
    def drop_table(self, table_name: Table) -> None:
        with self.engine.connect() as conn:
            conn.execute(text(f"drop table if exists {table_name};"))
            conn.commit()
    
    def overwrite(self, data: list[dict], table: Table, metadata: MetaData) -> None:
        self.drop_table(table.name)
        self.insert(data=data, table=table, metadata=metadata)

    def upsert(self, data: list[dict], table: Table, metadata: MetaData) -> None:
        metadata.create_all(self.engine)
        key_columns = [
            pk_column.name for pk_column in table.primary_key.columns.values()
        ]
        print(f"Key columns: {key_columns}")  
        print(f"Data: {data}") 
        insert_statement = postgresql.insert(table).values(data)
        print(insert_statement)
        upsert_statement = insert_statement.on_conflict_do_update(
            index_elements = key_columns,
            set_ = {
                c.key: c for c in insert_statement.excluded if c.key not in key_columns
            },
        )
        print(f"Upsert statement: {upsert_statement}") 
        with self.engine.connect() as conn:
            conn.execute(upsert_statement)



        