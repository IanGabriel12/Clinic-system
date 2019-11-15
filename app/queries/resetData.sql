use clinic;
CREATE TABLE funcionarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    rg VARCHAR(13) NOT NULL,
    tipo_funcionario VARCHAR(1),
    nome_faculdade VARCHAR(100),
    ano_graduacao INT(4),
    titulo_tcc VARCHAR(100),
    numero_crm INT,
    is_ocupado TINYINT(1),
    endereco_id INT NOT NULL,
    constraint fk_endereco FOREIGN KEY (endereco_id) references enderecos(id)
);