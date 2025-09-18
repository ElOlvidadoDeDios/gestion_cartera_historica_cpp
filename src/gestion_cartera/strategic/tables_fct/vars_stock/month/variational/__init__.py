from gestion_cartera.core.utils import DatabaseConnection
from gestion_cartera.core.constants import *
from pathlib import Path
from sqlalchemy import text
import pandas as pd
from datetime import date

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

df.drop(columns=["Asesor"], inplace=True)

#############################
### LOAD
#############################

# Obtener la fecha actual
fecha_hoy = date.today().strftime("%Y-%m-%d")

# Eliminar registros de hoy
with engine_downstream.begin() as conn:
	conn.execute(
		text("DELETE FROM fct_stock_real WHERE CAST(Fecha AS DATE) = :fecha"),
		{"fecha": fecha_hoy}
	)

# Insertar registros actuales de hoy
df_stock_real_cartera_moras.to_sql(
    "fct_stock_real", con=engine_downstream, if_exists="append", index=False
)

###=============================
### Desconexion a bases de datos
###=============================

engine_upstream.dispose()
engine_downstream.dispose()
