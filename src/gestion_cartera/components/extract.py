import logging
import time
import pandas as pd
import traceback
from sqlalchemy.exc import SQLAlchemyError
from gestion_cartera.core.utils import DatabaseConnection


class Extractor:
    @classmethod
    def run(cls, sql: str) -> pd.DataFrame:
        # Extraemos un pedacito de la consulta SQL para saber de qué vista se trata
        vista_preview = sql.strip().split("\n")[0][:80]
        logging.info(
            f"🔍 Iniciando extracción SQL (Upstream)... Muestra: '{vista_preview}...'"
        )

        start_time = time.time()
        engine = None

        try:
            engine = DatabaseConnection.get_engine("upstream")

            # EL ESCUDO ANTI-BLOQUEOS
            with engine.connect().execution_options(
                isolation_level="READ UNCOMMITTED"
            ) as conn:
                df = pd.read_sql(sql, conn)

            elapsed_time = round(time.time() - start_time, 2)
            logging.info(
                f"✅ Extracción exitosa: Se recuperaron {len(df)} registros en {elapsed_time} segundos."
            )

            return df

        except SQLAlchemyError as db_err:
            elapsed_time = round(time.time() - start_time, 2)
            # LOG DE ERROR CRÍTICO DE BASE DE DATOS
            logging.error(f"❌ ERROR DE BASE DE DATOS tras {elapsed_time} segundos.")
            logging.error(f"Consulta que falló: '{vista_preview}...'")
            logging.error(f"Detalle del error SQL: {str(db_err)}")

            # Detenemos la ejecución porque si falla la extracción, el ETL no debe continuar
            raise SystemExit("🛑 ETL Detenido por fallo en la base de datos Upstream.")

        except Exception as e:
            elapsed_time = round(time.time() - start_time, 2)
            # LOG DE ERROR GENERAL (Falta de memoria, red, etc.)
            logging.error(
                f"❌ ERROR INESPERADO en la extracción tras {elapsed_time} segundos."
            )
            logging.error(f"Detalle: {str(e)}")
            logging.error(traceback.format_exc())

            raise SystemExit("🛑 ETL Detenido por error crítico en Python.")

        finally:
            # Aseguramos que la conexión se cierre SIEMPRE, incluso si hay error
            if engine:
                engine.dispose()
                logging.debug(
                    "🔌 Conexión al motor de base de datos cerrada y liberada."
                )


if __name__ == "__main__":
    from gestion_cartera.core import constants

    df = Extractor.run(constants.SQL_CARTERA_MORAS)
    print(df.head())
