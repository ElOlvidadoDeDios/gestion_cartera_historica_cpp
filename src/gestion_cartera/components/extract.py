from gestion_cartera.interfaces import ItfExtractor
from omegaconf import DictConfig
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

class Extractor():
    def __init__(self, cfg: DictConfig) -> None:
        self.cfg = cfg
        self.engine = None


    def data_connection(self):
        str_conn = (
            f"mssql+pyodbc://{self.cfg.db.upstream.user}:{self.cfg.db.upstream.pwd}"
            f"@{self.cfg.db.upstream.server}/{self.cfg.db.upstream.db}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
        )
        self.engine = create_engine(str_conn)


    def _load_sql(self) -> str:
        query_path = Path(self.cfg.extract.query).expanduser().resolve()
        return query_path.read_text(encoding='utf-8')


    def data_extraction(self) -> pd.DataFrame:
        sql = self._load_sql()
        with self.engine.begin() as conn:
            df = pd.read_sql(sql, conn)
        return df
        

    def data_desconnection(self):
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None


    def extract(self) -> pd.DataFrame:
        self.data_connection()
        try:
            return self.data_extraction()
        finally:
            self.data_desconnection()
