from gestion_cartera.core.utils import DatabaseConnection
from pathlib import Path
from gestion_cartera.core.constants import *
import pandas as pd

#############################
### EXTRACT
#############################

database_connection = DatabaseConnection()

###==========================
### Conexion a bases de datos
###==========================

### Database upstream

engine_upstream = database_connection.engine('upstream')

### Database downstream

engine_downstream = database_connection.engine('downstream')

###==========================
### T-SQL Queries
###==========================

###-------------------------------------
### Tabla "dim_asesor"
###-------------------------------------

query_path = Path(PATH_PROJECT, "sql/dim_asesor.sql")

query = query_path.read_text(encoding='utf-8')

df = pd.read_sql(query, engine_upstream)

#############################
### TRANSFORM
#############################

# Quitar registros de asesores o recuperadores atípicos
df = df[df['IdSAgencia'].notna()]

# Creacion de la variable 'Asesor'. Esta columna será usada como alias de los asesores en reporteria
def alias_asesor(nombre):
    apellidos, nombres = nombre.split(', ')
    iniciales_apellidos = ''.join([a[0].upper() for a in apellidos.split()])
    primer_nombre = nombres.split()[0].capitalize()
    return f"{primer_nombre} {iniciales_apellidos}"

df['Asesor'] = df['AsesorNombresApellidos'].apply(alias_asesor)

#############################
### LOAD
#############################

df.to_sql(
    'dim_asesor', con=engine_downstream, if_exists='replace', index=False
)

###=============================
### Desconexion a bases de datos
###=============================

engine_upstream.dispose()
engine_downstream.dispose()
