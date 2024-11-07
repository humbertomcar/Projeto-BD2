USE Restaurante;

DELIMITER $$

CREATE TRIGGER verificaValidadeIngrediente
    AFTER UPDATE ON ingredientes
    FOR EACH ROW
BEGIN
    DECLARE validade_vencida BOOLEAN;

    -- ve se o ingrediente atualizado está vencido
    SET validade_vencida = (NEW.validade < CURDATE());

    IF validade_vencida THEN
        -- att a disponibilidade dospratos que usam o ingrediente vencido
    UPDATE prato 
        JOIN usos u ON p.id_prato = u.id_prato
        SET p.disponibilidade = 0
    WHERE u.id_ingrediente = NEW.id_ingrediente;
END IF;
END$$

DELIMITER ;

SELECT * FROM prato;

SELECT * FROM ingredientes;
