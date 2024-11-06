USE Restaurante;

DELIMITER $$

CREATE TRIGGER reduzirIngredientes
AFTER INSERT ON venda
FOR EACH ROW
BEGIN

	UPDATE ingredientes i
	JOIN usos u ON i.id_ingrediente = u.id_ingrediente
	SET i.quantidade = i.quantidade - (NEW.quantidade)
	WHERE u.id_prato = NEW.id_prato;

    
END$$

DELIMITER ;

SELECT * FROM prato;

SELECT * FROM ingredientes;

INSERT INTO venda (id_cliente, id_prato, quantidade, dia, hora, valor) 
VALUES (1, 1, 2, CURDATE(), CURTIME(), 25.00);
