import pandas as pd
import logging
from src.core.config import DBConfig
from src.core.constants import QUERY_LOAD_STOCK, QUERY_LOAD_FLOW


class Loader:
    @staticmethod
    def load_stock_mensual(df: pd.DataFrame):
        if df.empty:
            logging.warning("Sin datos de Stock procesados para insertar.")
            return

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
        logging.info("Inyeccion incremental en fct_stock_mensual finalizada con éxito.")

    @staticmethod
    def load_flow_diario(df: pd.DataFrame):
        if df.empty:
            logging.warning("Sin datos de Flujo procesados para insertar.")
            return

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
        logging.info("Inyeccion incremental en fct_flow_diario finalizada con éxito.")
