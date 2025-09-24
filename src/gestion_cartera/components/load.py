from abc import ABC, abstractmethod
import pandas as pd
from gestion_cartera.core.utils import DatabaseConnection
from enum import Enum
from typing import Literal

from gestion_cartera.core.config import ConfigManager

# Producto
class Loader(ABC):
    @abstractmethod
    def run(cls, df: pd.DataFrame, table: str):
        pass


# Productos concretos

class LoaderStrategic(Loader):
    engine = DatabaseConnection.get_engine('downstream')
    
    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        df.to_sql(table, con=cls.engine, if_exists='replace', index=False)
        cls.engine.dispose()

class LoaderOperational(Loader):
    pass


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
    LoaderFactory.get_loader('hola')