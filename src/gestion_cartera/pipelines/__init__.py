from omegaconf import DictConfig
import pandas as pd


class PipelineDimAsesor:
    def __init__(self, cfg:DictConfig):
        self.cfg_extract = cfg.extract
        self.cfg_transform = cfg.transform
        self.cfg_load = cfg.load
        
    
    def extract(self) -> pd.DataFrame:
        return step_extract_dim_asesor(self.cfg_extract)

    def transform(self):
        pass

    def load(self):
        pass

    def run(self):
        df = self.extract()
        df = self.transform()
        self.load()