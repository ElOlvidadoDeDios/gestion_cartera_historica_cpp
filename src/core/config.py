import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    PERIODO = os.getenv("PERIODO", "202606").strip()

    # Vistas de Origen (TRANSACMIF)
    VW_SRC_ASESOR = os.getenv("VW_SRC_ASESOR", "dbo.vw_dwh_dim_asesor").strip()
    VW_SRC_STOCK = os.getenv("VW_SRC_STOCK", "dbo.vw_dwh_fct_stock_mensual").strip()
    VW_SRC_FLOW = os.getenv("VW_SRC_FLOW", "dbo.vw_dwh_fct_flow_diario").strip()

    # Tablas de Destino (DWH_Gestion_Cartera)
    TBL_DWH_ASESOR = os.getenv("TBL_DWH_ASESOR", "dbo.dim_asesor").strip()
    TBL_DWH_STOCK = os.getenv("TBL_DWH_STOCK", "dbo.fct_stock_mensual").strip()
    TBL_DWH_FLOW = os.getenv("TBL_DWH_FLOW", "dbo.fct_flow_diario").strip()

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
