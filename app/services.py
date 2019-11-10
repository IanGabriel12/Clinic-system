from validacao import Validacao
import models
import pymysql as mysql

ID = 0
#PACIENTE
NOME = 1
RG = 2
TELEFONE = 3
ENDERECO_ID = 4
#ENDERECO
RUA = 1
CIDADE = 2
ESTADO = 3
NUMERO = 4

con = mysql.connect('localhost', 'root', 'root', 'clinic')
cursor = con.cursor()

def cadastrarPaciente(paciente):
    """recebe um objeto do tipo pessoa e cadastra no banco de dados"""
    cadastrarEndereco(paciente.endereco)
    cursor.execute(
        f'''INSERT INTO pacientes (nome, rg, telefone, endereco_id) VALUES
        ("{paciente.nome.title()}", "{paciente.rg}", "{paciente.telefone}", LAST_INSERT_ID())'''
    )
    con.commit()

def editarPaciente(paciente):
    editarEndereco(paciente.endereco)
    cursor.execute(
        f'''UPDATE pacientes SET nome="{paciente.nome.title()}", rg="{paciente.rg}", telefone="{paciente.telefone}"
        WHERE id={paciente.id}'''
    )
    con.commit()

def getPacientes():
    cursor.execute(f'''SELECT * FROM pacientes''')
    pacientes_bd = cursor.fetchall()
    pacientes = []

    for paciente_bd in pacientes_bd:
        endereco_bd = getEnderecoById(paciente_bd[ENDERECO_ID])
        endereco = models.Endereco(endereco_bd[RUA], endereco_bd[CIDADE], endereco_bd[ESTADO], endereco_bd[NUMERO],endereco_bd[ID])
        paciente = models.Pessoa(paciente_bd[NOME], paciente_bd[RG], endereco, paciente_bd[TELEFONE], paciente_bd[ID])
        pacientes.append(paciente)
    
    return pacientes
    
    
def cadastrarEndereco(endereco):
    """recebe um objeto do tipo endereco e cadastra no banco de dados"""
    cursor.execute(
        f'''INSERT INTO enderecos (rua, cidade, estado, numero) VALUES 
        ("{endereco.rua.title()}", "{endereco.cidade.title()}", "{endereco.estado.upper()}", "{endereco.numero}")'''
    )
    con.commit()

def editarEndereco(endereco):
    cursor.execute(
        f'''UPDATE enderecos SET rua="{endereco.rua.title()}", cidade="{endereco.cidade.title()}", estado="{endereco.estado.upper()}",
        numero="{endereco.numero}" WHERE id={endereco.id};'''
        )

    con.commit()

def getEnderecoById(id):
    cursor.execute(f'''SELECT * FROM enderecos WHERE id = {id}''')
    endereco_bd = cursor.fetchone()
    return endereco_bd


def cadastrarTelefones(telefones):
    """recebe uma lista de telefones e cadastra no banco de dados"""
    telefones = Validacao.validarTelefones(telefones)

def excluir(objeto):
    tabela = ''
    if isinstance(objeto, models.Pessoa):
        tabela = 'pacientes'
        posicao_fk = ENDERECO_ID
    
    # achar o objeto especifico
    cursor.execute(
        f'''SELECT * FROM {tabela} WHERE id = {objeto.id}'''
    )

    id_fk = cursor.fetchone()[posicao_fk] # id da foreign key

    #deletar o endereco especificado (consequentemente deletará o objeto)
    cursor.execute(
        f'''DELETE FROM enderecos WHERE id = {id_fk}'''
    )

    con.commit()
