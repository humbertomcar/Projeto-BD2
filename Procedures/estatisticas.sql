USE Restaurante;

-- INSERTS PARA TESTES 

-- Tabela cliente
INSERT INTO cliente (nome, sexo, idade, nascimento, pontos) VALUES
('Carlos', 'm', 32, '1991-05-15', 100),
('Ana', 'f', 28, '1995-08-24', 200);

-- Tabela prato
INSERT INTO prato (nome, descricao, valor, disponibilidade) VALUES
('Pizza', 'Pizza de queijo com orégano', 30.00, TRUE),
('Hamburguer', 'Hamburguer de carne com queijo', 25.00, TRUE),
('Salada', 'Salada de folhas e legumes frescos', 15.00, TRUE);

-- Tabela fornecedor
INSERT INTO fornecedor (nome, estado_origem) VALUES
('Fornecedor SP', 'SP'),
('Fornecedor RJ', 'RJ');

-- Tabela ingredientes
INSERT INTO ingredientes (nome, data_fabricacao, data_validade, quantidade, observacao) VALUES
('Queijo', '2024-01-01', '2025-01-01', 50, 'Queijo fresco'),
('Carne', '2024-02-01', '2024-12-01', 30, 'Carne moída'),
('Folhas', '2024-01-10', '2024-03-10', 20, 'Folhas verdes frescas');

-- Tabela usos
INSERT INTO usos (id_prato, id_ingrediente) VALUES
(1, 1), -- Pizza usa Queijo
(2, 2), -- Hamburguer usa Carne
(3, 3); -- Salada usa Folhas

-- Vendas da Pizza
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) VALUES
(1, 1, 10, '2024-01-15', '12:30:00', 300.00), -- Janeiro
(1, 1, 5, '2024-02-10', '13:45:00', 150.00), -- Fevereiro
(1, 1, 20, '2024-03-05', '14:30:00', 600.00); -- Março

-- Vendas do Hamburguer
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) VALUES
(2, 2, 15, '2024-01-20', '15:00:00', 375.00), -- Janeiro
(2, 2, 7, '2024-02-15', '16:30:00', 175.00), -- Fevereiro
(2, 2, 3, '2024-03-18', '17:00:00', 75.00); -- Março


-- Vendas da Salada
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) VALUES
(1, 3, 2, '2024-01-22', '18:00:00', 30.00),  -- Janeiro
(1, 3, 8, '2024-02-25', '19:30:00', 120.00), -- Fevereiro
(1, 3, 4, '2024-03-12', '20:00:00', 60.00);  -- Março

-- PROCEDURE ESTATISTICAS
DELIMITER //

CREATE PROCEDURE Estatisticas_Vendas()
BEGIN
    DECLARE produto_mais_vendido INT;
    DECLARE produto_menos_vendido INT;

    -- criando uma tabela temporária para armazenar todos os resultados sem ela nao seria possivel exibir todos os resultados
    CREATE TEMPORARY TABLE IF NOT EXISTS resultado_estatisticas (
        descricao VARCHAR(255),
        valor VARCHAR(255)
    );

    -- Produto mais vendido
    SELECT id_prato INTO produto_mais_vendido
    FROM venda
    GROUP BY id_prato
    ORDER BY SUM(quantidade) DESC
    LIMIT 1;

    -- Produto menos vendido
    SELECT id_prato INTO produto_menos_vendido
    FROM venda
    GROUP BY id_prato
    ORDER BY SUM(quantidade) ASC
    LIMIT 1;

    -- Produto mais vendido (nome)
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Produto mais vendido', p.nome
    FROM prato p
    WHERE p.id_prato = produto_mais_vendido;

    -- Vendedor associado ao produto mais vendido
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Vendedor do produto mais vendido', c.nome
    FROM venda v
    JOIN cliente c ON v.id_cliente = c.id_cliente
    WHERE v.id_prato = produto_mais_vendido
    GROUP BY c.nome
    ORDER BY SUM(v.quantidade) DESC
    LIMIT 1;

    -- Produto menos vendido (nome)
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Produto menos vendido', p.nome
    FROM prato p
    WHERE p.id_prato = produto_menos_vendido;

    -- Valor ganho com o produto mais vendido
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Valor ganho com o mais vendido', SUM(v.valor)
    FROM venda v
    WHERE v.id_prato = produto_mais_vendido;

    -- Mês de maior venda do produto mais vendido
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Mês de maior venda do mais vendido', MONTH(dia)
    FROM venda
    WHERE id_prato = produto_mais_vendido
    GROUP BY MONTH(dia)
    ORDER BY SUM(quantidade) DESC
    LIMIT 1;

    -- Mês de menor venda do produto mais vendido
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Mês de menor venda do mais vendido', MONTH(dia)
    FROM venda
    WHERE id_prato = produto_mais_vendido
    GROUP BY MONTH(dia)
    ORDER BY SUM(quantidade) ASC
    LIMIT 1;

    -- Valor ganho com o produto menos vendido
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Valor ganho com o menos vendido', SUM(v.valor)
    FROM venda v
    WHERE v.id_prato = produto_menos_vendido;

    -- Mês de maior venda do produto menos vendido
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Mês de maior venda do menos vendido', MONTH(dia)
    FROM venda
    WHERE id_prato = produto_menos_vendido
    GROUP BY MONTH(dia)
    ORDER BY SUM(quantidade) DESC
    LIMIT 1;

    -- Mês de menor venda do produto menos vendido
    INSERT INTO resultado_estatisticas (descricao, valor)
    SELECT 'Mês de menor venda do menos vendido', MONTH(dia)
    FROM venda
    WHERE id_prato = produto_menos_vendido
    GROUP BY MONTH(dia)
    ORDER BY SUM(quantidade) ASC
    LIMIT 1;

    SELECT * FROM resultado_estatisticas;
	
    -- Limpando a tabela temporária
    DROP TEMPORARY TABLE resultado_estatisticas;
END //

DELIMITER ;

CALL Estatisticas_Vendas();

-- Tabela cliente
SELECT * FROM cliente;

-- Tabela prato
SELECT * FROM prato;

-- Tabela fornecedor
SELECT * FROM fornecedor;

-- Tabela ingredientes
SELECT * FROM ingredientes;

-- Tabela usos (relações entre prato e ingrediente)
SELECT * FROM usos;

-- Tabela venda
SELECT * FROM venda;
