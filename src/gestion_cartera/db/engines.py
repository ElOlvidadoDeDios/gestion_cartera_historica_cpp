from abc import ABC, abstractmethod
from config.config import Settings
from gestion_cartera.dim_asesor.constants import QUERY_DIM_ASESOR
import pandas as pd

class DataStrategy(ABC):

    @abstractmethod
    def main(self):
        pass


class DataConnectionStrategy(DataStrategy):

    def __init__(self, settings: Settings):
        self.settings = settings

    def main(self):
        conn_string_upstream = f"mssql+pyodbc://{self.settings.db_upstream.user}:{self.settings.db_upstream.pwd}@{self.settings.db_upstream.server}/{self.settings.db_upstream.database}?driver=ODBC+Driver+17+for+SQL+Server"
        engine_upstream = create_engine(conn_string_upstream)
        return engine_upstream


class DataExtractionStrategy(DataStrategy):

    def __init__(self, engine, query: str):
        self.engine = engine
        self.query = query

    def main(self) -> pd.DataFrame:
        query_path = Path(query)
        query = query_path.read_text(encoding='utf-8')
        df = pd.read_sql(query, engine)
        return df


class DataDesconnectionStrategy(DataStrategy):

    def __init__(self, engine):
        self.engine = engine

    def main(self):
        engine_upstream = self.engine
        engine_upstream.dispose()


if __name__ == "__main__":
    pass
