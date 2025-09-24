from abc import ABC, abstractmethod
import pandas as pd
from enum import Enum
from typing import Literal

# Producto
class Transformer(ABC):
    @abstractmethod
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

# Productos concretos

class TransformerDimAsesor(Transformer):

    @staticmethod
    def _quitar_asesores_atipicos(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df_new = df[df['IdSAgencia'].notna()]
        return df_new


    @staticmethod
    def _alias_asesor(var_name):
        apellidos, nombres = var_name.split(', ')
        iniciales_apellidos = ''.join([a[0].upper() for a in apellidos.split()])
        primer_nombre = nombres.split()[0].capitalize()
        return f"{primer_nombre} {iniciales_apellidos}"


    @staticmethod
    def _run_alias_asesor(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['Asesor'] = df['AsesorNombresApellidos'].apply(TransformerDimAsesor._alias_asesor)
        return df


    @staticmethod
    def run(df: pd.DataFrame) -> pd.DataFrame:
        df = TransformerDimAsesor._quitar_asesores_atipicos(df)
        df = TransformerDimAsesor._run_alias_asesor(df)
        return df


# Factory

class TypeTable(Enum):
    dim_asesor = 'dim_asesor'

class TransformerFactory:
    @staticmethod
    def get_transformer(type_table: Literal['dim_asesor']) -> Transformer:
        try:
            type_table = TypeTable(type_table)
        except ValueError:
            raise ValueError(f"Unsupported table type: {type_table}")

        if type_table is TypeTable.dim_asesor:
            return TransformerDimAsesor()


if __name__ == '__main__':
    pass