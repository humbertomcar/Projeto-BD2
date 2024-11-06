USE Restaurante;

DELIMITER $$

CREATE PROCEDURE Gastar_pontos(
    IN id_cliente INT,
    IN id_prato INT
)
BEGIN
    DECLARE pontos_cliente INT;
    DECLARE valor DECIMAL(10, 2);
    DECLARE pontos_utilizados INT;
    DECLARE pontos_restantes INT;

    -- pega o saldo de pontos do cliente
SELECT pontos INTO pontos_cliente
FROM cliente
WHERE id_cliente = id_cliente;

-- pega o valor do prato
SELECT valor INTO valor
FROM prato
WHERE id_prato = id_prato;

-- calc os pontos necessários para cobrir o valor do prato
SET pontos_utilizados = CEIL(valor);

    -- Verifica se o cliente possui pontos suficientes
    IF pontos_cliente >= pontos_utilizados THEN
        -- Calcula os pontos restantes após a compra
        SET pontos_restantes = pontos_cliente - pontos_utilizados;

        -- Atualiza o saldo de pontos do cliente
UPDATE cliente
SET pontos = pontos_restantes
WHERE id_cliente = id_cliente;

-- reg a venda como uma compra realizada com pontos
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor)
VALUES (id_cliente, id_prato, 1, CURDATE(), CURTIME(), 0);

-- motra uma mensagem de confirmação e o saldo de pontos restantes
SELECT 'Compra realizada com sucesso' AS mensagem, pontos_restantes AS "Pontos Restantes";
ELSE
        -- se o cliente não tenha pontos suficientes, exibe uma mensagem de erro
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Pontos insuficientes para completar a compra';
END IF;

END$$

DELIMITER ;

-- test do procedimento Gastar_pontos
CALL Gastar_pontos(1, 1);

-- ve o saldo de pontos do cliente após a compra
SELECT * FROM cliente;
