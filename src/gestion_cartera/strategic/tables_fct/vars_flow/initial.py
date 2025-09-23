from dotenv import load_dotenv
load_dotenv('.env')
import os
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

#############################
### EXTRACT
#############################

###==========================
### Conexion a bases de datos
###==========================

### Database upstream

user_upstream = os.getenv("DB_UPSTREAM_USER")
pwd_upstream = os.getenv("DB_UPSTREAM_PASSWORD")
server_upstream = os.getenv("DB_UPSTREAM_SERVER")
database_upstream = os.getenv("DB_UPSTREAM_DATABASE")

conn_string_upstream = f"mssql+pyodbc://{user_upstream}:{pwd_upstream}@{server_upstream}/{database_upstream}?driver=ODBC+Driver+17+for+SQL+Server"
engine_upstream = create_engine(conn_string_upstream)

### Database upstream y downstream

server_downstream = os.getenv("DB_DOWNSTREAM_SERVER")
database_downstream = os.getenv("DB_DOWNSTREAM_DATABASE")

conn_string_downstream = f"mssql+pyodbc://@{server_downstream}/{database_downstream}?driver=ODBC+Driver+17+for+SQL+Server"
engine_downstream = create_engine(conn_string_downstream)

###==========================
### T-SQL Queries
###==========================

###---------------------------------
### DataFrame "repago"
###---------------------------------

query_path = Path("src/gestion_cartera/tables_fct/vars_flow/day/initial/repago.sql")

query = query_path.read_text(encoding='utf-8')

df_repago = pd.read_sql(query, engine_upstream)

###---------------------------------
### DataFrame "dim_asesor"
###---------------------------------

query_path = Path("src/gestion_cartera/tables_dim/dim_asesor.sql")

query = query_path.read_text(encoding='utf-8')

df_dim_asesor = pd.read_sql(query, engine_upstream)

#############################
### TRANSFORM
#############################

###------------------------------------
### Tabla de variables de flujo "puras"
###------------------------------------

# Extraer el listado respecto a las fechas y los asesores
df_fechas = df_flow_real_colocacion[['Fecha', 'Periodo']].drop_duplicates()
df_asesores = df_dim_asesor[['IdSAgencia', 'IdAsesor']].drop_duplicates()

# Obtener el DataFrame producto cartesiano "fechas"x"asesor"
df_fechas["key"] = 1
df_asesores["key"] = 1
df_producto_cartersiano = df_fechas.merge(df_asesores, on="key").drop(columns="key")

# Combinar con datos
df_flow = df_producto_cartersiano.merge(
    	df_flow_real_colocacion.drop(columns=['Periodo']), on=["Fecha", "IdAsesor"], how="left"
	).merge(
    	df_flow_real_repago, on=["Fecha", "IdAsesor"], how="left"
	)

# Rellenar los NaN en las columnas numéricas con 0
df_flow[df_flow.select_dtypes(include='number').columns] = df_flow.select_dtypes(include='number').fillna(0)

# Ordenar registros
df_flow = df_flow.sort_values(["Fecha", "IdSAgencia", "IdAsesor"])

###------------------------------------
### Tabla de variables de "cuasi"-flujo
###------------------------------------

# Reordenar por fecha, agencia y asesor
df_stock_real_cartera_moras = df_stock_real_cartera_moras.sort_values(["IdSAgencia", "IdAsesor", "Fecha"])

# Calcular variaciones respecto al dia anterior por asesor
df_stock_real_cartera_moras["CarteraQuasiFlujo"] = df_stock_real_cartera_moras.groupby(["IdSAgencia", "IdAsesor"])["Cartera"].diff()
df_stock_real_cartera_moras["Mora9QuasiFlujo"] = df_stock_real_cartera_moras.groupby(["IdSAgencia", "IdAsesor"])["Mora9"].diff()
df_stock_real_cartera_moras["Mora31QuasiFlujo"] = df_stock_real_cartera_moras.groupby(["IdSAgencia", "IdAsesor"])["Mora31"].diff()

# Rellenar NaN en las variaciones del primer dia de cada asesor con 0
df_stock_real_cartera_moras[["CarteraQuasiFlujo", "Mora9QuasiFlujo", "Mora31QuasiFlujo"]] = df_stock_real_cartera_moras[["CarteraQuasiFlujo", "Mora9QuasiFlujo", "Mora31QuasiFlujo"]].fillna(0)

###----------------------------------------------------------------
### Combinación de las tablas de variables de flujo y "cuasi"-flujo
###----------------------------------------------------------------

df_flow_quasi_flow = df_flow.merge(
    df_stock_real_cartera_moras[["Fecha", "IdSAgencia", "IdAsesor", "CarteraQuasiFlujo", "Mora9QuasiFlujo", "Mora31QuasiFlujo"]], 
    on=["Fecha", "IdSAgencia", "IdAsesor"], 
    how="inner"
)

#############################
### LOAD
#############################

df_flow_quasi_flow.to_sql(
    "fct_flow_real", con=engine_downstream, if_exists="replace", index=False
)

###=============================
### Desconexion a bases de datos
###=============================

engine_upstream.dispose()
engine_downstream.dispose()
