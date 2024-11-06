class Inserts:
        
    def insertDefault():
        insertDefaultCliente = """
            REPLACE INTO cliente (id_cliente, nome, sexo, idade, nascimento) VALUES 
            (1, 'João Silva', 'm', 30, '1993-05-15'),
            (2, 'Maria Oliveira', 'f', 25, '1998-03-22'),
            (3, 'Carlos Santos', 'm', 40, '1983-07-11'),
            (4, 'Ana Souza', 'f', 28, '1995-01-30'),
            (5, 'Pedro Costa', 'm', 35, '1988-10-05'),
            (6, 'Bruna Ferreira', 'f', 22, '2001-08-15'),
            (7, 'Lucas Almeida', 'm', 27, '1996-12-10'),
            (8, 'Gabriela Pereira', 'f', 32, '1991-04-25'),
            (9, 'Fernando Rocha', 'm', 29, '1994-11-13'),
            (10, 'Juliana Lima', 'f', 31, '1992-06-08');
        """
        insertDefaultPrato = """
            REPLACE INTO prato (id_prato, nome, descricao, valor, disponibilidade) VALUES
            (1, 'Feijoada', 'Feijoada completa com carnes e acompanhamentos', 25.50, TRUE),
            (2, 'Moqueca de Peixe', 'Moqueca capixaba com peixe fresco', 32.00, TRUE),
            (3, 'Bife a Cavalo', 'Bife de carne com ovo frito', 22.00, TRUE),
            (4, 'Strogonoff de Frango', 'Frango ao molho de strogonoff', 20.00, FALSE),
            (5, 'Lasagna Bolonhesa', 'Lasagna com molho à bolonhesa', 28.50, TRUE),
            (6, 'Salada Caesar', 'Salada com alface, croutons e parmesão', 18.00, TRUE),
            (7, 'Sopa de Legumes', 'Sopa leve com legumes variados', 15.00, TRUE),
            (8, 'Pizza Marguerita', 'Pizza de queijo e tomate', 30.00, TRUE),
            (9, 'Bacalhau à Brás', 'Bacalhau com batata e ovo', 35.00, FALSE),
            (10, 'Picanha na Brasa', 'Picanha grelhada com acompanhamentos', 40.00, TRUE);
        """

        insertDefaultFornecedor = """
            REPLACE INTO fornecedor (id_fornecedor, nome, estado_origem) VALUES 
            (1, 'Sabor do Campo', 'SP'),
            (2, 'Distribuidora Nacional', 'RJ'),
            (3, 'Hortifruti SA', 'MG'),
            (4, 'Carne Certificada', 'RS'),
            (5, 'Delícias do Mar', 'PE'),
            (6, 'Gourmet Importados', 'PR'),
            (7, 'Padaria Brasil', 'BA'),
            (8, 'Super Alimentos', 'SC'),
            (9, 'Fazenda Orgânica', 'GO'),
            (10, 'Importadora Gourmet', 'ES');
        """
        insertDefaultIngredientes = """
            REPLACE INTO ingredientes (nome, data_fabricacao, data_validade, quantidade, observacao) VALUES 
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
            REPLACE INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) VALUES 
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
        insertDefaultUsos = """
            INSERT INTO usos (id_prato, id_ingrediente) VALUES
            (1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7), (4, 8), (5, 9), (5, 10);
        """
        insertList = (insertDefaultIngredientes, insertDefaultCliente, insertDefaultFornecedor, insertDefaultPrato, insertDefaultVenda, insertDefaultUsos)
        return insertList

    def newInsertCliente(nome, sexo, idade, nascimento):
        result = f"""
            INSERT INTO cliente (nome, sexo, idade, nascimento) VALUES
            ('{nome}', '{sexo}', {idade}, '{nascimento}')
        """
        return result
    
    def newInsertPrato(nome, descricao, valor, disponibilidade):
        result = f"""
            INSERT INTO prato (nome, descricao, valor, disponibilidade) VALUES
            ('{nome}', '{descricao}', {valor}, {disponibilidade})
        """
        return result

    def newInsertVenda(id_cliente, id_prato, quantidade, dia, hora, valor):
        result = f"""
            INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) VALUES
            ({id_cliente}, {id_prato}, {quantidade}, '{dia}', '{hora}', {valor})
        """
        return result
    
    def newInsertFornecedor(nome, estado_origem):
        result = f"""
            INSERT INTO fornecedor (nome, estado_origem) VALUES
            ('{nome}', '{estado_origem}')
        """
        return result
    
    def newInsertIngredientes(nome, data_fabricacao, data_validade, quantidade, observacao):
        result = f"""
            INSERT INTO ingredientes (nome, data_fabricacao, data_validade, quantidade, observacao) VALUES
            ('{nome}', '{data_fabricacao}', '{data_validade}', {quantidade}, '{observacao}')
        """
        return result
    
    def newInsertUsos(id_prato, id_ingrediente):
        result = f"""
            INSERT INTO usos (id_prato, id_ingrediente) VALUES
            ({id_prato}, {id_ingrediente})
        """
        return result