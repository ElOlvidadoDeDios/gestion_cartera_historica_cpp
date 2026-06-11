import pandas as pd
import logging
from src.core.config import DBConfig
from src.core.constants import (
    QUERY_EXTRACT_ASESOR,
    QUERY_EXTRACT_STOCK,
    QUERY_EXTRACT_FLOW,
)


class Extractor:
    @staticmethod
    def extract_dim_asesor() -> pd.DataFrame:
        periodo = DBConfig.PERIODO
        logging.info(
            f"Extrayendo Asesores desde {DBConfig.VW_SRC_ASESOR} para el Periodo: {periodo}..."
        )
        with DBConfig.get_source_connection() as conn:
            df = pd.read_sql(QUERY_EXTRACT_ASESOR, conn, params=[periodo])
        logging.info(f"Extraccion de Asesores completada. Registros: {len(df)}")
        return df

    @staticmethod
    def extract_stock_mensual() -> pd.DataFrame:
        periodo = DBConfig.PERIODO
        logging.info(
            f"Extrayendo Stock Mensual desde {DBConfig.VW_SRC_STOCK} para el Periodo: {periodo}..."
        )
        with DBConfig.get_source_connection() as conn:
            df = pd.read_sql(QUERY_EXTRACT_STOCK, conn, params=[periodo])
        logging.info(f"Extraccion de Stock completada. Registros: {len(df)}")
        return df

    @staticmethod
    def extract_flow_diario() -> pd.DataFrame:
        periodo = DBConfig.PERIODO
        logging.info(
            f"Extrayendo Flujo Diario desde {DBConfig.VW_SRC_FLOW} para el Periodo: {periodo}..."
        )
        with DBConfig.get_source_connection() as conn:
            df = pd.read_sql(QUERY_EXTRACT_FLOW, conn, params=[periodo])
        logging.info(f"Extraccion de Flujo completada. Registros: {len(df)}")
        return df
