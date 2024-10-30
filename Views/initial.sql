USE Restaurante;

CREATE VIEW VendasPorCliente AS
SELECT 
    c.nome AS nome_cliente,
    COUNT(v.id_venda) AS total_vendas
FROM 
    cliente c
JOIN 
    venda v ON c.id_cliente = v.id_cliente
GROUP BY 
    c.nome;

SELECT * FROM VendasPorCliente