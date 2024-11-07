class ConstructProcedures:

    dropProcedureSorteio = "DROP PROCEDURE IF EXISTS Sorteio;"
    dropProcedureEstatisticas = "DROP PROCEDURE IF EXISTS Estatisticas_Vendas;"
    dropProcedureReajuste = "DROP PROCEDURE IF EXISTS Reajuste;"
    dropProcedureGastarPontos = "DROP PROCEDURE IF EXISTS Gastar_Pontos;"

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
            
        END
    """

    createProcedureGastarPontos = """

        CREATE PROCEDURE Gastar_pontos(IN id_cliente_input INT, IN id_prato_input INT)
        BEGIN
            DECLARE pontos_cliente INT;
            DECLARE valor_prato DECIMAL(10, 2);
            DECLARE pontos_necessarios INT;
            DECLARE diferenca_pontos INT;

            -- Verifica os pontos do cliente
            SELECT pontos INTO pontos_cliente
            FROM cliente
            WHERE id_cliente = id_cliente_input;

            -- Verifica o valor do prato
            SELECT valor INTO valor_prato
            FROM prato
            WHERE id_prato = id_prato_input;

            -- Calcula os pontos necessários para comprar o prato
            SET pontos_necessarios = CEIL(valor_prato);

            -- Verifica se o cliente tem pontos suficientes
            IF pontos_cliente >= pontos_necessarios THEN
                -- Calcula a diferença de pontos se sobrar
                SET diferenca_pontos = pontos_cliente - pontos_necessarios;

                -- Atualiza os pontos do cliente
                UPDATE cliente
                SET pontos = diferenca_pontos
                WHERE id_cliente = id_cliente_input;

                -- Registra a venda (exemplo de registro)
                INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor)
                VALUES (id_cliente_input, id_prato_input, 1, CURDATE(), CURTIME(), valor_prato);
            ELSE
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Pontos insuficientes para realizar a compra';
            END IF;
        END

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

    def dropProcedures():
        dropProceduresList = (ConstructProcedures.dropProcedureEstatisticas, ConstructProcedures.dropProcedureGastarPontos,
                              ConstructProcedures.dropProcedureReajuste, ConstructProcedures.dropProcedureSorteio)
        return dropProceduresList

    def createProcedures():
        proceduresList = (ConstructProcedures.createProcedureEstatisticas, ConstructProcedures.createProcedureGastarPontos,
                          ConstructProcedures.createProcedureReajuste, ConstructProcedures.createProcedureSorteio)
        return proceduresList