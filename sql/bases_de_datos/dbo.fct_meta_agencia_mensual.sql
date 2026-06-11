CREATE TABLE dbo.fct_meta_agencia_mensual (
    Periodo                 CHAR(6)           NOT NULL, -- AAAAMM
    CodAgencia              VARCHAR(10)       NOT NULL,

    -- Metas Mensuales Manuales (Original vs Ajustada que lee Power BI)
    MetaAsesor              INT               NOT NULL DEFAULT 0,
    MetaAsesorAjus          INT               NOT NULL DEFAULT 0,
    MetaOpMes               INT               NOT NULL DEFAULT 0,    -- Cantidad de operaciones meta
    MetaOpMesAjus           INT               NOT NULL DEFAULT 0,
    MetaMonto               DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    MetaMontoAjus           DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    MetaCrecimiento         DECIMAL(18,2)     NOT NULL DEFAULT 0.00, -- Monto a colocar meta
    MetaCrecimientoAjus     DECIMAL(18,2)     NOT NULL DEFAULT 0.00, 
    
    -- Contención de Mora por Agencia (Valores fijos como 0.02 o 0.10)
    MetaMora9               DECIMAL(5,4)      NOT NULL DEFAULT 0.1000, 
    MetaMora31              DECIMAL(5,4)      NOT NULL DEFAULT 0.0200, 

    CONSTRAINT PK_fct_meta_agencia_mensual PRIMARY KEY CLUSTERED (Periodo, CodAgencia),
    CONSTRAINT FK_meta_mensual_dim_agencia FOREIGN KEY (CodAgencia) REFERENCES dbo.dim_agencia(CodAgencia)
);