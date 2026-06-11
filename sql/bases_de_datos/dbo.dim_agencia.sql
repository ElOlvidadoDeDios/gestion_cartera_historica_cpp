CREATE TABLE dbo.dim_agencia (
    CodAgencia VARCHAR(10)       NOT NULL, -- Clave Primaria Natural
    NomAgencia VARCHAR(100)      NOT NULL,
    CONSTRAINT PK_dim_agencia PRIMARY KEY CLUSTERED (CodAgencia)
);