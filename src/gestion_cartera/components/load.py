import os
import logging
from abc import ABC, abstractmethod
import pandas as pd
from gestion_cartera.core.utils import DatabaseConnection
from sqlalchemy import text
from enum import Enum
from typing import Literal

from gestion_cartera.core.config import ConfigManager

from gestion_cartera.components.view_builder import ViewBuilder


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

    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        pass


# Productos/Estrategias concretas
class LoaderStrategicInitial(StrategyLoaderStrategic):

    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        logging.info(f"🔄 Reemplazando tabla completa (Load Initial): {table}")
        df.to_sql(table, con=cls.engine, if_exists="replace", index=False)
        cls.engine.dispose()
        logging.info(f"✅ Tabla {table} recreada exitosamente con {len(df)} registros.")


class LoaderStrategicVariational(StrategyLoaderStrategic):

    @classmethod
    def run(cls, df: pd.DataFrame, table: str):
        # 1. Obtener el periodo inteligentemente (garantizado por ViewBuilder)
        period, _ = ViewBuilder.get_dynamic_periods()

        logging.info(
            f"🎯 Iniciando carga incremental para la tabla destino: '{table}' | Periodo: {period}"
        )

        # 🔥 CORRECCIÓN DEL BUG DE ACUMULACIÓN:
        # Inyectamos el periodo obligatoriamente al DataFrame para que SQL Server no ponga NULL
        if not df.empty:
            if "Periodo" not in df.columns and "PERIODO" not in df.columns:
                df["Periodo"] = period
            elif "Periodo" in df.columns:
                df["Periodo"] = period  # Homologamos por seguridad
            elif "PERIODO" in df.columns:
                df["PERIODO"] = period

        # 3. Lógica Incremental: Borra solo la "foto" actual y hace append
        with cls.engine.begin() as conn:
            logging.info(
                f"🗑️  Ejecutando DELETE FROM {table} WHERE Periodo = '{period}'..."
            )
            conn.execute(
                text(f"DELETE FROM {table} WHERE Periodo = :periodo"),
                {"periodo": period},
            )

            if not df.empty:
                logging.info(
                    f"💾 Insertando {len(df)} nuevos registros en '{table}'..."
                )
                df.to_sql(table, con=conn, if_exists="append", index=False)
                logging.info(f"✅ Carga incremental finalizada con éxito en '{table}'.")
            else:
                logging.warning(
                    f"⚠️ El DataFrame para '{table}' está vacío. No se insertaron registros."
                )


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
class BIType(Enum):
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
            pass
