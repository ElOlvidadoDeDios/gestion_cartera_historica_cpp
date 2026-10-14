CREATE OR ALTER VIEW gc_socios_cpp WITH ENCRYPTION AS
WITH
-- =========================================================
-- 1. LÓGICA ORIGINAL INTACTA
-- =========================================================
CTE_AUX_SOCIOS AS (
    SELECT
        T_PRE.PERIODO,
        T_USU.ID_USER,
        COUNT(DISTINCT T_PRE.CUENTA) AS NroSocios
    FROM PREEC T_PRE
    INNER JOIN SEGURIDAD.DBO.ANAREC T_ANA ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU ON T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN SEGURIDAD.dbo.GRUPOUSER T_GRU ON T_GRU.ID_GRUPO = T_USU.ID_GRUPO AND T_GRU.NOM_GRUPO = 'CREDITOS'
    WHERE T_PRE.PERIODO IN ('{PERIODO_ANTERIOR}','{PERIODO_ACTUAL}')
      AND T_PRE.SALDO_PRES > 0 
    GROUP BY T_PRE.PERIODO, T_USU.ID_USER
),
CTE_AUX_SOCIOS_ANTERIORES AS (
    SELECT
        T.PERIODO,
        T.ID_USER,
        T.NroSocios,
        ISNULL(LAG(T.NroSocios) OVER(PARTITION BY T.ID_USER ORDER BY T.PERIODO), 0) AS NroSociosAnterior
    FROM CTE_AUX_SOCIOS T
),
-- =========================================================
-- 2. LÓGICA DE TRANSICIÓN (Mantenidos, Cancelados, etc.)
-- =========================================================
Cartera_Inicio AS (
    SELECT 
        T_PRE.CUENTA AS Codigo_Socio,
        T_ANA.ID_USER AS Asesor_Anterior
    FROM PREEC T_PRE WITH (NOLOCK)
    INNER JOIN SEGURIDAD.dbo.ANAREC T_ANA WITH (NOLOCK) ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    WHERE T_PRE.PERIODO = '{PERIODO_ANTERIOR}' AND T_PRE.SALDO_PRES > 0
    GROUP BY T_PRE.CUENTA, T_ANA.ID_USER
),
Cartera_Actual AS (
    SELECT 
        T_PRE.CUENTA AS Codigo_Socio,
        T_ANA.ID_USER AS Asesor_Actual,
        MAX(T_CAR.DESCRIP) AS Cargo_Actual
    FROM PREEC T_PRE WITH (NOLOCK)
    INNER JOIN SEGURIDAD.dbo.ANAREC T_ANA WITH (NOLOCK) ON T_ANA.ID_ANAREC = T_PRE.ID_ANA AND T_ANA.FLAG_ANAREC = 'A'
    INNER JOIN SEGURIDAD.dbo.USUARIOS T_USU WITH (NOLOCK) ON T_USU.ID_USER = T_ANA.ID_USER
    INNER JOIN SEGURIDAD.dbo.PERSONAL T_PER WITH (NOLOCK) ON T_PER.DNI = T_USU.DNI
    INNER JOIN SEGURIDAD.dbo.TCARGO_USER T_CAR WITH (NOLOCK) ON T_CAR.ID_CARGO = T_PER.ID_CARGO
    WHERE T_PRE.PERIODO = '{PERIODO_ACTUAL}' AND T_PRE.SALDO_PRES > 0
    GROUP BY T_PRE.CUENTA, T_ANA.ID_USER
),
CTE_TRANSICION AS (
    SELECT 
        I.Asesor_Anterior AS ID_USER,
        COUNT(DISTINCT CASE WHEN A.Asesor_Actual = I.Asesor_Anterior THEN I.Codigo_Socio END) AS Mantenidos,
        COUNT(DISTINCT CASE WHEN A.Codigo_Socio IS NULL THEN I.Codigo_Socio END) AS Cancelados,
        COUNT(DISTINCT CASE WHEN A.Cargo_Actual LIKE '%RECUPERADOR%' THEN I.Codigo_Socio END) AS Recuperacion,
        COUNT(DISTINCT CASE WHEN A.Asesor_Actual <> I.Asesor_Anterior AND A.Cargo_Actual NOT LIKE '%RECUPERADOR%' THEN I.Codigo_Socio END) AS Traspasados
    FROM Cartera_Inicio I
    LEFT JOIN Cartera_Actual A ON I.Codigo_Socio = A.Codigo_Socio
    GROUP BY I.Asesor_Anterior
),
-- =========================================================
-- 3. NUEVA LÓGICA: SOCIOS ACTIVOS DEL MES
-- =========================================================
Pagos_Del_Mes AS (
    SELECT DISTINCT M.CUENTA AS Codigo_Socio
    FROM PREMOV M WITH (NOLOCK)
    WHERE FORMAT(M.FECHA_MOV, 'yyyyMM') = '{PERIODO_ACTUAL}' -- Dinámico
      AND M.TIPO_MOV != '0001'      
      AND M.TIPO_DOC IN ('01','03') 
      AND NOT EXISTS (
          SELECT 1 FROM PREMOV REV WITH (NOLOCK)
          WHERE REV.FECHA_MOV = M.FECHA_MOV AND REV.COD_AGE = M.COD_AGE 
            AND REV.COD_CAJA = M.COD_CAJA AND REV.TIPO_DOC = M.TIPO_DOC 
            AND REV.NRO_DOC = M.NRO_DOC AND LEFT(REV.TIPO_MOV, 2) = '01'
      )
),
CTE_ACTIVOS AS (
    SELECT 
        A.Asesor_Actual AS ID_USER,
        COUNT(DISTINCT P.Codigo_Socio) AS NroSociosActivos
    FROM Cartera_Actual A
    INNER JOIN Pagos_Del_Mes P ON A.Codigo_Socio = P.Codigo_Socio
    GROUP BY A.Asesor_Actual
)
-- =========================================================
-- 4. RESULTADO FINAL (Unificando todo)
-- =========================================================
SELECT
    T.PERIODO AS Periodo,
    T.ID_USER AS IdSAsesor,
    T.NroSocios,
    T.NroSociosAnterior,
    ISNULL(TR.Mantenidos, 0) AS NroSociosMantenidos,
    ISNULL(TR.Cancelados, 0) AS NroSociosCancelados,
    ISNULL(TR.Recuperacion, 0) AS NroSociosRecuperacion,
    ISNULL(TR.Traspasados, 0) AS NroSociosTraspasados,
    -- Nuevo campo integrado
    ISNULL(ACT.NroSociosActivos, 0) AS NroSociosActivos
FROM CTE_AUX_SOCIOS_ANTERIORES T
LEFT JOIN CTE_TRANSICION TR ON T.ID_USER = TR.ID_USER
LEFT JOIN CTE_ACTIVOS ACT ON T.ID_USER = ACT.ID_USER
WHERE T.PERIODO = '{PERIODO_ACTUAL}';