USE Restaurante;

CREATE USER 'administrador'@'localhost' IDENTIFIED BY '123';
GRANT ALL ON Restaurante.* TO 'administrador'@'localhost';

CREATE USER 'gerente'@'localhost' IDENTIFIED BY '123';
GRANT SELECT, UPDATE, DELETE ON Restaurante.* TO 'gerente'@'localhost';

CREATE USER 'funcionario'@'localhost' IDENTIFIED BY '123';
GRANT SELECT, INSERT ON Restaurante.* TO 'funcionario'@'localhost';
