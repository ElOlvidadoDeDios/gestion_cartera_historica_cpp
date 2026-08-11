import sys
import os
import argparse
import logging
import warnings
import pyodbc
import subprocess
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# 1. Modificar el path para los módulos locales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

# 🔥 LA CORRECCIÓN CLAVE: Cargar el .env AQUÍ, antes de que los pipelines intenten leerlo
from gestion_cartera.core.constants import PATH_ENV

load_dotenv(PATH_ENV)

# 2. Ahora sí importamos los pipelines (ya tendrán las credenciales disponibles)
from gestion_cartera.pipelines import (
    pipeline_initial,
    pipeline_variational,
    pipeline_operational,
    pipeline_operational_ranking_asesor,
)

# Silenciar las advertencias estéticas de Pandas en el log
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

# Configuración de Logs con Rotación Automática (Reemplaza la función manual)
# Mantiene un máximo de 1MB por archivo y guarda hasta 2 archivos de respaldo.
LOG_FILE = os.path.join(BASE_DIR, "ejecucion.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            LOG_FILE, maxBytes=1024 * 1024, backupCount=2, encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)

PIPELINES = {
    "initial": pipeline_initial,
    "variational": pipeline_variational,
    "operational": pipeline_operational,
    "opr_ranking_asesor": pipeline_operational_ranking_asesor,
}


# 🔥 FUNCIÓN CORREGIDA: Cierre seguro garantizado (finally)
def actualizar_fecha_bd():
    conn = None
    try:
        server = os.getenv("DB_DOWNSTREAM_SERVER")
        db = os.getenv("DB_DOWNSTREAM_DATABASE")

        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={db};"
            f"Trusted_Connection=yes;"
        )

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # 1. Intentamos hacer el UPDATE
        cursor.execute(
            "UPDATE [dbo].[Log_Actualizacion] SET UltimaActualizacion = GETDATE() WHERE Id = 1;"
        )

        # 2. Verificamos si realmente se modificó; si no, forzamos el INSERT
        if cursor.rowcount == 0:
            logging.warning(
                "⚠️ No se encontró el Id = 1. Creando el registro inicial..."
            )
            cursor.execute(
                "INSERT INTO [dbo].[Log_Actualizacion] (Id, UltimaActualizacion) VALUES (1, GETDATE());"
            )

        conn.commit()
        logging.info("✅ Fecha de Última Actualización renovada exitosamente en BD.")

    except Exception as e:
        logging.error(f"❌ Error al actualizar la fecha en BD: {e}")

    finally:
        # Esto garantiza que el motor cierre la conexión SIEMPRE, haya error o no.
        if conn:
            conn.close()


def actualizar_powerbi():
    ruta_script = os.path.join(BASE_DIR, "refresh_powerbi.ps1")
    try:
        resultado = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ruta_script],
            capture_output=True,
            text=True,
        )
        if resultado.returncode == 0:
            print(resultado.stdout)
            logging.info("✅ Power BI actualizado correctamente mediante PowerShell.")
        else:
            logging.error(f"❌ Error de PowerShell: {resultado.stderr}")
    except Exception as e:
        logging.error(f"❌ Excepción fatal al intentar ejecutar PowerShell: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ejecutar pipelines de gestión de cartera."
    )
    parser.add_argument(
        "pipeline",
        choices=PIPELINES.keys(),
        help="Pipeline a ejecutar: 'initial', 'variational', 'operational' o 'opr_ranking_asesor'.",
    )
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  ETL COMPLETO - GESTION CARTERA HISTORICA CPP")
    print("=" * 60)

    print(f"\n[1/3] Ejecutando procesamiento principal ({args.pipeline})...")
    logging.info(f"🚀 Iniciando ejecución de pipeline: {args.pipeline}")

    PIPELINES[args.pipeline]()

    print("\n[2/3] Registrando hora de última actualización en BD...")
    actualizar_fecha_bd()

    print("\n[3/3] Sincronizando el Dashboard en Power BI Service...")
    actualizar_powerbi()

    print("\n" + "=" * 60)
    print("  PROCESO COMPLETADO CON EXITO")
    print("=" * 60 + "\n")

    logging.info(f"🏁 Ejecución total de {args.pipeline} finalizada.")


if __name__ == "__main__":
    main()
