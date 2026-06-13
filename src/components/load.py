import pandas as pd
import logging
from src.core.config import DBConfig
from src.core.constants import QUERY_LOAD_ASESOR, QUERY_LOAD_STOCK, QUERY_LOAD_FLOW


class Loader:
    @staticmethod
    def load_dim_asesor(df: pd.DataFrame):
        if df.empty:
            return
        logging.info(
            f"Actualizando {len(df)} registros en {DBConfig.TBL_DWH_ASESOR}..."
        )

        # OPTIMIZACIÓN: Creación masiva de parámetros usando zip nativo (Evita la lentitud de iterrows)
        params = list(
            zip(
                df["CodAsesor"],
                df["Periodo"],
                df["AsesorNombresApellidos"],
                df["Cargo"],
                df["CodAgencia"],
                df["AsesorNombresApellidos"],
                df["Cargo"],
                df["CodAgencia"],
            )
        )

        with DBConfig.get_dwh_connection() as conn:
            with conn.cursor() as cursor:
                cursor.fast_executemany = True
                cursor.executemany(QUERY_LOAD_ASESOR, params)
                conn.commit()
        logging.info("Dimension dim_asesor sincronizada con exito.")

    @staticmethod
    def load_stock_mensual(df: pd.DataFrame):
        if df.empty:
            return
        logging.info(f"Actualizando {len(df)} registros en {DBConfig.TBL_DWH_STOCK}...")

        # OPTIMIZACIÓN: Estructuración de tuplas duplicadas para el MERGE en microsegundos
        params = list(
            zip(
                df["Periodo"],
                df["CodAsesor"],
                df["CodAgencia"],
                df["SaldoTotalReal"],
                df["SaldoMora9Real"],
                df["SaldoMora31Real"],
                df["SaldoMora150Real"],
                df["NumeroSociosReal"],
                df["NumeroSociosAnterior"],
                df["CodAgencia"],
                df["SaldoTotalReal"],
                df["SaldoMora9Real"],
                df["SaldoMora31Real"],
                df["SaldoMora150Real"],
                df["NumeroSociosReal"],
                df["NumeroSociosAnterior"],
                df["Varios"],
                df["TEA"],
            )
        )

        with DBConfig.get_dwh_connection() as conn:
            with conn.cursor() as cursor:
                cursor.fast_executemany = True
                cursor.executemany(QUERY_LOAD_STOCK, params)
                conn.commit()
        logging.info("Tabla fct_stock_mensual actualizada incrementalmente.")

    @staticmethod
    def load_flow_diario(df: pd.DataFrame):
        if df.empty:
            return
        logging.info(f"Actualizando {len(df)} registros en {DBConfig.TBL_DWH_FLOW}...")

        # OPTIMIZACIÓN: Alta velocidad de procesamiento para el volumen transaccional diario
        params = list(
            zip(
                df["Fecha"],
                df["CodAsesor"],
                df["CodAgencia"],
                df["SaldoCarteraReal"],
                df["MontoColocacionReal"],
                df["NumColocacionesReal"],
                df["MontoRepagoReal"],
                df["CodAgencia"],
                df["SaldoCarteraReal"],
                df["MontoColocacionReal"],
                df["NumColocacionesReal"],
                df["MontoRepagoReal"],
            )
        )

        with DBConfig.get_dwh_connection() as conn:
            with conn.cursor() as cursor:
                cursor.fast_executemany = True
                cursor.executemany(QUERY_LOAD_FLOW, params)
                conn.commit()
        logging.info("Tabla fct_flow_diario actualizada incrementalmente sin perdidas.")
