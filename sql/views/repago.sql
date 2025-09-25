GO
CREATE OR ALTER VIEW gc_repago WITH ENCRYPTION
AS

--- ############
--- NOTAS
--- ############

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
	T1.FECHA_MOV,
	T1.CUENTA,
	T1.PAGARE,
	T1.OTORGA,
	T2.ID_USER,
	T1.CAPITAL
------
FROM
------
	PREMOV                          T1
		INNER JOIN PREEC            NEXO_PRE ON NEXO_PRE.CUENTA = T1.CUENTA       AND NEXO_PRE.PAGARE = T1.PAGARE AND NEXO_PRE.OTORGA = T1.OTORGA AND NEXO_PRE.PERIODO = FORMAT(GETDATE(), 'yyyyMM')
	INNER JOIN SEGURIDAD.dbo.ANAREC T2       ON T2.ID_ANAREC    = NEXO_PRE.ID_ANA AND T2.FLAG_ANAREC  = 'A'
------
WHERE
------
	FORMAT(T1.FECHA_MOV, 'yyyyMM') = FORMAT(GETDATE(), 'yyyyMM') AND
	T1.TIPO_MOV                    != '0001'                     AND
	NOT EXISTS (
		SELECT 1
		FROM PREMOV A
		WHERE
			A.FECHA_MOV = T1.FECHA_MOV AND
			A.COD_AGE   = T1.COD_AGE   AND
			A.COD_CAJA  = T1.COD_CAJA  AND
			A.TIPO_DOC  = T1.TIPO_DOC  AND
			A.NRO_DOC   = T1.NRO_DOC   AND
			LEFT(A.TIPO_MOV, 2) = '01'
	) AND
	T1.TIPO_DOC IN ('01','03') 

)

--- ############
--- MAIN
--- ############

SELECT
	CAST(T.FECHA_MOV AS DATE) AS Fecha,
	T.ID_USER                 AS IdSAsesor,
	SUM(T.CAPITAL)            AS RepagoReal
FROM CTE T
GROUP BY
	T.FECHA_MOV,
	T.ID_USER
--ORDER BY
--	Fecha    ASC,
--	IdSAsesor ASC
GO