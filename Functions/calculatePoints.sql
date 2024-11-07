USE Restaurante;

DELIMITER $$

CREATE FUNCTION Calculo_pontos(valor_compra DECIMAL)
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE pontos INT;
    SET pontos = FLOOR(valor_compra / 10);
    RETURN pontos;
END $$

DELIMITER ;

SELECT Calculo_pontos(40.53);