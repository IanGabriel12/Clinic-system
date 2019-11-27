from tkinter import *
from tkinter import ttk
from validacao import Validacao
from functools import partial
import services
import models
class Interface:
    #posicionamento
    PADY_MENU_PRINCIPAL = 20
    PADX_MENU_PRINCIPAL = 10
    PADY = 10
    PADX = 15
    LISTAR_BUTTON_WIDTH = 5
    LISTAR_LABEL_WIDTH = 25
    TAMANHO_OBJETO_LISTA = 50 # Qualquer outro valor dá errado (Não sei porque)

    PADY_CADASTRO = 5

    #posição dos inputs de cadastro
    NOME = 0
    RG = 1
    SIGLA_CONVENIO = 1
    RUA = 2
    CIDADE = 3
    ESTADO = 4
    ESPECIALIZACOES = 7
    CRM = 8
    NUMERO = 5
    TELEFONE = 6
    ANO_GRADUACAO = 7
    NOME_FACULDADE = 8
    TITULO_TCC = 9

    def __init__(self, raiz, largura, altura):
        self.LARGURA = largura
        self.ALTURA = altura
        self.raiz = raiz
        self.main_container = Frame(raiz)
        self.main_container.pack()
        self.menuPrincipal()

    def resetarTela(self):
        self.main_container.destroy()
        self.main_container = Frame(self.raiz,)
        self.main_container.pack()

    def menuPrincipal(self):
        self.resetarTela()

        #Criação das abas
        abas = ttk.Notebook(self.main_container)
        frame_pacientes = Frame(abas)
        frame_funcionarios = Frame(abas)
        frame_convenios = Frame(abas)
        abas.pack(fill=BOTH)

        abas.add(frame_pacientes, text='Pacientes')
        abas.add(frame_funcionarios, text='Funcionários')
        abas.add(frame_convenios, text='Convênios')

        botoes = [
            Button(frame_pacientes, text='Cadastrar Paciente', command=lambda: self.renderFormulario(models.Pessoa)),
            Button(frame_pacientes, text='Lista de Pacientes', command=lambda: self.listar(models.Pessoa)),
            Button(frame_funcionarios, text='Cadastrar Funcionário', command=self.chooseFuncionarioFunction),
            Button(frame_funcionarios, text='Lista de Funcionários', command=lambda: self.listar(models.Funcionario)),
            Button(frame_convenios, text='Cadastrar Convênio', command=lambda: self.renderFormulario(models.Convenio)),
            Button(frame_convenios, text='Lista de Convênios', command=lambda: self.listar(models.Convenio)),
        ]

        coluna = 0
        for posicao, botao in enumerate(botoes):
            botoes[posicao].grid(row=0, column=coluna, pady=self.PADY_MENU_PRINCIPAL, padx=self.PADX_MENU_PRINCIPAL)
            if coluna == 0:
                coluna = 1
            else:
                coluna = 0
    
    def chooseFuncionarioFunction(self):
        self.resetarTela()

        titulo = Label(self.main_container, text='Selecione a função:')
        titulo.grid(row=0, column=0, pady=self.PADY)

        frame_botoes = Frame(self.main_container, bd=1, relief='solid')
        frame_botoes.grid(row=1, column=0, pady=self.PADY)

        botoes = [
            Button(frame_botoes, text='Limpeza', command= lambda: self.renderFormulario(models.Funcionario)),
            Button(frame_botoes, text='Médico', command=lambda: self.renderFormulario(models.Medico)),
            Button(frame_botoes, text='Enfermeiro', command=lambda: self.renderFormulario(models.Enfermeiro))
        ]

        for posicao, botao in enumerate(botoes):
            botao.grid(row=1, column=posicao+1, padx=self.PADX)
        
        frame_voltar = Frame(self.main_container)
        frame_voltar.grid(row=2, column=0, pady=self.PADY)

        botao_voltar = Button(frame_voltar, text='Voltar', command=self.menuPrincipal)
        botao_voltar.pack()

        
    def renderFormulario(self, classe, objeto=None, edit=False):
        '''Renderiza o formulário de uma classe (pessoa, funcionario, convenio)
        O formulário já vem preenchido se for para editar informações de uma pessoa existente
        '''
        campos = []
        dados = []
        id_endereco = None
        id_objeto = None
        if classe is models.Pessoa or classe is models.Funcionario:
            #Colocados na ordem de aparição
            campos = [
                {'nome': 'Nome:', 'obs': ''},
                {'nome': 'Rg:', 'obs': '*Apenas números'},
                {'nome': 'Rua:', 'obs': ''},
                {'nome': 'Cidade:', 'obs': ''},
                {'nome': 'Estado:', 'obs': '*Sigla'},
                {'nome': 'Número', 'obs': ''},
                {'nome': 'Telefone:', 'obs': ''},
            ]

            # Se passarmos um objeto como parâmetro, os dados já deverão estar preenchidos.
            if objeto != None:
                dados = [
                    objeto.nome, objeto.rg, objeto.endereco.rua,
                    objeto.endereco.cidade, objeto.endereco.estado,
                    objeto.endereco.numero, objeto.telefone
                ]
                id_objeto = objeto.id
                id_endereco = objeto.endereco.id
        elif classe is models.Enfermeiro:
            campos = [
                {'nome': 'Nome:', 'obs': ''},
                {'nome': 'Rg:', 'obs': '*Apenas números'},
                {'nome': 'Rua:', 'obs': ''},
                {'nome': 'Cidade:', 'obs': ''},
                {'nome': 'Estado:', 'obs': '*Sigla'},
                {'nome': 'Número', 'obs': ''},
                {'nome': 'Telefone:', 'obs': ''},
                {'nome': 'Ano da graduação:', 'obs':''},
                {'nome': 'Faculdade de graduação:', 'obs':''},
                {'nome': 'Título do TCC:', 'obs':''},
            ]

            if objeto != None:
                dados = [
                    objeto.nome, objeto.rg, objeto.endereco.rua,
                    objeto.endereco.cidade, objeto.endereco.estado,
                    objeto.endereco.numero, objeto.telefone, objeto.ano_graduacao,
                    objeto.nome_faculdade, objeto.titulo_tcc
                ]
                id_objeto = objeto.id
                id_endereco = objeto.endereco.id
        elif classe is models.Convenio:
            campos = [
                {'nome': 'Nome:', 'obs': ''},
                {'nome': 'Sigla:', 'obs': ''},
                {'nome': 'Rua:', 'obs': ''},
                {'nome': 'Cidade:', 'obs': ''},
                {'nome': 'Estado:', 'obs': '*Sigla'},
                {'nome': 'Número', 'obs': ''},
                {'nome': 'Telefone:', 'obs': ''},
            ]

            if objeto != None:
                dados = [
                    objeto.nome, objeto.sigla, objeto.endereco.rua, objeto.endereco.cidade,
                    objeto.endereco.estado, objeto.endereco.numero,
                    objeto.telefone,
                ]
                id_objeto = objeto.id
                id_endereco = objeto.endereco.id
        elif classe is models.Medico:
            campos = [
                {'nome': 'Nome:', 'obs': ''},
                {'nome': 'Rg:', 'obs': '*Apenas números'},
                {'nome': 'Rua:', 'obs': ''},
                {'nome': 'Cidade:', 'obs': ''},
                {'nome': 'Estado:', 'obs': '*Sigla'},
                {'nome': 'Número:', 'obs': ''},
                {'nome': 'Telefone(s):', 'obs': '*Separe-os usando ";"'},
                {'nome': 'Especializações:', 'obs': '*Separe-as usando ";"'},
                {'nome': 'N° CRM:', 'obs': ''},
            ]

            if objeto != None:
                dados = [
                    objeto.nome, objeto.rg, objeto.endereco.rua,
                    objeto.endereco.cidade, objeto.endereco.estado,
                    objeto.endereco.numero, ';'.join(objeto.telefone), objeto.especializacoes,
                    objeto.crm
                ]
                id_objeto = objeto.id
                id_endereco = objeto.endereco.id


        self.resetarTela()
        
        #criacao de um input para cada campo
        self.lista_inputs = []
        for i in range(0,len(campos)):
            self.lista_inputs.append(Entry(self.main_container))
            if edit:
                self.lista_inputs[-1].insert(0, dados[i])
        
        #labels de indentificação
        labels = []
        for i in range(0,len(campos)):
            labels.append(Label(self.main_container))
            labels[-1]['text'] = campos[i]['nome']

        
        #Posicionamento dos objetos
        for i in range(0,len(campos)):
            labels[i].grid(row=i, column=0, pady=self.PADY_CADASTRO)
            self.lista_inputs[i].grid(row=i, column=1, pady=self.PADY_CADASTRO)
        
        #labels de observação (n_linha, objeto)
        obs = [Label(self.main_container, text=campo['obs'], font='helvetica 10 italic') for campo in campos]
    
        for posicao, observacao in enumerate(obs):
            observacao.grid(row=posicao, column=2, pady=self.PADY_CADASTRO)

        
        # Comum a todos os objetos, aqui não é preciso mudar nada
        self.label_erro = Label(self.main_container)
        self.label_erro.grid(row=len(campos), column=0, columnspan=3)

        self.frame_botoes = Frame(self.main_container)
        self.frame_botoes.grid(row=len(campos)+1, column=0, columnspan=3)
        
        botoes = [
            Button(self.frame_botoes, text='Voltar'),
            Button(self.frame_botoes, text='Cadastrar', command= partial(self.alterarBancoDeDados,classe, edit, id_endereco, id_objeto))
        ]

        if edit:
            if isinstance(objeto, models.Funcionario):
                classe = models.Funcionario
            elif isinstance(objeto, models.Pessoa):
                classe = models.Pessoa
            botoes[0]['command'] = lambda: self.listar(classe)
        else:
            botoes[0]['command'] = self.menuPrincipal


        for posicao, botao in enumerate(botoes):
            botao.grid(row=0, column=posicao)
        
    
    def alterarBancoDeDados(self, classe, edit=False, id_endereco=None, id_objeto=None):
        '''
        Cadastra ou altera um objeto no banco de dados dependendo da variavel edit
        Este método cria um objeto da classe passada como parâmetro e utiliza um método de 
        services de edição ou de cadastro dependendo da variável edit, se ela for True é preciso
        passar os próximos dois parâmetros para identificarmos os objetos no BD;

        classe: classe no qual o objeto cadastrado é instância,
        edit: define se o serviço utilizado é de edição ou de cadastro,
        id_endereco: para editar precisamos passá-lo,
        id_objeto: também necessário para edição
        '''

        #Todos os objetos tem um endereço
        endereco = models.Endereco(
            self.lista_inputs[self.RUA].get().strip(),
            self.lista_inputs[self.CIDADE].get().strip(),
            self.lista_inputs[self.ESTADO].get().strip(),
            self.lista_inputs[self.NUMERO].get().strip(),
            id_endereco
        )
        objeto = None
        metodo_validacao = None
        servico = None
        
        #Na verificacao muda o tipo do objeto e seus métodos de cadastro e validação
        if classe is models.Pessoa:
            objeto = models.Pessoa(
                self.lista_inputs[self.NOME].get().strip(),
                self.lista_inputs[self.RG].get().strip(),
                endereco,
                self.lista_inputs[self.TELEFONE].get().strip(),
                id_objeto
            )

            metodo_validacao = Validacao.validarPessoa

            if edit:
                servico = services.editarPaciente
            else:
                servico = services.cadastrarPaciente
        elif classe is models.Funcionario:
            objeto = models.Funcionario(
                self.lista_inputs[self.NOME].get().strip(),
                self.lista_inputs[self.RG].get().strip(),
                endereco,
                self.lista_inputs[self.TELEFONE].get().strip(),
                id_objeto
            )

            metodo_validacao = Validacao.validarPessoa
            if edit:
                servico = services.editarFuncionarioLimpeza
            else:
                servico = services.cadastrarFuncionarioLimpeza
        elif classe is models.Enfermeiro:
            objeto = models.Enfermeiro(
                self.lista_inputs[self.NOME].get().strip(),
                self.lista_inputs[self.RG].get().strip(),
                endereco,
                self.lista_inputs[self.TELEFONE].get().strip(),
                self.lista_inputs[self.ANO_GRADUACAO].get().strip(),
                self.lista_inputs[self.NOME_FACULDADE].get().strip(),
                self.lista_inputs[self.TITULO_TCC].get().strip(),
                id_objeto
            )

            metodo_validacao = Validacao.validarEnfermeiro
            if edit:
                servico = services.editarEnfermeiro
            else:
                servico = services.cadastrarEnfermeiro
        elif classe is models.Convenio:
            objeto = models.Convenio(
                self.lista_inputs[self.NOME].get().strip(),
                self.lista_inputs[self.SIGLA_CONVENIO].get().strip(),
                endereco,
                self.lista_inputs[self.TELEFONE].get().strip(),
                id=id_objeto
            )
            metodo_validacao = Validacao.validarConvenio
            if edit:
                servico = services.editarConvenio
            else:
                servico = services.cadastrarConvenio
        elif classe is models.Medico:
            #caso termine com ';' o último caractere é retirado para não causar problemas
            telefones_string = self.lista_inputs[self.TELEFONE].get().strip()
            if telefones_string.endswith(';'):
                telefones_string = telefones_string[:-1]

            telefones = [telefone for telefone in telefones_string.split(';')]
            objeto = models.Medico(
                self.lista_inputs[self.NOME].get().strip(),
                self.lista_inputs[self.RG].get().strip(),
                endereco,
                telefones,
                self.lista_inputs[self.ESPECIALIZACOES].get().strip(),
                self.lista_inputs[self.CRM].get().strip(),
                id=id_objeto
            )

            metodo_validacao = Validacao.validarMedico

            if edit:
                servico = services.editarMedico
            else:
                servico = services.cadastrarMedico

        try:
            metodo_validacao(objeto)

            Validacao.validarEndereco(endereco)

            servico(objeto)

            self.label_erro['fg'] = 'green'
            self.label_erro['text'] = 'Cadastrado com sucesso'

            self.frame_botoes.destroy()
            self.frame_botoes = Frame(self.main_container)
            self.frame_botoes.grid(row=len(self.lista_inputs)+1, column=0, columnspan=3)
            botao_voltar = Button(self.frame_botoes, text='Voltar', command=self.menuPrincipal)
            botao_voltar.grid(row=0, column=0)
              
        except Exception as e:
            self.label_erro['fg'] = 'red'
            self.label_erro['text'] = e
    
    def listar(self, classe):
        self.resetarTela()
        '''Serve para pacientes, funcionarios, ou convenios'''
       
        objetos = []
        notebook = ttk.Notebook(self.main_container)
        abas = []
        if classe is models.Pessoa:
            objetos.append(services.getPacientes())
            abas.append(Frame(notebook))
            notebook.add(abas[0], text='Pacientes')   
        elif classe is models.Funcionario:
            objetos.extend(services.getFuncionarios())
            for i in range(0,3):
                abas.append(Frame(notebook))
            notebook.add(abas[0], text='Faxineiros')
            notebook.add(abas[1], text='Enfermeiros')
            notebook.add(abas[2], text='Médicos')
        elif classe is models.Convenio:
            objetos.append(services.getConvenios())
            abas.append(Frame(notebook))
            notebook.add(abas[0], text='Convênios')
        
        #Frame do canvas
        for posicao_aba, aba in enumerate(abas):
            frame_canvas = Frame(aba)
            frame_canvas.grid(row=0, column=0)

            #Canvas e o frame
            canvas = Canvas(frame_canvas)
            list_frame = Frame(canvas)
            
            list_frame.grid(row=0, column=0)
            
            canvas.pack(side=LEFT)

            #Barra de rolagem
            scrollbar = Scrollbar(frame_canvas, command=canvas.yview)
            scrollbar.pack(fill=Y, side=RIGHT)
            canvas.configure(yscrollcommand=scrollbar.set, scrollregion=(0,0,self.LARGURA, self.TAMANHO_OBJETO_LISTA*len(objetos[posicao_aba])))


            for posicao, objeto in enumerate(objetos[posicao_aba]):
                frame_objeto = Frame(list_frame, height=self.TAMANHO_OBJETO_LISTA,)
                nome = Label(frame_objeto, text=objeto.nome, width=self.LISTAR_LABEL_WIDTH)
                botao_editar = Button(frame_objeto, text='Editar', width=self.LISTAR_BUTTON_WIDTH, command=partial(self.renderFormulario, type(objeto), objeto, True))
                botao_excluir = Button(frame_objeto, text='Excluir', command=partial(self.confirmarExclusao, objeto), width=self.LISTAR_BUTTON_WIDTH)
                
                nome.grid(row=0, column=0)
                botao_editar.grid(row=0, column=1)
                botao_excluir.grid(row=0, column=2)
                frame_objeto.grid(column=0, row=posicao, pady=self.PADY)
                

            canvas.create_window(0,0, anchor='nw', window=list_frame)
        
        #botão para voltar
        notebook.grid(row=0, column=0)
        botao_voltar = Button(self.main_container, text='Voltar', command=self.menuPrincipal)
        botao_voltar.grid(row=1, column=0)
              
    def confirmarExclusao(self, objeto):
        self.resetarTela()
        if isinstance(objeto, models.Funcionario):
            classe = models.Funcionario
        elif isinstance(objeto, models.Pessoa):
            classe = models.Pessoa
        elif isinstance(objeto, models.Convenio):
            classe = models.Convenio
        
        self.frame_botoes = Frame(self.main_container)
        msg = Label(self.main_container, text=f'Tem certeza que deseja excluir {objeto.nome}')
        botao_sim = Button(self.frame_botoes, text='Sim', command=lambda: self.excluir(objeto, classe))
        botao_nao = Button(self.frame_botoes, text='Não', command=lambda: self.listar(classe))

        msg.grid(row=0, column=0)
        self.frame_botoes.grid(row=1, column=0)
        botao_sim.grid(row=0, column=0, padx=self.PADX)
        botao_nao.grid(row=0, column=1, padx=self.PADX)
    
    def excluir(self, objeto, classe):
        services.excluir(objeto)

        self.resetarTela()

        label = Label(self.main_container, text='Excluido com sucesso', fg='green')
        botao = Button(self.main_container, text='Voltar', command=lambda: self.listar(classe))

        label.pack()
        botao.pack()
        
        
