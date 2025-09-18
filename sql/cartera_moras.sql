--=============
--NOTAS
--=============

--=============
--PREAMBULO
--=============

---------------
--CTEs
WITH
---------------

CTE AS (
--CTE-INICIO. Cartera y Moras

------
SELECT
------

--Variables de agrupacion
  T1.PERIODO,
  T1.PAGARE,
  --Nombre completo del asesor
  DBO.OBT_NOMBRE_USER(
      (
        SELECT
          ID_USER
        FROM
          SEGURIDAD.DBO.ANAREC
        WHERE
          FLAG_ANAREC = 'A'        AND
          ID_AGE      = T1.AGE_ANA AND
          ID_ANAREC   = T1.ID_ANA
      ),
      'A'
  ) AS Asesor,
  --Agencia
  CASE
    WHEN T1.AGE_ANA = '98' THEN
      CASE
        WHEN RIGHT(RTRIM(NEXO_ANA.ID_USER), 1) = '6' THEN '06'
        WHEN RIGHT(RTRIM(NEXO_ANA.ID_USER), 1) = '7' THEN '07'
      END
    ELSE NEXO_ANA.ID_AGE
  END AS IdSAgencia,
  NEXO_ANA.ID_USER AS IdAsesor,

--Variables a ser agrupadas

  --Saldo capital que conforma la cartera
  T1.SALDO_PRES AS SaldoCapital,

  --Saldo capital en Mora CPP
  CASE
    WHEN T1.DIAS_REALES >= 9 THEN T1.SALDO_PRES
    ELSE 0
  END AS Mora9_SaldoCapital,

  --Saldo capital en Mora Deficiente
  CASE
    WHEN T1.DIAS_REALES >= 31 THEN T1.SALDO_PRES
    ELSE 0
  END AS Mora31_SaldoCapital

------
FROM
------
  PREEC                              T1
  INNER JOIN SEGURIDAD.DBO.ANAREC    NEXO_ANA ON NEXO_ANA.ID_ANAREC = T1.ID_ANA         AND NEXO_ANA.FLAG_ANAREC = 'A'
  INNER JOIN SEGURIDAD.dbo.USUARIOS  NEXO_USU ON NEXO_USU.ID_USER   = NEXO_ANA.ID_USER
  INNER JOIN SEGURIDAD.dbo.GRUPOUSER NEXO_GRU ON NEXO_GRU.ID_GRUPO  = NEXO_USU.ID_GRUPO
------
WHERE
------
  T1.PERIODO        >= FORMAT(GETDATE(), 'yyyyMM') AND
  NEXO_GRU.ID_GRUPO =  '04'

--CTE-FIN. Cartera y Moras
)

--==============
--MAIN
--==============

SELECT
  CAST(GETDATE() AS DATE)  AS Fecha,
  IdSAgencia,
  IdAsesor,
  Asesor,
  SUM(SaldoCapital)        AS Cartera,
  SUM(Mora9_SaldoCapital)  AS Mora9,
  SUM(Mora31_SaldoCapital) AS Mora31
FROM
  CTE
GROUP BY
  IdSAgencia,
  IdAsesor,
  Asesor
ORDER BY
  Fecha      ASC,
  IdSAgencia ASC,
  IdAsesor   ASC
;