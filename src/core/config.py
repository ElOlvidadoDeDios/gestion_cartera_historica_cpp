import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    PERIODO = os.getenv("PERIODO").strip()

    @staticmethod
    def get_source_connection():
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('SRC_SERVER')};"
            f"DATABASE={os.getenv('SRC_DATABASE')};"
            f"UID={os.getenv('SRC_UID')};"
            f"PWD={os.getenv('SRC_PWD')};"
        )
        return pyodbc.connect(conn_str)

    @staticmethod
    def get_dwh_connection():
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DWH_SERVER')};"
            f"DATABASE={os.getenv('DWH_DATABASE')};"
            f"UID={os.getenv('DWH_UID')};"
            f"PWD={os.getenv('DWH_PWD')};"
        )
        return pyodbc.connect(conn_str)
