CREATE TABLE dbo.fct_stock_mensual (
    Periodo                 CHAR(6)           NOT NULL, -- AAAAMM
    CodAsesor               VARCHAR(20)       NOT NULL,
    CodAgencia              VARCHAR(10)       NOT NULL,

    -- Métricas Reales fijas mensuales
    SaldoTotalReal          DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    SaldoMora9Real          DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    SaldoMora31Real         DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    SaldoMora150Real        DECIMAL(18,2)     NOT NULL DEFAULT 0.00,
    NumeroSociosReal        INT               NOT NULL DEFAULT 0,
    NumeroSociosAnterior    INT               NOT NULL DEFAULT 0,
    Varios                  DECIMAL(18,2)     NOT NULL DEFAULT 0.00,   -- 👈 Agregado para Plazo
    TEA                     DECIMAL(18,4)     NOT NULL DEFAULT 0.0000, -- 👈 Agregado para Tasa

    CONSTRAINT PK_fct_stock_mensual PRIMARY KEY CLUSTERED (Periodo, CodAsesor),
    CONSTRAINT FK_fct_stock_dim_asesor FOREIGN KEY (CodAsesor, Periodo) REFERENCES dbo.dim_asesor(CodAsesor, Periodo),
    CONSTRAINT FK_fct_stock_dim_agencia FOREIGN KEY (CodAgencia) REFERENCES dbo.dim_agencia(CodAgencia)
);
GO