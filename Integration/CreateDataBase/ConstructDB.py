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

    

    createUserAdministrador = """
        CREATE USER IF NOT EXISTS 'administrador'@'localhost' IDENTIFIED BY '123';
        GRANT ALL ON Restaurante.* TO 'administrador'@'localhost';
    """
    createUserGerente = """
        CREATE USER IF NOT EXISTS 'gerente'@'localhost' IDENTIFIED BY '123';
        GRANT SELECT, UPDATE, DELETE ON Restaurante.* TO 'gerente'@'localhost';
    """

    createUserFuncionario = """
        CREATE USER IF NOT EXISTS 'funcionario'@'localhost' IDENTIFIED BY '123';
        GRANT SELECT, INSERT ON Restaurante.* TO 'funcionario'@'localhost';
    """

    createViewVendasPorCliente = """
        CREATE VIEW IF NOT EXISTS VendasPorCliente AS
        SELECT 
            c.nome AS nome_cliente,
            SUM(v.quantidade) AS total_vendas
        FROM 
            cliente c
        JOIN 
            venda v ON c.id_cliente = v.id_cliente
        GROUP BY 
            c.nome;
    """
    
    createViewTotalGastoPorCliente = """
        CREATE VIEW IF NOT EXISTS TotalGastoPorCliente AS
        SELECT 
            c.nome AS nome_cliente,
            SUM(v.valor) AS total_gasto
        FROM 
            cliente c
        JOIN 
            venda v ON c.id_cliente = v.id_cliente
        GROUP BY 
            c.nome;
    """

    createViewClientesEVendas = """
        CREATE VIEW IF NOT EXISTS ClientesEVendas AS
        SELECT 
            c.nome AS nome_cliente,
            COUNT(v.id_venda) AS total_vendas
        FROM 
            cliente c
        JOIN 
            venda v ON c.id_cliente = v.id_cliente
        GROUP BY 
            c.nome
        ORDER BY 
            c.nome ASC;
    """

    createViewClienteComMaisVendas = """
        CREATE VIEW IF NOT EXISTS ClientesComMaisPontos AS
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
    """

    createTriggerReduzirIngredientes = """
        CREATE TRIGGER IF NOT EXISTS reduzirIngredientes
        AFTER INSERT ON venda
        FOR EACH ROW
        BEGIN

            UPDATE ingredientes i
            JOIN usos u ON i.id_ingrediente = u.id_ingrediente
            SET i.quantidade = i.quantidade - (NEW.quantidade)
            WHERE u.id_prato = NEW.id_prato;
 
        END
    """

    createTriggerVerificaDisponibilidade = """
        CREATE TRIGGER IF NOT EXISTS VerificaDisponibilidade
        BEFORE INSERT ON venda
        FOR EACH ROW
        BEGIN
            DECLARE disp_prato BOOLEAN;

            -- Seleciona o valor de disponibilidade para o prato
            SELECT disponibilidade INTO disp_prato 
            FROM prato 
            WHERE id_prato = NEW.id_prato;

            IF disp_prato = 0 THEN
                -- Se o prato estiver indisponivel dispara o erro
                SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = 'O prato está indisponível, não é possível realizar a venda.';
            END IF;
        END
    """

    createTriggerAdicionaPontosCliente = """
        CREATE TRIGGER IF NOT EXISTS adiciona_pontos_cliente
        AFTER INSERT ON venda
        FOR EACH ROW
        BEGIN
            -- atualiza os pontos do cliente quando a venda for acionada (1 ponto a cada 10 reais)
            UPDATE cliente
            SET pontos = pontos + FLOOR(NEW.valor / 10)
            WHERE id_cliente = NEW.id_cliente;
        END
    """



    safeUpdateDisable = "SET SQL_SAFE_UPDATES = 0;"

    def createTriggers():
        triggersList = (ConstructDB.createTriggerAdicionaPontosCliente, ConstructDB.createTriggerReduzirIngredientes, ConstructDB.createTriggerVerificaDisponibilidade)
        return triggersList

    def createUsers():
        usersList = (ConstructDB.createUserAdministrador, ConstructDB.createUserGerente, ConstructDB.createUserFuncionario)
        return usersList

    def createViews():
        userViewsList = (ConstructDB.createViewVendasPorCliente, ConstructDB.createViewClientesEVendas, ConstructDB.createViewTotalGastoPorCliente,
                         ConstructDB.createViewClienteComMaisVendas)
        return userViewsList

    def createTables():

        tableList = (ConstructDB.createCliente, ConstructDB.createFornecedor, ConstructDB.createIngredientes,   
                     ConstructDB.createPrato, ConstructDB.createUsos, ConstructDB.createVenda, ConstructDB.safeUpdateDisable)
        return tableList
