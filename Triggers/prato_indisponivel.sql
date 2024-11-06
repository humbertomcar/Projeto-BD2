USE Restaurante;

DELIMITER $$

CREATE TRIGGER VerificaDisponibilidade
BEFORE INSERT ON venda
FOR EACH ROW
BEGIN
	DECLARE disp_prato BOOLEAN;

    -- Seleciona o valor de disponibilidade para o prato
    SELECT disponibilidade INTO disp_prato 
    FROM prato 
    WHERE id_prato = NEW.id_prato;

    IF disp_prato = 0 THEN
        -- Se o prato estiver indisponivel dispara o erro
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'O prato está indisponível, não é possível realizar a venda.';
    END IF;
END$$

DELIMITER ;

-- E pra funcionar essa aqui
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) 
VALUES (1, 1, 1, CURDATE(), CURTIME(), 25.00); 

-- Não é pra funcionar essa aqui
INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) 
VALUES (1, 3, 1, CURDATE(), CURTIME(), 18.00); -- Salada Caesar (indisponível)



