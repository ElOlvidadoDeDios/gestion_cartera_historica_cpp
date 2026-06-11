import pandas as pd
import logging


class Transformer:
    @staticmethod
    def clean_asesor_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        logging.info("Limpiando datos de Asesores...")
        df = df.copy()
        df["Periodo"] = df["Periodo"].astype(str).str.strip()
        df["CodAsesor"] = df["CodAsesor"].astype(str).str.strip()
        df["AsesorNombresApellidos"] = (
            df["AsesorNombresApellidos"].astype(str).str.strip()
        )
        df["Cargo"] = df["Cargo"].astype(str).str.strip()
        df["CodAgencia"] = df["CodAgencia"].astype(str).str.strip()
        return df

    @staticmethod
    def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        logging.info("Iniciando depuracion de Stock Mensual...")
        df = df.copy()
        df["Periodo"] = df["Periodo"].astype(str).str.strip()
        df["CodAsesor"] = df["CodAsesor"].astype(str).str.strip()
        df["CodAgencia"] = df["CodAgencia"].astype(str).str.strip()

        decimals = [
            "SaldoTotalReal",
            "SaldoMora9Real",
            "SaldoMora31Real",
            "SaldoMora150Real",
        ]
        df[decimals] = df[decimals].fillna(0.00).astype(float)
        df["NumeroSociosReal"] = df["NumeroSociosReal"].fillna(0).astype(int)
        df["NumeroSociosAnterior"] = df["NumeroSociosAnterior"].fillna(0).astype(int)
        return df

    @staticmethod
    def clean_flow_data(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        logging.info("Iniciando depuracion de Flujo Diario...")
        df = df.copy()
        df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.date
        df["CodAsesor"] = df["CodAsesor"].astype(str).str.strip()
        df["CodAgencia"] = df["CodAgencia"].astype(str).str.strip()

        money_cols = ["SaldoCarteraReal", "MontoColocacionReal", "MontoRepagoReal"]
        df[money_cols] = df[money_cols].fillna(0.00).astype(float)
        df["NumColocacionesReal"] = df["NumColocacionesReal"].fillna(0).astype(int)
        return df
