WITH

CTE_cartera_moras AS (
SELECT * FROM gc_cartera_moras
),

CTE_duracion AS (
SELECT * FROM gc_duracion
)

SELECT
    T.Fecha,
    T.IdSAsesor,
    T.Cartera,
    T.Mora9,
    T.Mora31,
    ISNULL(NEXO_DUR.Duracion, 0) AS Duracion
FROM CTE_cartera_moras T
    LEFT JOIN CTE_duracion NEXO_DUR ON NEXO_DUR.Fecha=T.Fecha AND NEXO_DUR.IdSAsesor=T.IdSAsesor