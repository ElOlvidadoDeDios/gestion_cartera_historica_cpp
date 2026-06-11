import pandas as pd
import logging
from src.core.config import DBConfig
from src.core.constants import QUERY_EXTRACT_STOCK, QUERY_EXTRACT_FLOW


class Extractor:
    @staticmethod
    def extract_stock_mensual() -> pd.DataFrame:
        periodo = DBConfig.PERIODO
        logging.info(
            f"Extrayendo Stock Mensual de TRANSACMIF para el Periodo: {periodo}..."
        )
        with DBConfig.get_source_connection() as conn:
            # Uso seguro de parámetros nativos de pyodbc para evitar inyecciones
            df = pd.read_sql(QUERY_EXTRACT_STOCK, conn, params=[periodo])
        logging.info(f"Extraccion de Stock completada. Registros: {len(df)}")
        return df

    @staticmethod
    def extract_flow_diario() -> pd.DataFrame:
        periodo = DBConfig.PERIODO
        logging.info(
            f"Extrayendo Flujo Diario de TRANSACMIF para el Periodo: {periodo}..."
        )
        with DBConfig.get_source_connection() as conn:
            df = pd.read_sql(QUERY_EXTRACT_FLOW, conn, params=[periodo])
        logging.info(f"Extraccion de Flujo completada. Registros: {len(df)}")
        return df
