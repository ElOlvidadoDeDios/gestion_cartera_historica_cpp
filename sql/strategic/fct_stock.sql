WITH

CTE_cartera_moras AS (
SELECT * FROM gc_cartera_moras
),

CTE_duracion AS (
SELECT * FROM gc_duracion
)

SELECT
    T.Periodo,
    T.IdSAsesor,
    T.Cartera,
    T.Mora9,
    T.Mora31,
    ISNULL(NEXO_DUR.Varios, 0) AS Varios
FROM CTE_cartera_moras T
    LEFT JOIN CTE_duracion NEXO_DUR ON NEXO_DUR.Periodo=T.Periodo AND NEXO_DUR.IdSAsesor=T.IdSAsesor