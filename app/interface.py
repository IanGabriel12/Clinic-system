from tkinter import *
from validacao import Validacao
from functools import partial
import services
import models
class Interface:
    #posicionamento
    PADY = 10
    PADX = 15
    LISTAR_BUTTON_WIDTH = 5
    LISTAR_LABEL_WIDTH = 25
    TAMANHO_OBJETO_LISTA = 50 # Qualquer outro valor dá errado (Não sei porque)

    PADY_CADASTRO = 5

    #posição dos inputs de cadastro
    NOME = 0
    RG = 1
    RUA = 2
    CIDADE = 3
    ESTADO = 4
    NUMERO = 5
    TELEFONE = 6
    ERRO = 7
    BOTOES = 8

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

        #elementos
        botoes = [
            Button(self.main_container, text='Novo Paciente', command=lambda: self.renderFormulario(models.Pessoa)),
            Button(self.main_container, text='Listar Pacientes', command=lambda: self.listar(models.Pessoa)),
            Button(self.main_container, text='Novo Funcionário'),
            Button(self.main_container, text='Listar Funcionários'),
            Button(self.main_container, text='Novo Convênio'),
            Button(self.main_container, text='Listar Convênios'),
        ]

        textos = [
            Label(self.main_container, text='Pacientes:'),
            Label(self.main_container, text='Funcionários:'),
            Label(self.main_container, text='Convênios:'),
        ]

        linha = 0
        cont_botoes = 0
        for i in range(0,3):
            textos[i].grid(row=linha, column=0, columnspan=2, pady=self.PADY, padx=self.PADX)
            linha+=1
            for i in range(0,2):
                botoes[cont_botoes].grid(row=linha, column=i, pady=self.PADY, padx=self.PADX)
                cont_botoes += 1
            linha += 1
        
    def renderFormulario(self, classe, objeto=None, edit=False):
        '''Renderiza o formulário de uma classe (pessoa, funcionario, convenio)
        O formulário já vem preenchido se for para editar informações de uma pessoa existente
        '''

        campos = []
        if classe is models.Pessoa:
            #Colocados na ordem de aparição
            campos = [
                {'nome': 'Nome:', 'obs': '', 'tipo': Entry},
                {'nome': 'Rg:', 'obs': '*Apenas números', 'tipo': Entry},
                {'nome': 'Rua:', 'obs': '', 'tipo': Entry},
                {'nome': 'Cidade:', 'obs': '', 'tipo': Entry},
                {'nome': 'Estado:', 'obs': '*Sigla', 'tipo': Entry},
                {'nome': 'Número', 'obs': '', 'tipo': Entry},
                {'nome': 'Telefone:', 'obs': '', 'tipo': Entry},
            ]
        
        self.resetarTela()
        
        #criacao de um input para cada campo
        inputs = []
        for i in range(0,len(campos)):
            if campos[i]['tipo'] is Entry:
                inputs.append(Entry(self.main_container))
        
        #labels de indentificação
        labels = []
        for i in range(0,len(campos)):
            labels.append(Label(self.main_container))
            labels[-1]['text'] = campos[i]['nome']

        
        #Posicionamento dos objetos
        for i in range(0,len(campos)):
            labels[i].grid(row=i, column=0, pady=self.PADY_CADASTRO)
            inputs[i].grid(row=i, column=1, pady=self.PADY_CADASTRO)
        
        #labels de observação (n_linha, objeto)
        obs = [Label(self.main_container, text=campo['obs'], font='helvetica 10 italic') for campo in campos]
    
        for posicao, observacao in enumerate(obs):
            observacao.grid(row=posicao, column=2, pady=self.PADY_CADASTRO)

        
        # Comum a todos os objetos, aqui não é preciso mudar nada
        label_erro = Label(self.main_container)
        label_erro.grid(row=self.ERRO, column=0, columnspan=3)

        frame_botoes = Frame(self.main_container)
        frame_botoes.grid(row=self.BOTOES, column=0, columnspan=3)
        
        botoes = [
            Button(frame_botoes, text='Voltar', command=self.menuPrincipal),
            Button(frame_botoes, text='Cadastrar',command= lambda: self.cadastrarObjeto(inputs, label_erro, frame_botoes, classe))
        ]

        for posicao, botao in enumerate(botoes):
            botao.grid(row=0, column=posicao)
        
    
    def cadastrarObjeto(self, lista_inputs, label_erro, frame_botoes, classe):
        #Todos os objetos tem um endereço
        endereco = models.Endereco(
            lista_inputs[self.RUA].get().strip(),
            lista_inputs[self.CIDADE].get().strip(),
            lista_inputs[self.ESTADO].get().strip(),
            lista_inputs[self.NUMERO].get().strip()
        )
        
        #Na verificacao muda o tipo do objeto e seus métodos de cadastro e validação
        if classe is models.Pessoa:
            objeto = models.Pessoa(
                lista_inputs[self.NOME].get().strip(),
                lista_inputs[self.RG].get().strip(),
                endereco,
                lista_inputs[self.TELEFONE].get().strip()
            )
            metodo_validacao = Validacao.validarPessoa
            service_cadastro = services.cadastrarPessoa

        try:
            metodo_validacao(objeto)
            Validacao.validarEndereco(endereco)
            services.cadastrarPessoa(objeto)
            label_erro['fg'] = 'green'
            label_erro['text'] = 'Cadastrado com sucesso'
            frame_botoes.destroy()
            frame_botoes = Frame(self.main_container)
            frame_botoes.grid(row=self.BOTOES, column=0, columnspan=3)
            botao_voltar = Button(frame_botoes, text='Voltar', command=self.menuPrincipal)
            botao_voltar.grid(row=0, column=0)
              
        except Exception as e:
            label_erro['fg'] = 'red'
            label_erro['text'] = e
    
    def listar(self, classe):
        self.resetarTela()
        '''Serve para pacientes, funcionarios, ou convenios'''
       
        objetos = []
        if classe is models.Pessoa:
            objetos = services.getPacientes()     
        
        #Frame do canvas
        frame_canvas = Frame(self.main_container)
        frame_canvas.grid(row=0, column=0)

        #Canvas e o frame
        canvas = Canvas(frame_canvas)
        list_frame = Frame(canvas)
        
        list_frame.grid(row=0, column=0)
        
        canvas.pack(side=LEFT)

        #Barra de rolagem
        scrollbar = Scrollbar(frame_canvas, command=canvas.yview)
        scrollbar.pack(fill=Y, side=RIGHT)
        canvas.configure(yscrollcommand=scrollbar.set, scrollregion=(0,0,self.LARGURA, self.TAMANHO_OBJETO_LISTA*len(objetos)))


        for posicao, objeto in enumerate(objetos):
            frame_objeto = Frame(list_frame, height=self.TAMANHO_OBJETO_LISTA,)
            nome = Label(frame_objeto, text=objeto.nome, width=self.LISTAR_LABEL_WIDTH)
            botao_editar = Button(frame_objeto, text='Editar', width=self.LISTAR_BUTTON_WIDTH)
            botao_excluir = Button(frame_objeto, text='Excluir', command=partial(self.confirmarExclusao, objeto), width=self.LISTAR_BUTTON_WIDTH)
            
            nome.grid(row=0, column=0)
            botao_editar.grid(row=0, column=1)
            botao_excluir.grid(row=0, column=2)
            frame_objeto.grid(column=0, row=posicao, pady=self.PADY)
            

        canvas.create_window(0,0, anchor='nw', window=list_frame)
        botao_voltar = Button(self.main_container, text='Voltar', command=self.menuPrincipal)
        botao_voltar.grid(row=1, column=0)
              
    def confirmarExclusao(self, objeto):
        self.resetarTela()
        classe = ''

        if isinstance(objeto, models.Pessoa):
            classe = models.Pessoa
        
        frame_botoes = Frame(self.main_container)
        msg = Label(self.main_container, text=f'Tem certeza que deseja excluir {objeto.nome}')
        botao_sim = Button(frame_botoes, text='Sim', command=lambda: self.excluir(objeto, classe))
        botao_nao = Button(frame_botoes, text='Não', command=lambda: self.listar(classe))

        msg.grid(row=0, column=0)
        frame_botoes.grid(row=1, column=0)
        botao_sim.grid(row=0, column=0, padx=self.PADX)
        botao_nao.grid(row=0, column=1, padx=self.PADX)
    
    def excluir(self, objeto, classe):
        services.excluir(objeto)

        self.resetarTela()

        label = Label(self.main_container, text='Excluido com sucesso', fg='green')
        botao = Button(self.main_container, command=lambda: self.listar(classe))

        label.pack()
        botao.pack()
        
        
