WITH

CTE_CARTERA_MORAS AS (
SELECT * FROM gc_cartera_moras
),

CTE_DURACION AS (
SELECT * FROM gc_duracion
),

CTE_TEA AS (
SELECT * FROM gc_tea
)

SELECT
    T.Periodo,
    T.IdSAsesor,
    T.Cartera,
    T.Mora9,
    T.Mora31,
    T.Mora150,
    ISNULL(T_DUR.Varios, 0) AS Varios,
    ISNULL(T_TEA.TEA, 0) AS TEA
FROM
    CTE_CARTERA_MORAS T
    LEFT JOIN CTE_DURACION T_DUR
        ON  T_DUR.Periodo = T.Periodo
        AND T_DUR.IdSAsesor = T.IdSAsesor
    LEFT JOIN CTE_TEA T_TEA
        ON  T_TEA.Periodo = T.Periodo
        AND T_TEA.IdSAsesor = T.IdSAsesor