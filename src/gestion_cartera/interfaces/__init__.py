import pandas as pd
from abc import ABC, abstractmethod


class ItfExtractor(ABC):
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        raise NotImplementedError


class ItfTransformer(ABC):
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError


class ItfLoader(ABC):
    @abstractmethod
    def load(self, data: pd.DataFrame) -> None:
        raise NotImplementedError
