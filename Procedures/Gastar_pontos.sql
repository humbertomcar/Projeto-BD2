USE Restaurante;

--  dados para teste
INSERT INTO cliente (nome, sexo, idade, nascimento, pontos)
VALUES
    ('Carlos', 'm', 30, '1994-04-25', 50),
    ('Ana', 'f', 22, '2002-07-18', 80);

INSERT INTO prato (nome, descricao, valor, disponibilidade)
VALUES
    ('Hambúrguer', 'Hambúrguer clássico', 25.00, TRUE),
    ('Batata Frita', 'Porção de batata frita', 10.00, TRUE);

DELIMITER $$

CREATE PROCEDURE Gastar_pontos(
    IN id_cliente INT,
    IN id_prato INT
)
BEGIN
    DECLARE pontos_cliente INT;
    DECLARE valor_prato DECIMAL(10, 2);
    DECLARE pontos_utilizados INT;

    -- pontos do cliente
SELECT pontos INTO pontos_cliente
FROM cliente
WHERE id = id_cliente;

-- valor do prato
SELECT valor INTO valor_prato
FROM prato
WHERE id = id_prato;

-- calcuila pontos necessários
SET pontos_utilizados = CEIL(valor_prato);

    -- ve se o cliente tem pontos suficientes
    IF pontos_cliente >= pontos_utilizados THEN
        -- att o saldo de pontos do cliente
UPDATE cliente
SET pontos = pontos_cliente - pontos_utilizados
WHERE id = id_cliente;

-- registra a venda com o uso de pontos
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor)
VALUES (id_cliente, id_prato, 1, CURDATE(), CURTIME(), 0);
ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Pontos insuficientes para completar a compra';
END IF;

END$$

DELIMITER ;

-- teste
CALL Gastar_pontos(1, 1);

-- verifica o saldo de pontos do cliente depois
SELECT * FROM cliente;
