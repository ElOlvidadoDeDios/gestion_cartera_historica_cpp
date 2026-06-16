from src.core.config import DBConfig

# Consultas de extracción dinámicas parametrizadas por Periodo
QUERY_EXTRACT_ASESOR = f"""
SELECT Periodo, CodAsesor, AsesorNombresApellidos, Cargo, CodAgencia
FROM {DBConfig.VW_SRC_ASESOR}
WHERE Periodo = ?;
"""

QUERY_EXTRACT_STOCK = f"""
SELECT Periodo, CodAsesor, CodAgencia, SaldoTotalReal, SaldoMora9Real, 
       SaldoMora31Real, SaldoMora150Real, NumeroSociosReal, NumeroSociosAnterior, Varios, TEA
FROM {DBConfig.VW_SRC_STOCK} 
WHERE Periodo = ?;
"""

QUERY_EXTRACT_FLOW = f"""
SELECT Fecha, CodAsesor, CodAgencia, SaldoCarteraReal, MontoColocacionReal, 
       NumColocacionesReal, MontoRepagoReal, VariosReal, TEAPonderadaReal
FROM {DBConfig.VW_SRC_FLOW} 
WHERE CONVERT(CHAR(6), Fecha, 112) = ?;
"""

# Consultas Upsert (MERGE) - Garantizan la protección del histórico sin borrar días anteriores
QUERY_LOAD_ASESOR = f"""
MERGE {DBConfig.TBL_DWH_ASESOR} AS T
USING (SELECT ? AS CodAsesor, ? AS Periodo) AS S
ON (T.CodAsesor = S.CodAsesor AND T.Periodo = S.Periodo)
WHEN MATCHED THEN
    UPDATE SET T.AsesorNombresApellidos = ?, T.Cargo = ?, T.CodAgencia = ?
WHEN NOT MATCHED THEN
    INSERT (CodAsesor, Periodo, AsesorNombresApellidos, Cargo, CodAgencia)
    VALUES (S.CodAsesor, S.Periodo, ?, ?, ?);
"""

QUERY_LOAD_STOCK = f"""
MERGE {DBConfig.TBL_DWH_STOCK} AS T
USING (SELECT ? AS Periodo, ? AS CodAsesor) AS S
ON (T.Periodo = S.Periodo AND T.CodAsesor = S.CodAsesor)
WHEN MATCHED THEN
    UPDATE SET 
        T.CodAgencia = ?, T.SaldoTotalReal = ?, T.SaldoMora9Real = ?, 
        T.SaldoMora31Real = ?, T.SaldoMora150Real = ?, 
        T.NumeroSociosReal = ?, T.NumeroSociosAnterior = ?,
        T.Varios = ?, T.TEA = ?
WHEN NOT MATCHED THEN
    INSERT (Periodo, CodAsesor, CodAgencia, SaldoTotalReal, SaldoMora9Real, 
            SaldoMora31Real, SaldoMora150Real, NumeroSociosReal, NumeroSociosAnterior, Varios, TEA)
    VALUES (S.Periodo, S.CodAsesor, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

QUERY_LOAD_FLOW = f"""
MERGE {DBConfig.TBL_DWH_FLOW} AS T
USING (SELECT ? AS Fecha, ? AS CodAsesor) AS S
ON (T.Fecha = S.Fecha AND T.CodAsesor = S.CodAsesor)
WHEN MATCHED THEN
    UPDATE SET 
        T.CodAgencia = ?, T.SaldoCarteraReal = ?, T.MontoColocacionReal = ?, 
        T.NumColocacionesReal = ?, T.MontoRepagoReal = ?, T.VariosReal = ?, T.TEAPonderadaReal = ?
WHEN NOT MATCHED THEN
    INSERT (Fecha, CodAsesor, CodAgencia, SaldoCarteraReal, MontoColocacionReal, 
            NumColocacionesReal, MontoRepagoReal, VariosReal, TEAPonderadaReal)
    VALUES (S.Fecha, S.CodAsesor, ?, ?, ?, ?, ?, ?, ?);
"""
