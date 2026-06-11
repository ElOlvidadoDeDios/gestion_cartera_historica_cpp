import logging
from src.components.extract import Extractor
from src.components.transform import Transformer
from src.components.load import Loader

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
        # Executar Extracciones con Filtros Temporales
        raw_stock = Extractor.extract_stock_mensual()
        raw_flow = Extractor.extract_flow_diario()

        # Executar Limpieza e Integracion de Mapeos
        clean_stock = Transformer.clean_stock_data(raw_stock)
        clean_flow = Transformer.clean_flow_data(raw_flow)

        # Inyectar de Forma Incremental en DWH Local
        Loader.load_stock_mensual(clean_stock)
        Loader.load_flow_diario(clean_flow)

        logging.info("SUCCESS: Proceso ETL finalizado correctamente.")
    except Exception as e:
        logging.error(f"CRITICAL ERROR durante la ejecucion: {str(e)}", exc_info=True)


if __name__ == "__main__":
    run_pipeline()
