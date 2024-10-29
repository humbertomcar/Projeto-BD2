class DefaultInsert:

    def insertDefault():
        insertDefaultCliente = """
            INSERT INTO cliente (nome, sexo, idade, nascimento) VALUES 
            ('João Silva', 'm', 30, '1993-05-15'),
            ('Maria Oliveira', 'f', 25, '1998-03-22'),
            ('Carlos Santos', 'm', 40, '1983-07-11'),
            ('Ana Souza', 'f', 28, '1995-01-30'),
            ('Pedro Costa', 'm', 35, '1988-10-05'),
            ('Bruna Ferreira', 'f', 22, '2001-08-15'),
            ('Lucas Almeida', 'm', 27, '1996-12-10'),
            ('Gabriela Pereira', 'f', 32, '1991-04-25'),
            ('Fernando Rocha', 'm', 29, '1994-11-13'),
            ('Juliana Lima', 'f', 31, '1992-06-08');
        """
        insertDefaultPrato = """
            INSERT INTO prato (nome, descricao, valor, disponibilidade) VALUES 
            ('Feijoada', 'Feijoada completa com carnes e acompanhamentos', 25.50, TRUE),
            ('Moqueca de Peixe', 'Moqueca capixaba com peixe fresco', 32.00, TRUE),
            ('Bife a Cavalo', 'Bife de carne com ovo frito', 22.00, TRUE),
            ('Strogonoff de Frango', 'Frango ao molho de strogonoff', 20.00, FALSE),
            ('Lasagna Bolonhesa', 'Lasagna com molho à bolonhesa', 28.50, TRUE),
            ('Salada Caesar', 'Salada com alface, croutons e parmesão', 18.00, TRUE),
            ('Sopa de Legumes', 'Sopa leve com legumes variados', 15.00, TRUE),
            ('Pizza Marguerita', 'Pizza de queijo e tomate', 30.00, TRUE),
            ('Bacalhau à Brás', 'Bacalhau com batata e ovo', 35.00, FALSE),
            ('Picanha na Brasa', 'Picanha grelhada com acompanhamentos', 40.00, TRUE);
        """

        insertDefaultFornecedor = """
            INSERT INTO fornecedor (nome, estado_origem) VALUES 
            ('Sabor do Campo', 'SP'),
            ('Distribuidora Nacional', 'RJ'),
            ('Hortifruti SA', 'MG'),
            ('Carne Certificada', 'RS'),
            ('Delícias do Mar', 'PE'),
            ('Gourmet Importados', 'PR'),
            ('Padaria Brasil', 'BA'),
            ('Super Alimentos', 'SC'),
            ('Fazenda Orgânica', 'GO'),
            ('Importadora Gourmet', 'ES');
        """
        insertDefaultIngredientes = """
            INSERT INTO ingredientes (nome, data_fabricacao, data_validade, quantidade, observacao) VALUES 
            ('Feijão', '2024-01-10', '2025-01-10', 100, 'Feijão carioca selecionado'),
            ('Carne de Porco', '2024-02-15', '2024-08-15', 50, 'Carne fresca resfriada'),
            ('Peixe', '2024-03-12', '2024-09-12', 30, 'Peixe congelado'),
            ('Frango', '2024-05-18', '2024-11-18', 40, 'Frango caipira'),
            ('Tomate', '2024-06-01', '2024-07-15', 70, 'Tomates orgânicos'),
            ('Alface', '2024-06-05', '2024-07-10', 60, 'Alface crocante'),
            ('Batata', '2024-07-22', '2024-12-22', 120, 'Batatas frescas'),
            ('Ovo', '2024-08-11', '2024-10-11', 80, 'Ovos brancos grandes'),
            ('Arroz', '2024-09-30', '2025-09-30', 150, 'Arroz integral'),
            ('Picanha', '2024-10-15', '2025-04-15', 20, 'Picanha premium');
        """
        insertDefaultVenda = """
            INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) VALUES 
            (1, 1, 2, '2024-10-01', '12:30:00', 51.00),
            (2, 2, 1, '2024-10-02', '13:00:00', 32.00),
            (3, 3, 3, '2024-10-03', '19:15:00', 66.00),
            (4, 5, 1, '2024-10-04', '20:00:00', 28.50),
            (5, 6, 2, '2024-10-05', '11:30:00', 36.00),
            (6, 7, 1, '2024-10-06', '18:45:00', 15.00),
            (7, 8, 4, '2024-10-07', '14:20:00', 120.00),
            (8, 9, 1, '2024-10-08', '20:10:00', 35.00),
            (9, 10, 2, '2024-10-09', '12:00:00', 80.00),
            (10, 4, 3, '2024-10-10', '17:30:00', 60.00);
        """
        insertAll = f"""{insertDefaultCliente} {insertDefaultFornecedor}
        {insertDefaultIngredientes} {insertDefaultPrato}
        {insertDefaultVenda}"""

        return insertAll
        