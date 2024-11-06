USE Restaurante;

DELIMITER $$

CREATE PROCEDURE Sorteio()
BEGIN
    DECLARE id_cliente INT;

    -- pega um cliente aleatório
SELECT id_cliente INTO id_cliente
FROM cliente
ORDER BY RAND()
    LIMIT 1;

-- att os pontos do cliente sorteado com 100 pontos de premiação
UPDATE cliente
SET pontos = pontos + 100
WHERE id_cliente = id_cliente;

-- mostra o cliente sorteado e o novo saldo de pontos
SELECT nome AS "Cliente Sorteado", pontos AS "Pontos Atualizados"
FROM cliente
WHERE id_cliente = id_cliente;
END$$

DELIMITER ;

-- test do procedimento Sorteio
CALL Sorteio();

-- ve os pontos dos clientes após o sorteio
SELECT * FROM cliente;
