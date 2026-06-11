import logging
import warnings
from src.components.extract import Extractor
from src.components.transform import Transformer
from src.components.load import Loader

# FILTRO DE SEGURIDAD: Silencia las advertencias estéticas de Pandas por no usar SQLAlchemy
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():
    logging.info(
        "=========================================================================="
    )
    logging.info("START PIPELINE: gestion_cartera_historica_cpp")
    logging.info(
        "=========================================================================="
    )
    try:
        # 1. Extracciones del Periodo del .env
        raw_asesor = Extractor.extract_dim_asesor()
        raw_stock = Extractor.extract_stock_mensual()
        raw_flow = Extractor.extract_flow_diario()

        # 2. Transformaciones Sanitarias
        clean_asesor = Transformer.clean_asesor_data(raw_asesor)
        clean_stock = Transformer.clean_stock_data(raw_stock)
        clean_flow = Transformer.clean_flow_data(raw_flow)

        # 3. Cargas Incrementales Seguras (Dimension -> Hechos)
        Loader.load_dim_asesor(clean_asesor)
        Loader.load_stock_mensual(clean_stock)
        Loader.load_flow_diario(clean_flow)

        logging.info("SUCCESS: Proceso ETL finalizado de forma incremental correcta.")
    except Exception as e:
        logging.error(f"CRITICAL ERROR durante la ejecucion: {str(e)}", exc_info=True)


if __name__ == "__main__":
    run_pipeline()
