from gestion_cartera.interfaces import ItfExtractor
from gestion_cartera.entities import CfgExtractor
from sqlalchemy import create_engine
import pandas as pd


class ExtractorDimAsesor(ItfExtractor):
    def __init__(self, cfg: CfgExtractor) -> None:
        self.cfg = cfg

    def extract(self) -> pd.DataFrame:
        engine = create_engine(cfg.dsn)
        df = pd.read_sql(cfg.query, engine)
        return df


class ComponentExtract:
    def __init__(self, strategy: ItfExtractor) -> None:
        self.strategy = strategy

    def extract(self) -> pd.DataFrame:
        df = self.strategy.extract()
        return df
