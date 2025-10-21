GO
CREATE OR ALTER VIEW gc_dim_asesor WITH ENCRYPTION AS

--- ############
--- NOTAS
--- ############

--- ############
--- PREAMBLE
--- ############

--- ============
--- CTEs
WITH
--- ============

CTE AS (

------
SELECT
------

-- ID asesor
NEXO_ANA.ID_USER AS IdSAsesor,

--Nombre completo del asesor
NEXO_PER.RAZON AS AsesorNombresApellidos,

-- Cargo
NEXO_TCU.DESCRIP AS Cargo,

--ID Agencia
CASE
	WHEN T1.AGE_ANA = '98' THEN
		CASE
			WHEN RIGHT(RTRIM(NEXO_ANA.ID_USER), 1) = '6' THEN '06'
			WHEN RIGHT(RTRIM(NEXO_ANA.ID_USER), 1) = '7' THEN '07'
            -- Casos Excepcionales
            WHEN NEXO_ANA.ID_USER = 'RJULIACA' THEN '06'
		END
	ELSE NEXO_ANA.ID_AGE
END AS IdSAgencia

------
FROM
------
	PREEC                                   T1
    INNER JOIN PRESTAMO                     NEXO_PRE ON NEXO_PRE.CUENTA    = T1.CUENTA         AND NEXO_PRE.OTORGA      = T1.OTORGA AND NEXO_PRE.PAGARE = T1.PAGARE
	INNER JOIN SEGURIDAD.DBO.ANAREC         NEXO_ANA ON NEXO_ANA.ID_ANAREC = T1.ID_ANA         AND NEXO_ANA.FLAG_ANAREC = 'A'
	INNER JOIN SEGURIDAD.dbo.USUARIOS       NEXO_USU ON NEXO_USU.ID_USER   = NEXO_ANA.ID_USER
	INNER JOIN SEGURIDAD.dbo.GRUPOUSER      NEXO_GRU ON NEXO_GRU.ID_GRUPO  = NEXO_USU.ID_GRUPO
        INNER JOIN SEGURIDAD.dbo.PERSONAL   NEXO_PER ON NEXO_PER.DNI       = NEXO_USU.DNI
    INNER JOIN SEGURIDAD.dbo.TCARGO_USER    NEXO_TCU ON NEXO_TCU.ID_CARGO  = NEXO_PER.ID_CARGO
------
WHERE
------
	T1.PERIODO        = FORMAT(GETDATE(), 'yyyyMM') AND
	NEXO_GRU.ID_GRUPO =  '04' AND

--- Excluir asesores retirados
    NEXO_PRE.SALDO_PRES <> 0
	--- Implicancias:
	--- - Excluir repagos de asesores retirados
)

--- ############
--- MAIN
--- ############

SELECT DISTINCT
	IdSAsesor,
	AsesorNombresApellidos,
    Cargo,
	IdSAgencia
FROM
	CTE
--ORDER BY
--	IdSAgencia ASC,
--	IdSAsesor  ASC
GO