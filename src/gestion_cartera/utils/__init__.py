from dotenv import load_dotenv
load_dotenv('.env')
import os
from sqlalchemy import create_engine

class DatabaseConnection:
    def _get_env(self, stream: str) -> tuple[str]:
        if stream == 'upstream':
            user = os.getenv('DB_UPSTREAM_USER')
            password = os.getenv('DB_UPSTREAM_PASSWORD')
            server = os.getenv('DB_UPSTREAM_SERVER')
            database = os.getenv('DB_UPSTREAM_DATABASE')
            return user, password, server, database

        if stream == 'downstream':
            server = os.getenv('DB_DOWNSTREAM_SERVER')
            database = os.getenv('DB_DOWNSTREAM_DATABASE')
            return None, None, server, database 
            
    def _get_conn(self, stream:str, user, password, server, database) -> str:
        if stream == 'upstream':
            conn = f'mssql+pyodbc://{user}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
            return conn

        if stream == 'downstream':
            conn = f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
            return conn
    
    def _get_engine(self, conn:str):
        return create_engine(conn)
    
    def engine(self, stream:str):
        user, password, server, database = self._get_env(stream)
        conn = self._get_conn(stream, user, password, server, database)
        engine = self._get_engine(conn)
        return engine


if __name__ == '__main__':

    database_connection = DatabaseConnection()
    engine_upstream = database_connection.engine('downstream')
    print(engine_upstream)