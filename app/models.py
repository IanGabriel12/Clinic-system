#ClinicControl: Iniciado em 24/10/19
class Endereco:
    def __init__(self, rua, cidade, estado, numero, id=None):
        self.id = id
        self.rua = rua
        self.cidade = cidade
        self.estado = estado
        self.numero = numero

class Pessoa:
    def __init__(self, nome, rg, endereco, telefone, id=None):
        self.id = id
        self.nome = nome
        self.rg = rg
        self.endereco = endereco
        self.telefone = telefone

class Funcionario(Pessoa):
    pass

class Enfermeiro(Funcionario):
    def __init__(self, nome, rg, endereco, telefones, ano_graduacao, nome_faculdade, titulo_tcc, id=None):
        super().__init__(nome, rg, endereco, telefones, id)
        self.ano_graduacao = ano_graduacao
        self.nome_faculdade = nome_faculdade
        self.titulo_tcc = titulo_tcc

class Medico(Funcionario):
    def __init__(self, nome, rg, endereco, telefones, crm, id=None):
        super().__init__(nome, rg, endereco, telefones, id)
        self.crm = crm

class Convenio:
    def __init__(self, sigla, nome, telefone, hospital, medicos, id=None):
        self.sigla = sigla
        self.nome = nome
        self.telefone = telefone
        self.hospital = hospital
        self.medicos = medicos

class Hospital:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco