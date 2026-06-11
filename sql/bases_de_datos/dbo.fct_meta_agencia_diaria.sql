CREATE TABLE dbo.fct_meta_agencia_diaria (
    Fecha                   DATE              NOT NULL,
    CodAgencia              VARCHAR(10)       NOT NULL,
    
    -- ¡Agregado! Periodo automático persistido para navegación fluida en Power BI
    Periodo                 AS (CONVERT(CHAR(6), Fecha, 112)) PERSISTED, 

    -- Metas Diarias Manuales (Original vs Ajustada/Proyectada)
    ColocacionNumMeta       INT               NOT NULL DEFAULT 0,    
    ColocacionNumProy       INT               NOT NULL DEFAULT 0,    
    ColocacionMontoMeta     DECIMAL(18,2)     NOT NULL DEFAULT 0.00, 
    ColocacionMontoProy     DECIMAL(18,2)     NOT NULL DEFAULT 0.00, 

    CONSTRAINT PK_fct_meta_agencia_diaria PRIMARY KEY CLUSTERED (Fecha, CodAgencia),
    CONSTRAINT FK_meta_diaria_dim_calendario FOREIGN KEY (Fecha) REFERENCES dbo.dim_calendario(Fecha),
    CONSTRAINT FK_meta_diaria_dim_agencia FOREIGN KEY (CodAgencia) REFERENCES dbo.dim_agencia(CodAgencia)
);