# Estatisticas

## Inserts que coloquei como base para teste:

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

-- Tabela venda
-- Estruturando para que não haja ambiguidade de vendas entre produtos e meses

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

- Produto mais vendido: Pizza, com 35 unidades no total (10 em Janeiro, 5 em Fevereiro, e 20 em Março).

- Vendedor associado ao produto mais vendido: Carlos, pois ele é o único a vender a Pizza.

- Produto menos vendido: Salada, com um total de 14 unidades.

- Valor ganho com o produto mais vendido: R$1.050,00 (soma das vendas da Pizza).

- Mês de maior e menor vendas do produto mais vendido:
 1. Mês de maior venda: Março, com 20 unidades.
 2. Mês de menor venda: Fevereiro, com 5 unidades.

- Valor ganho com o produto menos vendido: R$210,00 (soma das vendas da Salada).

- Mês de maior e menor vendas do produto menos vendido:

 1. Mês de maior venda: Fevereiro, com 8 unidades.
 2. Mês de menor venda: Janeiro, com 2 unidades.