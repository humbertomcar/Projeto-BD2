USE Restaurante;

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
