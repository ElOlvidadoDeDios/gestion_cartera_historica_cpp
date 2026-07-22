import os
from abc import ABC, abstractmethod
import pandas as pd
from gestion_cartera.core.utils import DatabaseConnection
from sqlalchemy import text
from enum import Enum
from typing import Literal

from gestion_cartera.core.config import ConfigManager


# Producto
class Loader(ABC):

    @abstractmethod
    def run(cls, df: pd.DataFrame, table: str):
        pass


# Estrategias


class StrategyLoaderStrategic(Loader, ABC):

    engine = DatabaseConnection.get_engine("downstream")

    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        pass


class StrategyLoaderOperational(Loader, ABC):

    # TODO Especificar especifica obtencion de 'engine'

    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        pass


# Productos/Estrategias concretas


class LoaderStrategicInitial(StrategyLoaderStrategic):

    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        df.to_sql(table, con=cls.engine, if_exists="replace", index=False)
        cls.engine.dispose()


class LoaderStrategicVariational(StrategyLoaderStrategic):

    @classmethod
    def run(cls, df: pd.DataFrame, table: str):

        # 1. Intentamos leer el periodo desde tu archivo .env
        period = os.getenv("PERIODO")

        # 2. Respaldo inteligente: si no está en el .env, lo lee del DataFrame de la vista
        if not period and "Periodo" in df.columns and not df.empty:
            period = str(df["Periodo"].iloc[0])
        elif not period and "PERIODO" in df.columns and not df.empty:
            period = str(df["PERIODO"].iloc[0])

        if not period:
            raise ValueError(
                f"No se pudo determinar el periodo para la tabla {table}. Verifica el archivo .env o la vista SQL."
            )

        # 3. Lógica Incremental: Borra solo la "foto" actual y hace append de lo nuevo
        with cls.engine.begin() as conn:
            conn.execute(
                text(f"DELETE FROM {table} WHERE Periodo = :periodo"),
                {"periodo": period},
            )
            df.to_sql(table, con=conn, if_exists="append", index=False)


# Contextos


class LoaderStrategic(StrategyLoaderStrategic):

    def __init__(self, strategy: StrategyLoaderStrategic | None = None) -> None:
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def run(self, df: pd.DataFrame, table: str) -> None:
        return self.strategy.run(df, table)


# Factory


class BIType(Enum):  # Types of business intelligence
    strategic = "strategic"
    operational = "operational"


class LoaderFactory:
    @staticmethod
    def get_loader(bi_type: Literal["strategic", "operational"]) -> Loader:
        try:
            bi_type = BIType(bi_type)
        except ValueError:
            raise ValueError(f"Unsupported loader type: {bi_type}")

        if bi_type is BIType.strategic:
            return LoaderStrategic()
        elif bi_type is BIType.operational:
            # Aquí asumimos que crearás la clase LoaderOperational más adelante
            pass


if __name__ == "__main__":
    loader_strategic = LoaderFactory.get_loader("strategic")
    loader_strategic.strategy = LoaderStrategicVariational
    # Nota: df debe estar definido antes de llamar a run en tu flujo real
    loader_strategic.run(df, ConfigManager.table.fct.stock)
