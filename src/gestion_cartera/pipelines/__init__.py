from gestion_cartera.core.config import ConfigManager
from gestion_cartera.core import constants
from gestion_cartera.components.extract import Extractor
from gestion_cartera.components.transform import TransformerFactory
from gestion_cartera.components.load import LoaderFactory, LoaderStrategicInitial, LoaderStrategicVariational
import pandas as pd
from enum import Enum
from typing import Literal, Optional, Callable
from dataclasses import dataclass


class Variant(Enum):
    INITIAL = 'initial'
    VARIATIONAL = 'variational'


STRATEGY_BY_VARIANT = {
    Variant.INITIAL: LoaderStrategicInitial,
    Variant.VARIATIONAL: LoaderStrategicVariational
}


@dataclass(frozen=True)
class SubjectConfig:
    sql: str
    table: object
    transformer_key: Optional[str] = None


def _get_transformer(transformer_key: Optional[str]) -> Callable:
    if not transformer_key:
        return lambda df: df

    transformer = TransformerFactory().get_transformer(transformer_key)
    return lambda df: transformer.run(df=df)


SUBJECTS = {
    'dim_asesor': SubjectConfig(
        sql=constants.SQL_DIM_ASESOR,
        table=ConfigManager.table.dim.asesor,
        transformer_key='dim_asesor',
    ),
    'fct_stock': SubjectConfig(
        sql=constants.SQL_FCT_STOCK,
        table=ConfigManager.table.fct.stock,
        transformer_key=None,
    ),
    'fct_flow': SubjectConfig(
        sql=constants.SQL_FCT_FLOW,
        table=ConfigManager.table.fct.flow,
        transformer_key=None,
    ),
}


def pipeline(subject: Literal['dim_asesor', 'fct_stock', 'fct_flow'], variant: Variant) -> None:
    
    # Preambule
    cfg = SUBJECTS[subject]

    # Extract
    df_extracted = Extractor.run(cfg.sql)

    # Transform
    transform = _get_transformer(cfg.transformer_key)
    df_transformed = transform(df_extracted)

    # Load
    loader = LoaderFactory.get_loader('strategic')
    loader.strategy = STRATEGY_BY_VARIANT[variant]
    loader.run(df=df_transformed, table=cfg.table)


def pipeline_initial() -> None:
    pipeline('dim_asesor', Variant.INITIAL)
    pipeline('fct_stock', Variant.INITIAL)
    pipeline('fct_flow', Variant.INITIAL)


def pipeline_variational() -> None:
    pipeline('dim_asesor', Variant.INITIAL)
    pipeline('fct_stock', Variant.VARIATIONAL)
    pipeline('fct_flow', Variant.VARIATIONAL)


if __name__ == '__main__':
    pipeline_dim_asesor()
