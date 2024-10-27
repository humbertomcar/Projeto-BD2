USE Restaurante;

-- dados para teste
INSERT INTO cliente (nome, sexo, idade, nascimento, pontos)
VALUES
    ('João', 'm', 28, '1996-01-15', 0),
    ('Maria', 'f', 34, '1990-05-22', 0),
    ('Pedro', 'm', 45, '1979-09-10', 0);

DELIMITER $$

CREATE PROCEDURE Sorteio()
BEGIN
    DECLARE cliente_id INT;

    --   cliente random
SELECT id INTO cliente_id
FROM cliente
ORDER BY RAND()
    LIMIT 1;

-- att os pontos do cliente sorteado
UPDATE cliente
SET pontos = pontos + 100
WHERE id = cliente_id;

-- exibe o cliente sorteado
SELECT nome, pontos
FROM cliente
WHERE id = cliente_id;

END$$

DELIMITER ;

-- teste
CALL Sorteio();

-- ve os pontos dos clientes depossi
SELECT * FROM cliente;
