from zenml import pipeline
from gestion_cartera.entities import CfgExtractor
from gestion_cartera.steps.extract import step_extract_dim_asesor

@pipeline
def pipeline_dim_asesor(
    cfg: CfgExtractor
    ):

    df = step_extract_dim_asesor(cfg)
    return df