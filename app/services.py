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
    conectarBD()
    editarEndereco(paciente.endereco)
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
        endereco = getEnderecoById(paciente_bd[ENDERECO_ID])
        paciente = models.Pessoa(paciente_bd[NOME], paciente_bd[RG], endereco, paciente_bd[TELEFONE], paciente_bd[ID])
        pacientes.append(paciente)

    return pacientes

def cadastrarEnfermeiro(enfermeiro):
    """recebe um objeto da classe enfermeiro e cadastra no banco de dados"""
    cadastrarEndereco(enfermeiro.endereco)
    try:
        cursor.execute(
            f'''INSERT INTO funcionarios (tipo_funcionario, nome, rg, nome_faculdade, ano_graduacao,
            titulo_tcc, endereco_id) VALUES ("E", "{enfermeiro.nome.title()}",
            "{enfermeiro.rg}", "{enfermeiro.nome_faculdade}", "{enfermeiro.ano_graduacao}",
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

    tabela = ''
    if isinstance(objeto, models.Pessoa):
        tabela = 'pacientes'
        posicao_fk = ENDERECO_ID
    
        # achar o objeto especifico
        cursor.execute(
            f'''SELECT * FROM {tabela} WHERE id = {objeto.id}'''
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
