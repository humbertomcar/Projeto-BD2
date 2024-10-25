USE Restaurante;
-- inserindo valores para teste
INSERT INTO cliente (nome, sexo, idade, nascimento, pontos)
VALUES 
('João', 'm', 28, '1996-01-15', 0),
('Maria', 'f', 34, '1990-05-22', 0),
('Pedro', 'm', 45, '1979-09-10', 0);

-- inserindo valores para teste
INSERT INTO prato (nome, descricao, valor, disponibilidade)
VALUES 
('Lasanha', 'Lasanha de carne', 30.00, TRUE),
('Pizza', 'Pizza de quatro queijos', 25.00, TRUE),
('Salada', 'Salada Caesar', 15.00, TRUE);

-- Inserindo vendas (com diferentes pratos, quantidades e datas)
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor)
VALUES 
-- Vendas da Lasanha
(1, 1, 10, '2024-01-15', '12:30:00', 30.00),  -- Janeiro
(2, 1, 5, '2024-02-15', '13:00:00', 30.00),   -- Fevereiro
(3, 1, 20, '2024-03-15', '14:00:00', 30.00),  -- Março

-- Vendas da Pizza
(1, 2, 7, '2024-01-10', '12:45:00', 25.00),   -- Janeiro
(2, 2, 3, '2024-02-20', '12:50:00', 25.00),   -- Fevereiro

-- Vendas da Salada
(1, 3, 2, '2024-01-20', '13:00:00', 15.00),   -- Janeiro
(2, 3, 1, '2024-02-25', '13:15:00', 15.00),   -- Fevereiro
(3, 3, 4, '2024-03-18', '13:45:00', 15.00);   -- Março


DELIMITER $$

CREATE PROCEDURE Estatisticas_Vendas()
BEGIN
    -- Produto mais vendido
    SELECT p.nome AS 'Produto mais vendido'
    FROM venda v
    JOIN prato p ON v.id_prato = p.id
    GROUP BY v.id_prato
    ORDER BY SUM(v.quantidade) DESC
    LIMIT 1;

    -- Produto menos vendido
    SELECT p.nome AS 'Produto menos vendido'
    FROM venda v
    JOIN prato p ON v.id_prato = p.id
    GROUP BY v.id_prato
    ORDER BY SUM(v.quantidade) ASC
    LIMIT 1;

    -- Valor ganho com o produto mais vendido
    SELECT SUM(v.quantidade * v.valor) AS 'Valor ganho com o produto mais vendido'
    FROM venda v
    WHERE v.id_prato = (SELECT v2.id_prato FROM venda v2 GROUP BY v2.id_prato ORDER BY SUM(v2.quantidade) DESC LIMIT 1);

    -- Valor ganho com o produto menos vendido
    SELECT SUM(v.quantidade * v.valor) AS 'Valor ganho com o produto menos vendido'
    FROM venda v
    WHERE v.id_prato = (SELECT v2.id_prato FROM venda v2 GROUP BY v2.id_prato ORDER BY SUM(v2.quantidade) ASC LIMIT 1);

    -- Mês de maior vendas do produto mais vendido
    SELECT MONTH(v.dia) AS 'Mês de maior vendas do produto mais vendido'
    FROM venda v
    WHERE v.id_prato = (SELECT v2.id_prato FROM venda v2 GROUP BY v2.id_prato ORDER BY SUM(v2.quantidade) DESC LIMIT 1)
    GROUP BY MONTH(v.dia)
    ORDER BY SUM(v.quantidade) DESC
    LIMIT 1;

    -- Mês de menor vendas do produto mais vendido
    SELECT MONTH(v.dia) AS 'Mês de menor vendas do produto mais vendido'
    FROM venda v
    WHERE v.id_prato = (SELECT v2.id_prato FROM venda v2 GROUP BY v2.id_prato ORDER BY SUM(v2.quantidade) DESC LIMIT 1)
    GROUP BY MONTH(v.dia)
    ORDER BY SUM(v.quantidade) ASC
    LIMIT 1;

    -- Mês de maior vendas do produto menos vendido
    SELECT MONTH(v.dia) AS 'Mês de maior vendas do produto menos vendido'
    FROM venda v
    WHERE v.id_prato = (SELECT v2.id_prato FROM venda v2 GROUP BY v2.id_prato ORDER BY SUM(v2.quantidade) ASC LIMIT 1)
    GROUP BY MONTH(v.dia)
    ORDER BY SUM(v.quantidade) DESC
    LIMIT 1;

    -- Mês de menor vendas do produto menos vendido
    SELECT MONTH(v.dia) AS 'Mês de menor vendas do produto menos vendido'
    FROM venda v
    WHERE v.id_prato = (SELECT v2.id_prato FROM venda v2 GROUP BY v2.id_prato ORDER BY SUM(v2.quantidade) ASC LIMIT 1)
    GROUP BY MONTH(v.dia)
    ORDER BY SUM(v.quantidade) ASC
    LIMIT 1;
END$$

DELIMITER ;

CALL Estatisticas_Vendas();


