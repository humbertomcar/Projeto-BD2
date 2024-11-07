USE Restaurante;

CREATE VIEW VendasPorCliente AS
SELECT 
    c.nome AS nome_cliente,
    SUM(v.quantidade) AS total_vendas
FROM 
    cliente c
JOIN 
    venda v ON c.id_cliente = v.id_cliente
GROUP BY 
    c.nome;
  
SELECT * From VendasPorCliente;

CREATE VIEW TotalGastoPorCliente AS
SELECT 
    c.nome AS nome_cliente,
    SUM(v.valor) AS total_gasto
FROM 
    cliente c
JOIN 
    venda v ON c.id_cliente = v.id_cliente
GROUP BY 
    c.nome;

SELECT * FROM TotalGastoPorCliente;

CREATE VIEW ClientesComMaisPontos AS
SELECT 
    c.nome AS nome_cliente,
    c.pontos AS pontos_acumulados,
    COUNT(v.id_venda) AS total_vendas,
    SUM(v.valor) AS total_gasto
FROM 
    cliente c
JOIN 
    venda v ON c.id_cliente = v.id_cliente
GROUP BY 
    c.nome, c.pontos
ORDER BY 
    c.pontos DESC;

    
Select * from ClientesComMaisPontos;

