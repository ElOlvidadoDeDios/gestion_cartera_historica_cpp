from gestion_cartera.core.config import ConfigManager
from gestion_cartera.core import constants
from gestion_cartera.components.extract import Extractor
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

### Database downstream
engine_downstream = DatabaseConnection.engine('downstream')

###=============================
### Variación incremental
###=============================

# Insertar registros actuales de hoy
df.to_sql(
    ConfigManager.tables.fct.stock.month.calcbl, con=engine_downstream, if_exists="replace", index=False
)

###=============================
### Desconexion a bases de datos
###=============================

engine_downstream.dispose()
