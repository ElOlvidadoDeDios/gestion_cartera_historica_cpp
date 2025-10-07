WITH

CTE_fechas AS (
SELECT DISTINCT A.Fecha, 1 AS Llave FROM gc_colocacion A
),

CTE_asesores AS (
SELECT DISTINCT A.IdSAgencia, A.IdSAsesor, 1 AS Llave FROM gc_dim_asesor A
),

CTE_producto_cartersiano AS (
SELECT
    CTE_fechas.Fecha,
    CTE_asesores.IdSAsesor,
    CTE_asesores.IdSAgencia
FROM CTE_fechas
    CROSS JOIN CTE_asesores
)

SELECT
    CTE_PC.Fecha,
    FORMAT(CTE_PC.Fecha, 'yyyyMM')          As Periodo,
    CTE_PC.IdSAsesor,
    CTE_PC.IdSAgencia,
    ISNULL(NEXO_COL.ColocacionNumReal, 0)   AS ColocacionNumReal,
    ISNULL(NEXO_COL.ColocacionMontoReal, 0) As ColocacionMontoReal,
    ISNULL(NEXO_REP.RepagoReal, 0)          As RepagoReal
FROM
    CTE_producto_cartersiano      CTE_PC
    LEFT OUTER JOIN gc_colocacion NEXO_COL ON NEXO_COL.Fecha = CTE_PC.Fecha AND NEXO_COL.IdSAsesor = CTE_PC.IdSAsesor
    LEFT OUTER JOIN gc_repago     NEXO_REP ON NEXO_REP.Fecha = CTE_PC.Fecha AND NEXO_REP.IdSAsesor = CTE_PC.IdSAsesor
ORDER BY
    CTE_PC.Fecha ASC,
    CTE_PC.IdSAgencia ASC,
    CTE_PC.IdSAsesor ASC
;
