from gestion_cartera.core.config import ConfigManager
from gestion_cartera.core import constants
from gestion_cartera.components.extract import Extractor
from gestion_cartera.components.load import LoaderFactory

def pipeline_vars_stock():
    df = Extractor.run(constants.SQL_CARTERA_MORAS)
    LoaderFactory.get_loader('strategic').run(df=df, table=ConfigManager.tables.fct.stock.month.calcbl)


if __name__ == '__main__':
    pipeline_vars_stock()
