GO
CREATE OR ALTER VIEW gc_colocacion WITH ENCRYPTION
AS

--- ############
--- NOTAS
--- ############

/*
- Sobre creditos extornados (improcedentes)
- Sobre creditos castigados
*/

--- ############
--- PREAMBULO
--- ############

--- ============
--- CTEs
WITH
--- ============

CTE AS (
------
SELECT
------
	T1.CUENTA,
	CAST(T1.OTORGA AS DATE) AS Fecha,
	T1.PAGARE,
	T2.ID_USER,
	T1.MONTO_PRESTAMO
------
FROM
------
    PRESTAMO                              T1
		INNER JOIN PREEC                  NEXO_PRE ON NEXO_PRE.CUENTA    = T1.CUENTA        AND NEXO_PRE.OTORGA      = T1.OTORGA AND NEXO_PRE.PAGARE = T1.PAGARE
		INNER JOIN SEGURIDAD.dbo.ANAREC   NEXO_ANA ON NEXO_ANA.ID_ANAREC = NEXO_PRE.ID_ANA  AND NEXO_ANA.FLAG_ANAREC = 'A'
		INNER JOIN SEGURIDAD.dbo.USUARIOS T2       ON T2.ID_USER         = NEXO_ANA.ID_USER
------
WHERE
------
	T1.TIPO_PROD     != '52'           AND
	FORMAT(T1.OTORGA, 'yyyyMM')  = FORMAT(GETDATE(), 'yyyyMM') AND
	NEXO_PRE.PERIODO =
		(
		SELECT MIN(A.PERIODO) FROM PREEC A WHERE A.CUENTA = NEXO_PRE.CUENTA AND A.OTORGA = NEXO_PRE.OTORGA AND A.PAGARE = NEXO_PRE.PAGARE
		)

)

--- ############
--- MAIN
--- ############

SELECT
	CAST(T.Fecha AS DATE) AS Fecha,
	T.ID_USER             AS IdSAsesor,
	COUNT(T.PAGARE)       AS [ColocacionNumReal],
	SUM(T.MONTO_PRESTAMO) AS [ColocacionMontoReal]
FROM
	CTE T
GROUP BY
	T.Fecha,
	T.ID_USER
--ORDER BY
--	T.Fecha,
--	T.ID_USER
GO
