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
    telefone varchar(11),
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

CREATE TABLE IF NOT EXISTS convenios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla VARCHAR(10) NOT NULL,
    telefone VARCHAR(11) NOT NULL,
    endereco_id INT NOT NULL,
    CONSTRAINT fkEnderecoConvenio FOREIGN KEY (endereco_id) REFERENCES enderecos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS telefones_medicos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    telefone VARCHAR(11) NOT NULL,
    medico_id INT NOT NULL,
    CONSTRAINT fkTelefoneMedico FOREIGN KEY (medico_id) REFERENCES funcionarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS medicos_convenios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    convenio_id INT NOT NULL,
    medico_id INT NOT NULL,
    CONSTRAINT fkConvenio FOREIGN KEY (convenio_id) REFERENCES convenios(id) ON DELETE CASCADE,
    CONSTRAINT fkMedico FOREIGN KEY (medico_id) REFERENCES funcionarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS consultas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    convenio_id INT NOT NULL,
    medico_id INT NOT NULL,
    descricao VARCHAR(200),
    dia INT(2) NOT NULL,
    mes INT(2) NOT NULL,
    hora INT(2) NOT NULL,
    CONSTRAINT fkConsultaPaciente FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    CONSTRAINT fkConsultaConvenio FOREIGN KEY (convenio_id) REFERENCES convenios(id) ON DELETE CASCADE,
    CONSTRAINT fkConsultaMedico FOREIGN KEY (medico_id) REFERENCES funcionarios(id) ON DELETE CASCADE
);