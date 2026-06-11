CREATE TABLE dbo.dim_asesor (
    CodAsesor              VARCHAR(20)       NOT NULL, 
    Periodo                CHAR(6)           NOT NULL, -- Clave compuesta para congelar sucursal por mes
    AsesorNombresApellidos VARCHAR(150)      NOT NULL,
    Cargo                  VARCHAR(100)      NOT NULL,
    CodAgencia             VARCHAR(10)       NOT NULL, 
    CONSTRAINT PK_dim_asesor PRIMARY KEY CLUSTERED (CodAsesor, Periodo),
    CONSTRAINT FK_dim_asesor_dim_agencia FOREIGN KEY (CodAgencia) REFERENCES dbo.dim_agencia(CodAgencia)
);