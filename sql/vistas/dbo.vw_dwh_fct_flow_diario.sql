USE [TRANSACMIF];
GO

CREATE OR ALTER VIEW dbo.vw_dwh_fct_flow_diario
WITH ENCRYPTION 
AS
WITH CTE_Cartera_Base AS (
    SELECT 
        T_PRE.PERIODO AS Periodo,
        T_USU.ID_USER AS CodAsesor,
        -- Lógica de agencias integrada sin conflictos de GROUP BY
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
        T_PRE.SALDO_PRES AS SaldoCartera
    FROM dbo.PREEC T_PRE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU ON T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN SEGURIDAD.dbo.GRUPOUSER T_GRU ON T_GRU.ID_GRUPO = T_USU.ID_GRUPO AND T_GRU.NOM_GRUPO = 'CREDITOS'
    WHERE T_PRE.SALDO_PRES > 0
      AND T_USU.ID_USER NOT IN (
          'PRECASTIGO', 'RJULI6', 'RJULIACA', 'RLIMA7', 'RQUILLA3', 'RSICUA4',
          'LHR5', 'HTEJ5', 'TKPN5', 'GHVJ5', 'OTA5', 'SDHF5', 'CMN5', 'HQND5'
      )
),
CTE_Cartera_Historica AS (
    SELECT 
        Periodo,
        CodAsesor,
        CodAgencia,
        SUM(SaldoCartera) AS SaldoCarteraReal
    FROM CTE_Cartera_Base
    GROUP BY Periodo, CodAsesor, CodAgencia
),
CTE_Colocaciones_Diarias AS (
    SELECT 
        CAST(T_PTM.OTORGA AS DATE) AS Fecha,
        T_USU.ID_USER              AS CodAsesor,
        SUM(T_PTM.MONTO_PRESTAMO)  AS MontoColocacionReal,
        COUNT(T_PTM.PAGARE)        AS NumColocacionesReal
    FROM dbo.PRESTAMO T_PTM
    INNER JOIN dbo.PREEC T_PRE ON T_PRE.CUENTA = T_PTM.CUENTA AND T_PRE.OTORGA = T_PTM.OTORGA AND T_PRE.PAGARE = T_PTM.PAGARE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU ON T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN SEGURIDAD.dbo.GRUPOUSER T_GRU ON T_GRU.ID_GRUPO = T_USU.ID_GRUPO AND T_GRU.NOM_GRUPO = 'CREDITOS'
    WHERE T_PTM.TIPO_PROD <> '52'
      AND T_USU.ID_USER NOT IN (
          'PRECASTIGO', 'RJULI6', 'RJULIACA', 'RLIMA7', 'RQUILLA3', 'RSICUA4',
          'LHR5', 'HTEJ5', 'TKPN5', 'GHVJ5', 'OTA5', 'SDHF5', 'CMN5', 'HQND5'
      )
    GROUP BY CAST(T_PTM.OTORGA AS DATE), T_USU.ID_USER
),
CTE_Repagos_Diarios AS (
    SELECT 
        CAST(T_MOV.FECHA_MOV AS DATE) AS Fecha,
        T_USU.ID_USER                 AS CodAsesor,
        SUM(T_MOV.CAPITAL)            AS MontoRepagoReal
    FROM dbo.PREMOV T_MOV
    INNER JOIN dbo.PRESTAMO T_PTM ON T_PTM.CUENTA = T_MOV.CUENTA AND T_PTM.OTORGA = T_MOV.OTORGA AND T_PTM.PAGARE = T_MOV.PAGARE
    INNER JOIN dbo.PREEC T_PRE ON T_PRE.CUENTA = T_MOV.CUENTA AND T_PRE.OTORGA = T_MOV.OTORGA AND T_PRE.PAGARE = T_MOV.PAGARE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU ON T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN SEGURIDAD.dbo.GRUPOUSER T_GRU ON T_GRU.ID_GRUPO = T_USU.ID_GRUPO AND T_GRU.NOM_GRUPO = 'CREDITOS'
    WHERE T_MOV.TIPO_MOV != '0001' AND T_PTM.TIPO_PROD <> '52'
      AND T_USU.ID_USER NOT IN (
          'PRECASTIGO', 'RJULI6', 'RJULIACA', 'RLIMA7', 'RQUILLA3', 'RSICUA4',
          'LHR5', 'HTEJ5', 'TKPN5', 'GHVJ5', 'OTA5', 'SDHF5', 'CMN5', 'HQND5'
      )
    GROUP BY CAST(T_MOV.FECHA_MOV AS DATE), T_USU.ID_USER
),
CTE_Universo_Flow AS (
    SELECT Fecha, CodAsesor FROM CTE_Colocaciones_Diarias
    UNION
    SELECT Fecha, CodAsesor FROM CTE_Repagos_Diarios
)
SELECT 
    U.Fecha,
    U.CodAsesor,
    H.CodAgencia,
    ISNULL(H.SaldoCarteraReal, 0.00)    AS SaldoCarteraReal,
    ISNULL(C.MontoColocacionReal, 0.00) AS MontoColocacionReal,
    ISNULL(C.NumColocacionesReal, 0)    AS NumColocacionesReal,
    ISNULL(R.MontoRepagoReal, 0.00)     AS MontoRepagoReal
FROM CTE_Universo_Flow U
LEFT JOIN CTE_Colocaciones_Diarias C ON C.Fecha = U.Fecha AND C.CodAsesor = U.CodAsesor
LEFT JOIN CTE_Repagos_Diarios R ON R.Fecha = U.Fecha AND R.CodAsesor = U.CodAsesor
-- Cruce por periodo dinámico AAAAMM para heredar saldo de cartera viva y códigos de agencia oficiales
LEFT JOIN CTE_Cartera_Historica H ON H.CodAsesor = U.CodAsesor AND H.Periodo = CONVERT(CHAR(6), U.Fecha, 112)
WHERE H.CodAgencia IS NOT NULL; -- Excluye transacciones huerfanas de usuarios fuera del padrón oficial
GO