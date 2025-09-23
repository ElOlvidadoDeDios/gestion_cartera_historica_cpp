from gestion_cartera.core.utils import DatabaseConnection
from gestion_cartera.core.constants import *
from pathlib import Path
from sqlalchemy import text
import pandas as pd
from datetime import date
from gestion_cartera.core.utils import load_config
config = load_config()
from gestion_cartera.core.config import ConfigManager

#############################
### EXTRACT
#############################

###==========================
### Conexion a bases de datos
###==========================

database_connection = DatabaseConnection()

### Database upstream
engine_upstream = database_connection.engine('upstream')

### Database downstream
engine_downstream = database_connection.engine('downstream')

###==========================
### T-SQL Queries
###==========================

#project_path = Path(__file__).resolve().parents[6]

###-------------------------------------
### Tabla "stock_real_cartera_moras"
###-------------------------------------

path_query = Path(PATH_PROJECT, "sql/cartera_moras.sql")

query = path_query.read_text(encoding='utf-8')

df = pd.read_sql(query, engine_upstream)

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
