from validacao import Validacao
import models
import pymysql as mysql

ID = 0
#PACIENTE
NOME = 1
RG = 2
TELEFONE = 3
ENDERECO_PACIENTE = 4
#FUNCIONARIO
ENFERMEIRO = 'E'
LIMPEZA = 'L'
MEDICO = 'M'
TIPO_FUNCIONARIO = 4
NOME_FACULDADE = 5
ANO_GRADUACAO = 6
TITULO_TCC = 7
NUMERO_CRM = 8
IS_OCUPADO = 9
ENDERECO_FUNCIONARIO = 10

#ENDERECO
RUA = 1
CIDADE = 2
ESTADO = 3
NUMERO = 4

con = None
cursor = None
def conectarBD():
    global con
    con = mysql.connect('localhost', 'root', 'root', 'clinic')
    global cursor
    cursor = con.cursor()

def cadastrarPaciente(paciente):
    """recebe um objeto do tipo pessoa e cadastra no banco de dados"""
    cadastrarEndereco(paciente.endereco)
    try:
        cursor.execute(
            f'''INSERT INTO pacientes (nome, rg, telefone, endereco_id) VALUES
            ("{paciente.nome.title()}", "{paciente.rg}", "{paciente.telefone}", LAST_INSERT_ID())'''
        )
    except:
        cursor.execute(
            '''SELECT LAST_INSERT_ID()'''
        )
        id = cursor.fetchone()[0]
        con.close()
        endereco = getEnderecoById(id)
        excluir(endereco)
        return

    con.commit()
    con.close()

def editarPaciente(paciente):
    editarEndereco(paciente.endereco)
    conectarBD()
    cursor.execute(
        f'''UPDATE pacientes SET nome="{paciente.nome.title()}", rg="{paciente.rg}", telefone="{paciente.telefone}"
        WHERE id={paciente.id}'''
    )
    con.commit()
    con.close()

def getPacientes():
    conectarBD()
    cursor.execute(f'''SELECT * FROM pacientes''')
    pacientes_bd = cursor.fetchall()
    con.close()

    pacientes = []

    for paciente_bd in pacientes_bd:
        endereco = getEnderecoById(paciente_bd[ENDERECO_PACIENTE])
        paciente = models.Pessoa(paciente_bd[NOME], paciente_bd[RG], endereco, paciente_bd[TELEFONE], paciente_bd[ID])
        pacientes.append(paciente)

    return pacientes

def cadastrarEnfermeiro(enfermeiro):
    """recebe um objeto da classe enfermeiro e cadastra no banco de dados"""
    cadastrarEndereco(enfermeiro.endereco)
    try:
        cursor.execute(
            f'''INSERT INTO funcionarios (tipo_funcionario, nome, rg, telefone, nome_faculdade, ano_graduacao,
            titulo_tcc, endereco_id) VALUES ("E", "{enfermeiro.nome.title()}",
            "{enfermeiro.rg}", {enfermeiro.telefone},"{enfermeiro.nome_faculdade}", "{enfermeiro.ano_graduacao}",
            "{enfermeiro.titulo_tcc}", LAST_INSERT_ID())'''
        )
    except:
        cursor.execute(
            '''SELECT LAST_INSERT_ID()'''
        )
        id = cursor.fetchone()[0]
        con.close()
        endereco = getEnderecoById(id)
        excluir(endereco)
        return

    con.commit()
    con.close()

def editarEnfermeiro(enfermeiro):
    editarEndereco(enfermeiro.endereco)
    conectarBD()
    cursor.execute(
        f'''UPDATE funcionarios SET nome="{enfermeiro.nome}", rg="{enfermeiro.rg}", telefone="{enfermeiro.telefone}",
        nome_faculdade="{enfermeiro.nome_faculdade}", ano_graduacao="{enfermeiro.ano_graduacao}",
        titulo_tcc="{enfermeiro.titulo_tcc}" WHERE id = {enfermeiro.id}'''
    )
    con.commit()
    con.close()

def cadastrarFuncionarioLimpeza(funcionario):
    cadastrarEndereco(funcionario.endereco)
    try:
        cursor.execute(
            f'''INSERT INTO funcionarios (tipo_funcionario, nome, rg, telefone, endereco_id) 
            VALUES ("L", "{funcionario.nome.title()}",
            "{funcionario.rg}", "{funcionario.telefone}", LAST_INSERT_ID())'''
        )
    except:
        cursor.execute(
            '''SELECT LAST_INSERT_ID()'''
        )
        id = cursor.fetchone()[0]
        con.close()
        endereco = getEnderecoById(id)
        excluir(endereco)
        return

    con.commit()
    con.close()

def editarFuncionarioLimpeza(funcionario):
    editarEndereco(funcionario.endereco)
    conectarBD()
    cursor.execute(
        f'''UPDATE funcionarios SET nome="{funcionario.nome}", rg="{funcionario.rg}", 
        telefone="{funcionario.telefone}" WHERE id = {funcionario.id}'''
    )
    con.commit()
    con.close()

def getFuncionarios():
    conectarBD()
    cursor.execute('''SELECT * FROM funcionarios''')
    funcionarios_bd = cursor.fetchall()
    con.close()

    funcionarios = []
    faxineiros = []
    enfermeiros = []
    medicos = []

    for funcionario_bd in funcionarios_bd:
        endereco = getEnderecoById(funcionario_bd[ENDERECO_FUNCIONARIO])
        if funcionario_bd[TIPO_FUNCIONARIO] == LIMPEZA:
            faxineiro = models.Funcionario(funcionario_bd[NOME], funcionario_bd[RG], endereco,
            funcionario_bd[TELEFONE], funcionario_bd[ID])
            faxineiros.append(faxineiro)

        elif funcionario_bd[TIPO_FUNCIONARIO] == ENFERMEIRO:
            enfermeiro = models.Enfermeiro(funcionario_bd[NOME], funcionario_bd[RG], endereco,
            funcionario_bd[TELEFONE], funcionario_bd[ANO_GRADUACAO], funcionario_bd[NOME_FACULDADE],
            funcionario_bd[TITULO_TCC], funcionario_bd[ID])
            enfermeiros.append(enfermeiro)
        
        funcionarios.append(faxineiros)
        funcionarios.append(enfermeiros)
        funcionarios.append(medicos)
    
    return funcionarios
    
def cadastrarEndereco(endereco):
    """recebe um objeto do tipo endereco e cadastra no banco de dados"""
    conectarBD()
    cursor.execute(
        f'''INSERT INTO enderecos (rua, cidade, estado, numero) VALUES 
        ("{endereco.rua.title()}", "{endereco.cidade.title()}", "{endereco.estado.upper()}", "{endereco.numero}")'''
    )
    con.commit()

def editarEndereco(endereco):
    conectarBD()
    cursor.execute(
        f'''UPDATE enderecos SET rua="{endereco.rua.title()}", cidade="{endereco.cidade.title()}", estado="{endereco.estado.upper()}",
        numero="{endereco.numero}" WHERE id={endereco.id};'''
        )
    
    con.commit()
    con.close()


def getEnderecoById(id):
    conectarBD()
    cursor.execute(f'''SELECT * FROM enderecos WHERE id = {id}''')
    endereco_bd = cursor.fetchone()
    con.close()
    endereco = models.Endereco(endereco_bd[RUA], endereco_bd[CIDADE], endereco_bd[ESTADO], endereco_bd[NUMERO],endereco_bd[ID])
    return endereco #objeto do tipo Endereço

def excluir(objeto):
    conectarBD()

    if isinstance(objeto, models.Funcionario):
        posicao_fk = ENDERECO_FUNCIONARIO

        cursor.execute(
            f'''SELECT * FROM funcionarios WHERE id = {objeto.id}'''
        )
        endereco_id = cursor.fetchone()[posicao_fk]
    elif isinstance(objeto, models.Pessoa):
        posicao_fk = ENDERECO_PACIENTE
    
        # achar o objeto especifico
        cursor.execute(
            f'''SELECT * FROM pacientes WHERE id = {objeto.id}'''
        )

        endereco_id = cursor.fetchone()[posicao_fk] # id da foreign key
    elif isinstance(objeto, models.Endereco):
        endereco_id = objeto.id
    
        
    #deletar o endereco especificado (consequentemente deletará o objeto)
    cursor.execute(
        f'''DELETE FROM enderecos WHERE id = {endereco_id}'''
    )

    con.commit()
    con.close()
