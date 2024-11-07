USE Restaurante;

DELIMITER $$

CREATE TRIGGER atualizaDisponibilidadePrato
    AFTER UPDATE ON ingredientes
    FOR EACH ROW
BEGIN
    -- Verifica se o ingrediente atualizado está vencido
    IF NEW.validade < CURDATE() THEN
        -- Atualiza a disponibilidade dos pratos que usam o ingrediente vencido para indisponível (0)
        UPDATE prato p
            JOIN usos u ON p.id_prato = u.id_prato
            SET p.disponibilidade = 0
        WHERE u.id_ingrediente = NEW.id_ingrediente;
    END IF;
END$$

DELIMITER ;

SELECT * FROM prato;
