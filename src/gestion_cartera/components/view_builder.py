import os
import logging
from pathlib import Path
from datetime import date, timedelta
from sqlalchemy import text
from gestion_cartera.core.utils import DatabaseConnection
from gestion_cartera.core.constants import PATH_PROJECT


class ViewBuilder:
    @staticmethod
    def get_dynamic_periods() -> tuple[str, str]:
        # 1. Prioridad 1: Leer el .env
        period_env = os.getenv("PERIODO")

        if period_env:
            year, month = int(period_env[:4]), int(period_env[4:6])
        else:
            # Prioridad 2: Cálculo automático
            today = date.today()
            if today.day == 1:
                target_date = today.replace(day=1) - timedelta(days=1)
            else:
                target_date = today

            year, month = target_date.year, target_date.month

        periodo_actual = f"{year}{month:02d}"

        # Calcular periodo anterior (para el LAG de socios)
        prev_month = 12 if month == 1 else month - 1
        prev_year = year - 1 if month == 1 else year
        periodo_anterior = f"{prev_year}{prev_month:02d}"

        return periodo_actual, periodo_anterior

    @classmethod
    def run(cls):
        actual, anterior = cls.get_dynamic_periods()

        # --- SISTEMA DE CONTROL DE ESTADO ---
        # Guardaremos un archivo de texto ligero para no saturar la BD
        estado_file = Path(PATH_PROJECT, "conf", ".estado_vistas")

        if estado_file.exists():
            ultimo_periodo = estado_file.read_text(encoding="utf-8").strip()
            if ultimo_periodo == actual:
                logging.info(
                    f"⏭️ Las vistas SQL ya están configuradas para el periodo '{actual}'. Omitiendo reconstrucción."
                )
                return  # Detiene la ejecución aquí, ahorrando tiempo

        logging.info(
            f"🛠️ Construyendo vistas en Upstream | Actual: {actual} | Anterior: {anterior}"
        )

        engine = DatabaseConnection.get_engine("upstream")
        views_dir = Path(PATH_PROJECT, "sql", "strategic", "views")

        with engine.begin() as conn:
            for file_path in views_dir.glob("*.sql"):
                sql_template = file_path.read_text(encoding="utf-8")

                # Inyección de parámetros
                sql_query = sql_template.replace("{PERIODO_ACTUAL}", actual).replace(
                    "{PERIODO_ANTERIOR}", anterior
                )

                try:
                    conn.execute(text(sql_query))
                    logging.info(f"✅ Vista creada/actualizada: {file_path.name}")
                except Exception as e:
                    logging.error(f"❌ Error en {file_path.name}: {e}")

        engine.dispose()

        # Guardamos el nuevo estado en el archivo
        estado_file.parent.mkdir(parents=True, exist_ok=True)
        estado_file.write_text(actual, encoding="utf-8")
        logging.info(f"📝 Estado actualizado. Nuevo periodo fijado: {actual}")
