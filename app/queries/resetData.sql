DROP DATABASE clinic;
CREATE DATABASE clinic;
USE clinic;
CREATE TABLE IF NOT EXISTS enderecos(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    rua VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    numero INT NOT NULL
);

CREATE TABLE IF NOT EXISTS funcionarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    rg VARCHAR(13) NOT NULL,
    telefone varchar(11) NOT NULL,
    tipo_funcionario VARCHAR(1),
    nome_faculdade VARCHAR(100),
    ano_graduacao INT(4),
    titulo_tcc VARCHAR(100),
    numero_crm INT,
    is_ocupado TINYINT(1),
    endereco_id INT NOT NULL,
    constraint fkEnderecoFuncionario FOREIGN KEY (endereco_id) references enderecos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pacientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    rg VARCHAR(13) NOT NULL,
    telefone VARCHAR(11) NOT NULL,
    endereco_id INT NOT NULL,
    CONSTRAINT fkEnderecoPaciente FOREIGN KEY (endereco_id) REFERENCES enderecos(id) ON DELETE CASCADE
);