USE Restaurante;

-- Inserindo apenas para testes
INSERT INTO prato (nome, descricao, valor, disponibilidade) 
VALUES 
('Lasanha', 'Lasanha de carne', 30.00, TRUE),
('Pizza', 'Pizza de quatro queijos', 25.00, TRUE),
('Salada', 'Salada Caesar', 15.00, TRUE);

-- Reajuste - Receba um reajuste em percentual e aumente o valor de todos os pratos.
DELIMITER $$

CREATE PROCEDURE Reajuste(IN reajuste_percentual DECIMAL(5, 2))
BEGIN
    -- fazendo um aumento tomando como base o parametro dessa procedure (exemplo: caso o argumento seja 10, teria um aumento de 10%)
    UPDATE prato 
    SET valor = valor + (valor * (reajuste_percentual / 100));
END$$

DELIMITER ;

-- Testando reajuste de 10%
CALL Reajuste(10);

-- Verifica os valores atualizados
SELECT * FROM prato;
