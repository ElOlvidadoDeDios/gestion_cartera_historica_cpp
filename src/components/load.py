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
        params = []
        for _, row in df.iterrows():
            params.append(
                (
                    row["CodAsesor"],
                    row["Periodo"],
                    row["AsesorNombresApellidos"],
                    row["Cargo"],
                    row["CodAgencia"],
                    row["AsesorNombresApellidos"],
                    row["Cargo"],
                    row["CodAgencia"],
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
        params = []
        for _, row in df.iterrows():
            params.append(
                (
                    row["Periodo"],
                    row["CodAsesor"],
                    row["CodAgencia"],
                    row["SaldoTotalReal"],
                    row["SaldoMora9Real"],
                    row["SaldoMora31Real"],
                    row["SaldoMora150Real"],
                    row["NumeroSociosReal"],
                    row["NumeroSociosAnterior"],
                    row["CodAgencia"],
                    row["SaldoTotalReal"],
                    row["SaldoMora9Real"],
                    row["SaldoMora31Real"],
                    row["SaldoMora150Real"],
                    row["NumeroSociosReal"],
                    row["NumeroSociosAnterior"],
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
        params = []
        for _, row in df.iterrows():
            params.append(
                (
                    row["Fecha"],
                    row["CodAsesor"],
                    row["CodAgencia"],
                    row["SaldoCarteraReal"],
                    row["MontoColocacionReal"],
                    row["NumColocacionesReal"],
                    row["MontoRepagoReal"],
                    row["CodAgencia"],
                    row["SaldoCarteraReal"],
                    row["MontoColocacionReal"],
                    row["NumColocacionesReal"],
                    row["MontoRepagoReal"],
                )
            )
        with DBConfig.get_dwh_connection() as conn:
            with conn.cursor() as cursor:
                cursor.fast_executemany = True
                cursor.executemany(QUERY_LOAD_FLOW, params)
                conn.commit()
        logging.info("Tabla fct_flow_diario actualizada incrementalmente sin perdidas.")
