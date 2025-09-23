from gestion_cartera.core.config import ConfigManager
from gestion_cartera.core import constants
from gestion_cartera.core.utils import DatabaseConnection
import pandas as pd

#############################
### EXTRACT
#############################

###==========================
### Conexion a bases de datos
###==========================

### Database upstream
engine_upstream = DatabaseConnection.engine('upstream')

### Database downstream
engine_downstream = DatabaseConnection.engine('downstream')

###==========================
### T-SQL Queries
###==========================

df = pd.read_sql(constants.SQL_CARTERA_MORAS, engine_upstream)

#############################
### TRANSFORM
#############################

# Ninguna

#############################
### LOAD
#############################

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

engine_upstream.dispose()
engine_downstream.dispose()
