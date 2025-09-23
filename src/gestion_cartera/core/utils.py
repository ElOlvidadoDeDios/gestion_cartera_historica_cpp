from dotenv import load_dotenv
load_dotenv('.env')
import os
from sqlalchemy import create_engine
import yaml
from ensure import ensure_annotations
import yaml
from box.exceptions import BoxValueError
from box import ConfigBox
from pathlib import Path
from gestion_cartera.core.constants import *

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


def load_config(path_config: str = 'conf/config.yaml'):
    with open(path_config, 'r') as f:
        return yaml.safe_load(f)


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml, 'r') as file_yaml:
            content = yaml.safe_load(file_yaml)
            if not content:
                raise ValueError('YAML file is empty.')
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError('YAML file is empty.')
    except Exception as e:
        raise e


if __name__ == '__main__':
    config = read_yaml(PATH_CONFIG)
    print(config.table)