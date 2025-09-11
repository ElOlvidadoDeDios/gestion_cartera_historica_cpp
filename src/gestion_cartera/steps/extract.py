from zenml import step
import pandas as pd
from gestion_cartera.entities import CfgExtractor
from gestion_cartera.components.extract import ComponentExtract, ExtractorDimAsesor


@step
def step_extract_dim_asesor(cfg: CfgExtractor) -> pd.DataFrame:
    try:
        strategy = ExtractorDimAsesor(cfg)
        component_extract = ComponentExtract(strategy)
        df = component_extract.extract()
        return df

    except Exception as e:
        logging.error(e)
        raise e