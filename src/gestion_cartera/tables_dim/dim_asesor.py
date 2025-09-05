import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path
import re

#############################
### EXTRACT
#############################

###==========================
### Conexion a bases de datos
###==========================

load_dotenv()

### Database upstream

user_upstream = os.getenv("DB_UPSTREAM_USER")
pwd_upstream = os.getenv("DB_UPSTREAM_PWD")
server_upstream = os.getenv("DB_UPSTREAM_SERVER")
database_upstream = os.getenv("DB_UPSTREAM_DATABASE")

conn_string_upstream = f"mssql+pyodbc://{user_upstream}:{pwd_upstream}@{server_upstream}/{database_upstream}?driver=ODBC+Driver+17+for+SQL+Server"
engine_upstream = create_engine(conn_string_upstream)

### Database downstream

server_downstream = os.getenv("DB_DOWNSTREAM_SERVER")
database_downstream = os.getenv("DB_DOWNSTREAM_DATABASE")

conn_string_downstream = f"mssql+pyodbc://@{server_downstream}/{database_downstream}?driver=ODBC+Driver+17+for+SQL+Server"
engine_downstream = create_engine(conn_string_downstream)

###==========================
### T-SQL Queries
###==========================

###-------------------------------------
### Tabla "dim_asesor"
###-------------------------------------

query_path = Path("src/gestion_cartera/tables_dim/dim_asesor.sql")

query = query_path.read_text(encoding='utf-8')

df = pd.read_sql(query, engine_upstream)

#############################
### TRANSFORM
#############################

# Ordenar registros
df = df.sort_values(['IdSAgencia', 'IdAsesor'])

# Crear columna a ser usada como alias de los asesores en reporteria
def alias_asesor(nombre):
    # Manejo de NaN/None
    if pd.isna(nombre):
        return "Anónimo"

    s = str(nombre).strip()

    # 2) Separar por la primera coma (si no hay, nombres = "")
    apellidos, nombres = (s.split(',', 1) + [''])[:2]
    apellidos = apellidos.strip()
    nombres = nombres.strip(" .,")

    # 3) Iniciales de apellidos (ignora signos/palabras vacías)
    ap_tokens = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", apellidos)
    iniciales_apellidos = ''.join(t[0].upper() for t in ap_tokens) if ap_tokens else ""

    # 4) Primer nombre, si no existe, "Anónimo"
    m = re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", nombres)
    primer_nombre = m.group(0).capitalize() if m else "Ficticio"

    # 5) Armar alias (sin espacio extra si no hay iniciales)
    return f"{primer_nombre} {iniciales_apellidos}".strip()

df['AsesorAlias'] = df['Asesor'].apply(alias_asesor)

# Asignar agencia a registros sin agencia
mask_juliaca = df['AsesorAlias'].eq('Ficticio RJ')
df.loc[mask_juliaca & df['IdSAgencia'].isna(), 'IdSAgencia'] = '06'

# Identificar asesores ficticios asignables de cartera morosa de la agencia
mask_mora = df['AsesorAlias'].eq('Ficticio RJ')
df.loc[mask_mora & (df['Cargo'] == 'ANALISTA DE CREDITOS I'), 'Cargo'] = 'CARTERA MOROSA'

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
