class ConstructDB:
    
    createDatabase = "CREATE DATABASE IF NOT EXISTS Restaurante;"
    useDatabase = "USE Restaurante;"
    dropDatabase = "DROP DATABASE Restaurante;"

    createCliente = """

        -- Tabela cliente
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            sexo ENUM('m', 'f', 'o') NOT NULL, -- Usando ENUM para sexo
            idade INT NOT NULL,
            nascimento DATE NOT NULL,
            pontos INT DEFAULT 0
        );
        """
        
    createPrato = """   -- Tabela prato
        CREATE TABLE IF NOT EXISTS prato (
            id_prato INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            descricao TEXT NOT NULL,
            valor DECIMAL(10, 2) NOT NULL,
            disponibilidade BOOLEAN NOT NULL -- Usando BOOLEAN diretamente
        );
        """
        
    createFornecedor = """-- Tabela fornecedor
        CREATE TABLE IF NOT EXISTS fornecedor (
            id_fornecedor INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            estado_origem CHAR(2) NOT NULL,
            CONSTRAINT chk_estado_origem CHECK (estado_origem IN (
                'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 
                'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
            ))
        );
        """

    createIngredientes = """-- Tabela ingredientes
        CREATE TABLE IF NOT EXISTS ingredientes (
            id_ingrediente INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            data_fabricacao DATE NOT NULL,
            data_validade DATE NOT NULL,
            quantidade INT NOT NULL,
            observacao TEXT
        );
        """

    createUsos = """        -- Tabela usos (relações entre prato e ingrediente)
        CREATE TABLE IF NOT EXISTS usos (
            id_prato INT,
            id_ingrediente INT,
            PRIMARY KEY (id_prato, id_ingrediente),
            FOREIGN KEY (id_prato) REFERENCES prato(id_prato) ON DELETE CASCADE,
            FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente) ON DELETE CASCADE
        );
        """

    createVenda = """        -- Tabela venda
        CREATE TABLE IF NOT EXISTS venda (
            id_venda INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT,
            id_prato INT,
            quantidade INT NOT NULL,
            dia DATE NOT NULL,
            hora TIME NOT NULL,
            valor DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
            FOREIGN KEY (id_prato) REFERENCES prato(id_prato) ON DELETE CASCADE
        );  
        """
    
    createViews = """
        CREATE VIEW IF NOT EXISTS VendasPorCliente AS
        SELECT 
            c.nome AS nome_cliente,
            COUNT(v.id_venda) AS total_vendas
        FROM 
            cliente c
        JOIN 
            venda v ON c.id_cliente = v.id_cliente
        GROUP BY 
            c.nome;

        SELECT * FROM VendasPorCliente;
    """

    createProcedureSorteio = """
        DELIMITER $$

        CREATE PROCEDURE IF NOT EXISTS Sorteio()
        BEGIN
            DECLARE cliente_id INT;

            -- =pega um cliente aleatório
        SELECT id_cliente INTO cliente_id
        FROM cliente
        ORDER BY RAND()
            LIMIT 1;

        -- att os pontos do cliente sorteado com 100 pontos de premiação
        UPDATE cliente
        SET pontos = pontos + 100
        WHERE id_cliente = cliente_id;

        -- exibe o cliente sorteado e o novo saldo de pontos
        SELECT nome AS "Cliente Sorteado", pontos AS "Pontos Atualizados"
        FROM cliente
        WHERE id_cliente = cliente_id;
        END$$

        DELIMITER ;

        -- test do procedimento Sorteio
        CALL Sorteio();

        -- ve os pontos dos clientes após o sorteio
        SELECT * FROM cliente;
    """

    createProcedureReajuste = """
        -- Inserindo apenas para testes
        INSERT INTO prato (nome, descricao, valor, disponibilidade) 
        VALUES 
        ('Lasanha', 'Lasanha de carne', 30.00, TRUE),
        ('Pizza', 'Pizza de quatro queijos', 25.00, TRUE),
        ('Salada', 'Salada Caesar', 15.00, TRUE);

        -- Reajuste - Receba um reajuste em percentual e aumente o valor de todos os pratos.
        DELIMITER $$

        CREATE PROCEDURE Reajuste(IN reajuste_percentual DECIMAL(5, 2))
        BEGIN
            -- fazendo um aumento tomando como base o parametro dessa procedure (exemplo: caso o argumento seja 10, teria um aumento de 10%)
            UPDATE prato 
            SET valor = valor + (valor * (reajuste_percentual / 100));
        END$$

        DELIMITER ;

        -- Testando reajuste de 10%
        CALL Reajuste(10);

        -- Verifica os valores atualizados
        SELECT * FROM prato;
    """

    createProcedureGastarPontos = """
        DELIMITER $$

        CREATE PROCEDURE Gastar_pontos(
            IN id_cliente INT,
            IN id_prato INT
        )
        BEGIN
            DECLARE pontos_cliente INT;
            DECLARE valor_prato DECIMAL(10, 2);
            DECLARE pontos_utilizados INT;
            DECLARE pontos_restantes INT;

            -- pega o saldo de pontos do cliente
        SELECT pontos INTO pontos_cliente
        FROM cliente
        WHERE id_cliente = id_cliente;

        -- pega o valor do prato
        SELECT valor INTO valor_prato
        FROM prato
        WHERE id_prato = id_prato;

        -- calcula os pontos necessários para cobrir o valor do prato (1:1 em reais, arredondando para cima se necessário)
        SET pontos_utilizados = CEIL(valor_prato);

            -- ve se o cliente possui pontos suficientes
            IF pontos_cliente >= pontos_utilizados THEN
                -- calcula os pontos restantes após a compra
                SET pontos_restantes = pontos_cliente - pontos_utilizados;

                -- att o saldo de pontos do cliente
        UPDATE cliente
        SET pontos = pontos_restantes
        WHERE id_cliente = id_cliente;

        -- registra a venda como uma compra realizada com pontos
        INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor)
        VALUES (id_cliente, id_prato, 1, CURDATE(), CURTIME(), 0);

        -- mostra uma mensagem de confirmação e o saldo de pontos restantes
        SELECT 'Compra realizada com sucesso' AS mensagem, pontos_restantes AS "Pontos Restantes";
        ELSE
                -- ae o cliente não tiver pontos suficientes, exibe uma mensagem de erro
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Pontos insuficientes para completar a compra';
        END IF;

        END$$

        DELIMITER ;

        -- test do procedimento Gastar_pontos
        CALL Gastar_pontos(1, 1);

        -- ve o saldo de pontos do cliente após a compra
        SELECT * FROM cliente;

    """

    createProcedureEstatisticas = """
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
    """
    
    createUsers = """
        CREATE USER IF NOT EXISTS 'administrador'@'localhost' IDENTIFIED BY '123';
        GRANT ALL ON Restaurante.* TO 'administrador'@'localhost';

        CREATE USER IF NOT EXISTS 'gerente'@'localhost' IDENTIFIED BY '123';
        GRANT SELECT, UPDATE, DELETE ON Restaurante.* TO 'gerente'@'localhost';

        CREATE USER IF NOT EXISTS 'funcionario'@'localhost' IDENTIFIED BY '123';
        GRANT SELECT, INSERT ON Restaurante.* TO 'funcionario'@'localhost';
    """

    def constructTables():

        tableList = (ConstructDB.createCliente, ConstructDB.createFornecedor, ConstructDB.createIngredientes,   
                     ConstructDB.createPrato, ConstructDB.createUsos, ConstructDB.createVenda)
        return tableList

    
    def construct():
        componentsList = (ConstructDB.createViews, ConstructDB.createProcedureSorteio,
                          ConstructDB.createProcedureReajuste,ConstructDB.createProcedureGastarPontos,
                          ConstructDB.createProcedureEstatisticas, ConstructDB.createUsers)

        return componentsList