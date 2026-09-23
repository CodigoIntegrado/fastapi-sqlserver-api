IF DB_ID('CodigoIntegradoDB') IS NULL
BEGIN
    CREATE DATABASE CodigoIntegradoDB;
END
GO

USE CodigoIntegradoDB;
GO

IF OBJECT_ID('dbo.produto', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.produto
    (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        codigo      VARCHAR(20) NOT NULL UNIQUE,
        descricao   VARCHAR(150) NOT NULL,
        preco       DECIMAL(12,2) NOT NULL,
        estoque     INT NOT NULL DEFAULT 0,
        ativo       BIT NOT NULL DEFAULT 1,
        criado_em   DATETIME NOT NULL DEFAULT GETDATE()
    );
END
GO

INSERT INTO dbo.produto
    (codigo, descricao, preco, estoque)
VALUES
    ('1001', 'Mouse sem fio',      79.90, 25),
    ('1002', 'Teclado mecanico',  219.90, 10),
    ('1003', 'Monitor 24 polegadas', 899.00, 8);
GO

SELECT *
FROM dbo.produto;
GO