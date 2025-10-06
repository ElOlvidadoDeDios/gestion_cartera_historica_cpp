from abc import ABC, abstractmethod
import pandas as pd
from gestion_cartera.core.utils import DatabaseConnection
from sqlalchemy import text
from enum import Enum
from typing import Literal

from gestion_cartera.core.config import ConfigManager
from datetime import date

# Producto
class Loader(ABC):

    @abstractmethod
    def run(cls, df: pd.DataFrame, table: str, temporality=None):
        pass


# Estrategias

class StrategyLoaderStrategic(Loader, ABC):

    engine = DatabaseConnection.get_engine('downstream')
    
    @classmethod
    def run(cls, df: pd.DataFrame, table: str, temporality=None):
        pass

class StrategyLoaderOperational(Loader, ABC):

    # TODO Especificar especifica obtencion de 'engine'
    
    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        pass


# Productos/Estrategias concretas

class LoaderStrategicInitial(StrategyLoaderStrategic):

    @classmethod
    def run(cls, df: pd.DataFrame, table: str, temporality=None):
        df.to_sql(table, con=cls.engine, if_exists='replace', index=False)
        cls.engine.dispose()


class LoaderStrategicVariational(StrategyLoaderStrategic):

    @classmethod
    def run(cls, df: pd.DataFrame, table: str, temporality: Literal['at_date', 'on_date']):

        if date == 'at_date':
            temporality = date.today().strftime("%Y%m")

            with cls.engine.begin() as conn:
                conn.execute(
                    text("DELETE FROM :Tabla WHERE Periodo = :Periodo"),
                    {"Tabla": table, "Periodo": temporality}
                )

        elif date == 'on_date':
            temporality = date.today().strftime("%Y%m%d")

            with cls.engine.begin() as conn:
                conn.execute(
                    text("DELETE FROM :Tabla WHERE Fecha = :Fecha"),
                    {"Tabla": table, "Fecha": temporality}
                )

        df.to_sql(table, con=cls.engine, if_exists="append", index=False)
        cls.engine.dispose()


# Contextos

class LoaderStrategic(StrategyLoaderStrategic):

    def __init__(self, strategy: StrategyLoaderStrategic | None = None, temporality = None) -> None:
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def run(self, df: pd.DataFrame, table: str, temporality=None) -> None:
        return self.strategy.run(df, table, temporality)


# Factory

class BIType(Enum): # Types of business intelligence
    strategic = 'strategic'
    operational = 'operational'

class LoaderFactory:
    @staticmethod
    def get_loader(bi_type: Literal['strategic', 'operational']) -> Loader:
        try:
            bi_type = BIType(bi_type)
        except ValueError:
            raise ValueError(f"Unsupported loader type: {bi_type}")

        if bi_type is BIType.strategic:
            return LoaderStrategic()
        elif bi_type is BIType.operational:
            return LoaderOperational()


if __name__ == '__main__':
    loader_strategic = LoaderFactory.get_loader('strategic')
    loader_strategic.strategy = LoaderStrategicInitial
    loader_strategic.run(df, ConfigManager.table.fct.stock)