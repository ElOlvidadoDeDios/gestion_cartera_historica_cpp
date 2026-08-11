import os
import pyodbc
import pandas as pd
import logging
import calendar
import holidays
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
load_dotenv()

# Conexiones
REMOTE_DB = f"DRIVER={{SQL Server}};SERVER={os.getenv('DB_UPSTREAM_SERVER')};DATABASE={os.getenv('DB_UPSTREAM_DATABASE')};UID={os.getenv('DB_UPSTREAM_USER')};PWD={os.getenv('DB_UPSTREAM_PASSWORD')};"
LOCAL_DB = f"DRIVER={{SQL Server}};SERVER={os.getenv('DB_DOWNSTREAM_SERVER')};DATABASE={os.getenv('DB_DOWNSTREAM_DATABASE-productividad')};Trusted_Connection=yes;"

# Constantes para la actualización de vistas
ESTADO_ARCHIVO = "estado_vistas.txt"
CARPETA_VISTAS = "sql/operational/views"


def verificar_y_actualizar_vistas(periodo_nuevo):
    if not periodo_nuevo:
        logging.error("❌ No se encontró PERIODO en el archivo .env")
        return

    # 1. Leer el estado actual
    periodo_actual = None
    if os.path.exists(ESTADO_ARCHIVO):
        with open(ESTADO_ARCHIVO, "r", encoding="utf-8") as f:
            periodo_actual = f.read().strip()

    # 2. Comparar periodos
    if periodo_actual == str(periodo_nuevo):
        logging.info(
            f"✅ Vistas SQL Upstream ya actualizadas para el periodo {periodo_nuevo}. Se omite recreación."
        )
        return

    logging.info(
        f"🔄 Cambio de periodo detectado ({periodo_actual} -> {periodo_nuevo}). Actualizando vistas en origen..."
    )

    # 3. Leer y ejecutar cada vista
    vistas_sql = ["dbo.gc_cartera_agencia.sql", "dbo.gc_cartera_asesor.sql"]
    conn_remote = None

    try:
        # Autocommit=True es requerido por SQL Server para crear vistas (DDL) a través de pyodbc
        conn_remote = pyodbc.connect(REMOTE_DB, autocommit=True)
        cursor = conn_remote.cursor()

        for vista_file in vistas_sql:
            ruta_vista = os.path.join(CARPETA_VISTAS, vista_file)
            if os.path.exists(ruta_vista):
                with open(ruta_vista, "r", encoding="utf-8") as f:
                    sql_template = f.read()

                # Inyectar el periodo del .env en el código SQL
                sql_final = sql_template.replace("{PERIODO}", str(periodo_nuevo))

                # Ejecutar el query
                cursor.execute(sql_final)
                logging.info(f"✅ Vista reconstruida con éxito en origen: {vista_file}")
            else:
                logging.warning(f"⚠️ No se encontró el archivo de vista: {ruta_vista}")

        # 4. Guardar el nuevo estado si todo sale bien
        with open(ESTADO_ARCHIVO, "w", encoding="utf-8") as f:
            f.write(str(periodo_nuevo))
        logging.info(
            f"📝 Archivo de control actualizado. Periodo fijado: {periodo_nuevo}"
        )

    except Exception as e:
        logging.error(f"❌ Error al intentar crear las vistas SQL: {e}")
        raise SystemExit(
            "🛑 ETL Detenido: Fallo crítico al actualizar vistas de origen."
        )
    finally:
        if conn_remote:
            conn_remote.close()


def sync_data(vista, tabla, periodo, mapeo_columnas):
    conn_remote = None
    conn_local = None
    try:
        logging.info(f"--- Sincronizando: {vista} -> {tabla} ---")

        # 1. Extraer
        conn_remote = pyodbc.connect(REMOTE_DB)
        query = (
            f"SELECT * FROM [TRANSACMIF].[dbo].[{vista}] WHERE Periodo = '{periodo}'"
        )
        # Usamos el escudo NOLOCK a nivel de conexión por seguridad
        conn_remote.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        df = pd.read_sql(query, conn_remote)

        if df.empty:
            logging.warning(f"No hay datos para {periodo} en {vista}")
            conn_remote.close()
            return

        # 2. Preparar datos
        df = df.rename(columns=mapeo_columnas)
        columnas_finales = list(mapeo_columnas.values())
        df = df[columnas_finales]

        # 3. Cargar
        conn_local = pyodbc.connect(LOCAL_DB)
        cursor = conn_local.cursor()

        # Borrado y carga
        cursor.execute(
            f"DELETE FROM [dm_productividad].[dbo].[{tabla}] WHERE Periodo = '{periodo}'"
        )

        cols_str = ", ".join(columnas_finales)
        placeholders = ", ".join(["?"] * len(columnas_finales))
        sql_insert = f"INSERT INTO [dm_productividad].[dbo].[{tabla}] ({cols_str}) VALUES ({placeholders})"

        for _, row in df.iterrows():
            cursor.execute(sql_insert, tuple(row))

        conn_local.commit()
        logging.info(f"✅ Éxito: {len(df)} registros cargados en {tabla}")

    except Exception as e:
        if conn_local:
            conn_local.rollback()
        logging.error(f"❌ Error en {tabla}: {e}")
    finally:
        if conn_remote:
            conn_remote.close()
        if conn_local:
            conn_local.close()


def sync_dim_calendario(periodo: str):
    conn_local = None
    try:
        logging.info(f"--- Sincronizando: dim_calendario para el periodo {periodo} ---")

        # 1. Extraer año y mes del periodo (Ej: "202608" -> Año: 2026, Mes: 8)
        year = int(periodo[:4])
        month = int(periodo[4:])

        # Obtener el último día de ese mes específico
        _, last_day = calendar.monthrange(year, month)

        # 2. Generar el rango de fechas en Pandas
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day}"
        df = pd.DataFrame({"Fecha": pd.date_range(start_date, end_date)})

        # Diccionario para traducir los meses al español
        meses_es = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

        # 3. Cargar los Feriados Oficiales de Perú para ese año
        pe_holidays = holidays.PE(years=year)

        # 4. Construir las columnas exactamente como en tu reporte
        df["Año"] = df["Fecha"].dt.year
        df["Trimestre"] = df["Fecha"].dt.quarter
        df["Periodo"] = df["Fecha"].dt.strftime("%Y%m")
        df["NumMes"] = df["Fecha"].dt.month
        df["Mes"] = df["Fecha"].dt.strftime("%m")
        df["MesLargo"] = df["NumMes"].map(meses_es)
        df["Dia"] = df["Fecha"].dt.day

        # Lógica para Booleanos (1 = TRUE, 0 = FALSE)
        df["EsDomingo"] = (df["Fecha"].dt.dayofweek == 6).astype(int)
        df["EsFeriado"] = (
            df["Fecha"].apply(lambda x: 1 if x in pe_holidays else 0).astype(int)
        )

        # Convertir Fecha a string para evitar errores de pyodbc
        df["Fecha"] = df["Fecha"].dt.strftime("%Y-%m-%d")

        # 5. Cargar a la Base de Datos Local de forma Idempotente
        conn_local = pyodbc.connect(LOCAL_DB)
        cursor = conn_local.cursor()

        # Borrar el mes actual si ya existe para evitar duplicados
        cursor.execute(
            f"DELETE FROM [dm_productividad].[dbo].[dim_calendario] WHERE Periodo = '{periodo}'"
        )

        # Inserción masiva
        cols = [
            "Fecha",
            "Año",
            "Trimestre",
            "Periodo",
            "NumMes",
            "Mes",
            "MesLargo",
            "Dia",
            "EsDomingo",
            "EsFeriado",
        ]
        placeholders = ", ".join(["?"] * len(cols))
        sql_insert = f"INSERT INTO [dm_productividad].[dbo].[dim_calendario] ({', '.join(cols)}) VALUES ({placeholders})"

        # Convertir a lista de tuplas nativas de Python
        params = [tuple(row) for row in df.to_numpy()]

        cursor.fast_executemany = False
        cursor.executemany(sql_insert, params)
        conn_local.commit()

        logging.info(
            f"✅ Éxito: {len(df)} días insertados en dim_calendario para {periodo}."
        )

    except Exception as e:
        if conn_local:
            conn_local.rollback()
        logging.error(f"❌ Error al cargar dim_calendario: {e}")
    finally:
        if conn_local:
            conn_local.close()


if __name__ == "__main__":
    periodo = os.getenv("PERIODO")

    # 1. Rutina inteligente: Verificar y recrear vistas solo si es necesario
    verificar_y_actualizar_vistas(periodo)

    # 2. Rutina de extracción e inserción
    mapa_agencia = {
        "Periodo": "Periodo",
        "IdSAgencia": "IdSAgencia",
        "CarteraInicial": "CarteraInicial",
        "MetaMoraCPP": "Mora9Meta",
        "MetaMoraDeficiente": "Mora31Meta",
    }
    mapa_asesor = {
        "Periodo": "Periodo",
        "IdSAsesor": "IdSAsesor",
        "CarteraInicial": "CarteraInicial",
        "Mora9Meta": "Mora9Meta",
        "Mora31Meta": "Mora31Meta",
    }

    sync_data(
        os.getenv("VISTA_AGENCIA"), os.getenv("TABLA_AGENCIA"), periodo, mapa_agencia
    )
    sync_data(
        os.getenv("VISTA_ASESOR"), os.getenv("TABLA_ASESOR"), periodo, mapa_asesor
    )
    # Sincronizar el calendario para el mes
    sync_dim_calendario(periodo)
