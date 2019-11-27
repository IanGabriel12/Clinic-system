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
    def __init__(self, nome, rg, endereco, telefone, ano_graduacao, nome_faculdade, titulo_tcc, id=None):
        super().__init__(nome, rg, endereco, telefone, id)
        self.ano_graduacao = ano_graduacao
        self.nome_faculdade = nome_faculdade
        self.titulo_tcc = titulo_tcc

class Medico(Funcionario):
    def __init__(self, nome, rg, endereco, telefones, especializacoes, crm, is_ocupado=False, id=None):
        super().__init__(nome, rg, endereco, telefones, id)
        self.especializacoes = especializacoes
        self.crm = crm
        self.is_ocupado = is_ocupado

class Convenio:
    def __init__(self, nome, sigla, endereco, telefone, medicos=[], id=None):
        self.nome = nome
        self.sigla = sigla
        self.endereco = endereco
        self.telefone = telefone
        self.medicos = medicos
        self.id = id
