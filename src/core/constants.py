# Mapeos explícitos para homologación de variables entre Origen y Destino
MAPA_AGENCIA = {
    "Periodo": "Periodo",
    "IdSAgencia": "CodAgencia",
    "CarteraInicial": "SaldoTotalReal",
    "MetaMoraCPP": "MetaMora9",
    "MetaMoraDeficiente": "MetaMora31",
}

MAPA_ASESOR = {
    "Periodo": "Periodo",
    "IdSAsesor": "CodAsesor",
    "CarteraInicial": "SaldoTotalReal",
    "Mora9Meta": "MetaMora9",
    "Mora31Meta": "MetaMora31",
}

# Consultas de extracción parametrizadas por Periodo (?) para optimizar velocidad
QUERY_EXTRACT_STOCK = """
SELECT Periodo, CodAsesor, CodAgencia, SaldoTotalReal, SaldoMora9Real, 
       SaldoMora31Real, SaldoMora150Real, NumeroSociosReal, NumeroSociosAnterior
FROM dbo.vw_dwh_fct_stock_mensual 
WHERE Periodo = ?;
"""

QUERY_EXTRACT_FLOW = """
SELECT Fecha, CodAsesor, CodAgencia, SaldoCarteraReal, MontoColocacionReal, 
       NumColocacionesReal, MontoRepagoReal
FROM dbo.vw_dwh_fct_flow_diario 
WHERE CONVERT(CHAR(6), Fecha, 112) = ?;
"""

# Consultas Upsert (MERGE) para la inyección limpia en el DWH local
QUERY_LOAD_STOCK = """
MERGE dbo.fct_stock_mensual AS T
USING (SELECT ? AS Periodo, ? AS CodAsesor) AS S
ON (T.Periodo = S.Periodo AND T.CodAsesor = S.CodAsesor)
WHEN MATCHED THEN
    UPDATE SET 
        T.CodAgencia = ?, T.SaldoTotalReal = ?, T.SaldoMora9Real = ?, 
        T.SaldoMora31Real = ?, T.SaldoMora150Real = ?, 
        T.NumeroSociosReal = ?, T.NumeroSociosAnterior = ?
WHEN NOT MATCHED THEN
    INSERT (Periodo, CodAsesor, CodAgencia, SaldoTotalReal, SaldoMora9Real, 
            SaldoMora31Real, SaldoMora150Real, NumeroSociosReal, NumeroSociosAnterior)
    VALUES (S.Periodo, S.CodAsesor, ?, ?, ?, ?, ?, ?, ?);
"""

QUERY_LOAD_FLOW = """
MERGE dbo.fct_flow_diario AS T
USING (SELECT ? AS Fecha, ? AS CodAsesor) AS S
ON (T.Fecha = S.Fecha AND T.CodAsesor = S.CodAsesor)
WHEN MATCHED THEN
    UPDATE SET 
        T.CodAgencia = ?, T.SaldoCarteraReal = ?, T.MontoColocacionReal = ?, 
        T.NumColocacionesReal = ?, T.MontoRepagoReal = ?
WHEN NOT MATCHED THEN
    INSERT (Fecha, CodAsesor, CodAgencia, SaldoCarteraReal, MontoColocacionReal, 
            NumColocacionesReal, MontoRepagoReal)
    VALUES (S.Fecha, S.CodAsesor, ?, ?, ?, ?, ?);
"""
