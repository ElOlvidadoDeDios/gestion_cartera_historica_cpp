from dotenv import load_dotenv
load_dotenv(".env")

from hydra import main
from omegaconf import DictConfig, OmegaConf

from gestion_cartera.pipelines import PipelineDimAsesor


@main(config_path="conf", config_name="config", version_base=None)
def run_pipelines(cfg: DictConfig) -> None:

    PipelineDimAsesor.run()


if __name__ == "__main__":

    run_pipelines()
