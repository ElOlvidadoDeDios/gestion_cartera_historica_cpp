CREATE TABLE dbo.fct_flow_diario (
    Fecha                   DATE              NOT NULL,
    CodAsesor               VARCHAR(20)       NOT NULL,
    CodAgencia              VARCHAR(10)       NOT NULL,
    Periodo                 AS (CONVERT(CHAR(6), Fecha, 112)) PERSISTED, -- Sincronizado para JOINs rápidos

    -- Métricas Reales transaccionales del día
    SaldoCarteraReal        DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    MontoColocacionReal     DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    NumColocacionesReal     INT               NOT NULL DEFAULT 0,
    MontoRepagoReal         DECIMAL(18,2)     NOT NULL DEFAULT 0.00,

    CONSTRAINT PK_fct_flow_diario PRIMARY KEY CLUSTERED (Fecha, CodAsesor),
    CONSTRAINT FK_fct_flow_dim_calendario FOREIGN KEY (Fecha) REFERENCES dbo.dim_calendario(Fecha),
    CONSTRAINT FK_fct_flow_dim_asesor FOREIGN KEY (CodAsesor, Periodo) REFERENCES dbo.dim_asesor(CodAsesor, Periodo),
    CONSTRAINT FK_fct_flow_dim_agencia FOREIGN KEY (CodAgencia) REFERENCES dbo.dim_agencia(CodAgencia)
);


USE DWH_Gestion_Cartera;
GO
ALTER TABLE dbo.fct_flow_diario ADD VariosReal DECIMAL(18,2) NOT NULL DEFAULT 0.00;
ALTER TABLE dbo.fct_flow_diario ADD TEAPonderadaReal DECIMAL(18,4) NOT NULL DEFAULT 0.0000;
GO