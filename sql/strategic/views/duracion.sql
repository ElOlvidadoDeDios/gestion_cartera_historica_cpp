GO
CREATE OR ALTER VIEW gc_duracion WITH ENCRYPTION AS

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
    --Periodo
    E.PERIODO,
    --ID del asesor
    NEXO_ANA.ID_USER,
    --Varios
    SUM(NEXO_DED.CAPITAL) AS VARIOS,
    --Numero de operaciones
    (SELECT COUNT(PAGARE) FROM PREEC WHERE FORMAT(OTORGA, 'yyyyMM') = FORMAT(GETDATE(), 'yyyyMM') AND ID_ANA=E.ID_ANA) AS NUMERO_OPERACIONES
------
FROM
------
    PREEC                           E
    INNER JOIN SEGURIDAD.DBO.ANAREC NEXO_ANA ON NEXO_ANA.ID_ANAREC = E.ID_ANA         AND NEXO_ANA.FLAG_ANAREC              =  'A'
    INNER JOIN PRESTAMO             NEXO_PRE ON NEXO_PRE.PAGARE    = E.PAGARE         AND FORMAT(NEXO_PRE.OTORGA, 'yyyyMM') = FORMAT(GETDATE(), 'yyyyMM')
    INNER JOIN PRE_DEDUCESOLI       NEXO_DED ON NEXO_PRE.PAGARE    = NEXO_DED.NRO_SOL AND GLOSA                             =  'Cursos-Capacitación'
------
WHERE
------
    PERIODO = FORMAT(GETDATE(), 'yyyyMM')
--------
GROUP BY
--------
    E.PERIODO,
    E.ID_ANA,
    NEXO_ANA.ID_USER

)

--- ############
--- MAIN
--- ############

SELECT
    T.PERIODO                             AS Periodo,
    T.ID_USER                             AS IdSAsesor,
    T.VARIOS							  AS Varios
FROM
    CTE T
GO
