CREATE DATABASE Restaurante;
USE Restaurante;

-- Tabela cliente
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    sexo ENUM('m', 'f', 'o') NOT NULL, -- Usando ENUM para sexo
    idade INT NOT NULL,
    nascimento DATE NOT NULL,
    pontos INT DEFAULT 0
);

-- Tabela prato
CREATE TABLE prato (
    id_prato INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    disponibilidade BOOLEAN NOT NULL -- Usando BOOLEAN diretamente
);

-- Tabela fornecedor
CREATE TABLE fornecedor (
    id_fornecedor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    estado_origem CHAR(2) NOT NULL,
    CONSTRAINT chk_estado_origem CHECK (estado_origem IN (
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 
        'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ))
);

-- Tabela ingredientes
CREATE TABLE ingredientes (
    id_ingrediente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    data_fabricacao DATE NOT NULL,
    data_validade DATE NOT NULL,
    quantidade INT NOT NULL,
    observacao TEXT
);

-- Tabela usos (relações entre prato e ingrediente)
CREATE TABLE usos (
    id_prato INT,
    id_ingrediente INT,
    PRIMARY KEY (id_prato, id_ingrediente),
    FOREIGN KEY (id_prato) REFERENCES prato(id_prato) ON DELETE CASCADE,
    FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente) ON DELETE CASCADE
);

-- Tabela venda
CREATE TABLE venda (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_prato INT,
    quantidade INT NOT NULL,
    dia DATE NOT NULL,
    hora TIME NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_prato) REFERENCES prato(id_prato) ON DELETE CASCADE
);
