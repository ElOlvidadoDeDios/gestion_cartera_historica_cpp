import logging
import pandas as pd
from gestion_cartera.core.utils import DatabaseConnection


class Extractor:
    @classmethod
    def run(cls, sql: str) -> pd.DataFrame:
        # Extraemos un pedacito de la consulta SQL para saber de qué vista se trata
        vista_preview = sql.strip().split("\n")[0][:80]
        logging.info(
            f"🔍 Ejecutando extracción SQL (Upstream)... Muestra: '{vista_preview}...'"
        )

        engine = DatabaseConnection.get_engine("upstream")
        df = pd.read_sql(sql, engine)
        engine.dispose()

        logging.info(f"✅ Extracción completada. Se recuperaron {len(df)} registros.")
        return df


if __name__ == "__main__":
    from gestion_cartera.core import constants

    df = Extractor.run(constants.SQL_CARTERA_MORAS)
    print(df.head())
