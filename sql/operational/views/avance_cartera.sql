GO
CREATE OR ALTER VIEW gc_avance_cartera WITH ENCRYPTION AS

--- ####################################################
--- ####################################################
--- ####################################################

--- ######################
--- NOTAS
--- ######################

--- ######################
--- PREAMBULO
--- ######################


--- ######################
--- MAIN
--- ######################

------------
SELECT
------------
	T_USU.ID_USER,
	T_SOC.RAZON_SOCIAL,
    T_SOC.TLF_CEL1,
    T_SOC.TLF_CEL2,
    T_SOC.TLF_FIJO1,
    T_SOC.TLF_FIJO2,
	CUOTAS_TOTAL = (
		SELECT
			COUNT(NRO_CUO)
		FROM PRECUO A
		WHERE
			A.CUENTA = T_PRE.CUENTA
			AND A.OTORGA = T_PRE.OTORGA
			AND A.PAGARE = T_PRE.PAGARE
	),
	CUOTAS_CANCELADOS = (
		SELECT
			COUNT(1)
		FROM PRECUO A
		WHERE
			A.CUENTA = T_PRE.CUENTA
			AND A.OTORGA = T_PRE.OTORGA
			AND A.PAGARE = T_PRE.PAGARE
			AND A.ESTADO = 8
	)
------------
FROM
------------
    PREEC T_PRE
	INNER JOIN PRESTAMO T_PTM
		ON  T_PTM.CUENTA = T_PRE.CUENTA
		AND T_PTM.OTORGA = T_PRE.OTORGA
		AND T_PTM.PAGARE = T_PRE.PAGARE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA
		ON  T_ANA.ID_ANAREC = T_PRE.ID_ANA
		AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU
		ON  T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN SEGURIDAD.dbo.GRUPOUSER T_GRU
		ON  T_GRU.ID_GRUPO = T_USU.ID_GRUPO
		AND T_GRU.NOM_GRUPO =  'CREDITOS'
	INNER JOIN SOCIOS T_SOC
		ON  T_SOC.CUENTA = T_PRE.CUENTA
------------
WHERE
------------
	T_PRE.PERIODO = FORMAT(GETDATE(), 'yyyyMM')
	AND T_PTM.SALDO_PRES > 0 -- Excluir creditos cancelados
--- ####################################################
--- ####################################################
--- ####################################################
GO