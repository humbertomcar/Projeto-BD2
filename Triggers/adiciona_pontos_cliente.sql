USE Restaurante;

DELIMITER //

CREATE TRIGGER adiciona_pontos_cliente
AFTER INSERT ON venda
FOR EACH ROW
BEGIN
    -- atualiza os pontos do cliente quando a venda for acionada (1 ponto a cada 10 reais)
    UPDATE cliente
    SET pontos = pontos + FLOOR(NEW.valor / 10)
    WHERE id_cliente = NEW.id_cliente;
END //

DELIMITER ;