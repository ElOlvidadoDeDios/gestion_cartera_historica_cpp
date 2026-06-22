CREATE OR ALTER VIEW dbo.vw_dwh_fct_stock_mensual
WITH ENCRYPTION 
AS
WITH CTE_Base_Mensual AS (
    SELECT 
        T_PRE.PERIODO AS Periodo,
        T_USU.ID_USER AS CodAsesor,
        CASE
            WHEN T_ANA.ID_AGE = '98' THEN
                CASE
                    WHEN RIGHT(RTRIM(T_ANA.ID_USER), 1) = '6' THEN '06'
                    WHEN RIGHT(RTRIM(T_ANA.ID_USER), 1) = '7' THEN '07'
                    ELSE NULL
                END
            WHEN T_ANA.ID_AGE = '01' THEN
                CASE
                    WHEN RIGHT(RTRIM(T_ANA.ID_USER), 1) <> '9' THEN '01'
                    WHEN RIGHT(RTRIM(T_ANA.ID_USER), 1) = '9' THEN '09'
                END
            ELSE T_ANA.ID_AGE
        END AS CodAgencia,
        T_PRE.CUENTA,
        T_PRE.SALDO_PRES,
        T_PRE.DIAS_REALES
    FROM dbo.PREEC T_PRE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA 
        ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU 
        ON T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN SEGURIDAD.dbo.GRUPOUSER T_GRU 
        ON T_GRU.ID_GRUPO = T_USU.ID_GRUPO AND T_GRU.NOM_GRUPO = 'CREDITOS'
    WHERE T_PRE.SALDO_PRES > 0
      AND T_USU.ID_USER NOT IN (
          'PRECASTIGO', 'RJULI6', 'RJULIACA', 'RLIMA7', 'RQUILLA3', 'RSICUA4',
          'LHR5', 'HTEJ5', 'TKPN5', 'GHVJ5', 'OTA5', 'SDHF5', 'CMN5', 'HQND5'
      )
),
CTE_Metricas_Mensuales AS (
    SELECT 
        Periodo,
        CodAsesor,
        CodAgencia,
        SUM(SALDO_PRES) AS SaldoTotalReal,
        --SUM(CASE WHEN DIAS_REALES >= 9  THEN SALDO_PRES ELSE 0 END) AS SaldoMora9Real,
        SUM(CASE WHEN DIAS_REALES >= 4  THEN SALDO_PRES ELSE 0 END) AS SaldoMora9Real,
        SUM(CASE WHEN DIAS_REALES >= 31 THEN SALDO_PRES ELSE 0 END) AS SaldoMora31Real,
        SUM(CASE WHEN DIAS_REALES >= 151 THEN SALDO_PRES ELSE 0 END) AS SaldoMora150Real,
        COUNT(DISTINCT CUENTA) AS NumeroSociosReal
    FROM CTE_Base_Mensual
    GROUP BY Periodo, CodAsesor, CodAgencia
),
-- 👈 NUEVA SUB-METRICA: Plazo acumulado por Asesor
CTE_Duracion_Mensual AS (
    SELECT 
        T_PRE.PERIODO AS Periodo,
        T_USU.ID_USER AS CodAsesor,
        SUM(T_DED.CAPITAL) AS Varios
    FROM dbo.PRESTAMO T_PTM
    INNER JOIN dbo.PREEC T_PRE ON T_PRE.CUENTA = T_PTM.CUENTA AND T_PRE.OTORGA = T_PTM.OTORGA AND T_PRE.PAGARE = T_PTM.PAGARE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU ON T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN dbo.PRE_DEDUCESOLI T_DED ON T_PTM.PAGARE = T_DED.NRO_SOL AND T_DED.GLOSA = 'Cursos-Capacitación'
    WHERE T_PTM.TIPO_PROD <> '52'
    GROUP BY T_PRE.PERIODO, T_USU.ID_USER
),
-- 👈 NUEVA SUB-METRICA: TEA Promedio Ponderada por Asesor
CTE_TEA_Mensual AS (
    SELECT 
        T_PRE.PERIODO AS Periodo,
        T_USU.ID_USER AS CodAsesor,
        SUM(T_PTM.MONTO_PRESTAMO * T_PTM.TEA_INTERES) / NULLIF(SUM(T_PTM.MONTO_PRESTAMO), 0) AS TEA
    FROM dbo.PRESTAMO T_PTM
    INNER JOIN dbo.PREEC T_PRE ON T_PRE.CUENTA = T_PTM.CUENTA AND T_PRE.OTORGA = T_PTM.OTORGA AND T_PRE.PAGARE = T_PTM.PAGARE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU ON T_USU.ID_USER = T_ANA.ID_USER
    WHERE T_PTM.TIPO_PROD <> '52'
    GROUP BY T_PRE.PERIODO, T_USU.ID_USER
)
SELECT 
    M.Periodo,
    M.CodAsesor,
    M.CodAgencia,
    M.SaldoTotalReal,
    M.SaldoMora9Real,
    M.SaldoMora31Real,
    M.SaldoMora150Real,
    M.NumeroSociosReal,
    M.NumeroSociosAnterior,
    ISNULL(D.Varios, 0.00) AS Varios, -- Campo Plazo inyectado
    ISNULL(T.TEA, 0.0000)  AS TEA    -- Campo TEA inyectado
FROM (
    SELECT 
        M.*,
        ISNULL(LAG(M.NumeroSociosReal) OVER (PARTITION BY M.CodAsesor ORDER BY M.Periodo), 0) AS NumeroSociosAnterior
    FROM CTE_Metricas_Mensuales M
) M
LEFT JOIN CTE_Duracion_Mensual D ON D.Periodo = M.Periodo AND D.CodAsesor = M.CodAsesor
LEFT JOIN CTE_TEA_Mensual T ON T.Periodo = M.Periodo AND T.CodAsesor = M.CodAsesor;
GO