class ConstructProcedures:

    dropProcedureSorteio = "DROP PROCEDURE IF EXISTS Sorteio;"
    dropProcedureEstatisticas = "DROP PROCEDURE IF EXISTS Estatisticas_Vendas;"
    dropProcedureReajuste = "DROP PROCEDURE IF EXISTS Reajuste;"
    dropProcedureGastarPontos = ""

    createProcedureEstatisticas = """
                -- PROCEDURE ESTATISTICAS
        
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
        END
    """

    createProcedureGastarPontos = """

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
    """


    createProcedureReajuste = """
    CREATE PROCEDURE Reajuste(IN reajuste_percentual DECIMAL(5, 2))
    BEGIN
        -- fazendo um aumento tomando como base o parametro dessa procedure (exemplo: caso o argumento seja 10, teria um aumento de 10%)
        UPDATE prato 
        SET valor = valor + (valor * (reajuste_percentual / 100));
    END
    """
    

    createProcedureSorteio = """

    CREATE PROCEDURE Sorteio()
    BEGIN
        DECLARE cliente_id INT;
        
        SELECT id_cliente INTO cliente_id
        FROM cliente
        ORDER BY RAND()
        LIMIT 1;
        
        UPDATE cliente
        SET pontos = pontos + 100
        WHERE id_cliente = cliente_id;
        
        SELECT nome AS 'Cliente Sorteado', pontos AS 'Pontos Atualizados'
        FROM cliente
        WHERE id_cliente = cliente_id;
    END
    
    """
