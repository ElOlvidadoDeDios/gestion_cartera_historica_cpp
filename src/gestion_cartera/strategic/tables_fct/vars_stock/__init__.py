from gestion_cartera.core.config import ConfigManager
from gestion_cartera.core import constants
from gestion_cartera.components.extract import Extractor
from gestion_cartera.components.load import LoaderFactory
from gestion_cartera.core.utils import DatabaseConnection
import pandas as pd

#############################
### EXTRACT
#############################

df = Extractor.run(constants.SQL_CARTERA_MORAS)

#############################
### TRANSFORM
#############################

# Ninguna

#############################
### LOAD
#############################

LoaderFactory.get_loader('strategic').run(df=df, table=ConfigManager.tables.fct.stock.month.calcbl)

