from gestion_cartera.core.config import ConfigManager
from gestion_cartera.core import constants
from gestion_cartera.components.extract import Extractor
from gestion_cartera.components.transform import TransformerFactory
from gestion_cartera.components.load import LoaderFactory
import pandas as pd


def pipeline_dim_asesor() -> None:
    df_loaded = Extractor.run(constants.SQL_DIM_ASESOR)
    df_transformed = TransformerFactory().get_transformer('dim_asesor').run(df=df_loaded)
    LoaderFactory.get_loader('strategic').run(df=df_transformed, table=ConfigManager.table.dim.asesor)


def pipeline_vars_stock() -> None:
    df = Extractor.run(constants.SQL_CARTERA_MORAS)
    LoaderFactory.get_loader('strategic').run(df=df, table=ConfigManager.table.fct.stock)


def pipeline_vars_flow() -> None:
    df = Extractor.run(constants.SQL_FCT_FLOW)
    LoaderFactory.get_loader('strategic').run(df=df, table=ConfigManager.table.fct.flow)


if __name__ == '__main__':
    pipeline_vars_flow()
