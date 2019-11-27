import time
class ClinicError(Exception):
    pass

class Validacao:
    @staticmethod
    def validarRg(rg):
        if rg == '':
            raise ClinicError('O campo "rg" é obrigatório')
        if not rg.isdigit():
            raise ClinicError('Rg deve conter apenas números')
        if len(rg) > 13:
            raise ClinicError('Rg deve conter no máximo 13 caracteres')
        return rg

    @staticmethod
    def validarNome(nome, nome_campo):
        limite_char = 100
        if nome == '':
            raise ClinicError(f'O campo "{nome_campo}" é obrigatório')
        if len(nome) > limite_char:
            raise ClinicError(f'O campo "{nome_campo}" não pode conter mais de {limite_char} caracteres')
        
        for letra in nome:
            if letra.isdigit():
                raise ClinicError(f'O campo "{nome_campo}" Não pode conter números')
        
        return nome
    
    def validarRua(rua):
        if rua == '':
            raise ClinicError(f'O campo "rua" é obrigatório')
        return rua
    
    @staticmethod
    def validarEstado(estado):
        ESTADOS = ['RN', 'PB', 'PE', 'SE', 'BA', 'MA', 'RO', 'AC', 'PR', 'SP', 'RJ', 'GO', 'MG', 'MT', 'MS']
        if estado == '':
            raise ClinicError('O campo "estado" é obrigatório')
        if estado.upper() not in ESTADOS:
            raise ClinicError('Não é um estado válido')

        return estado

    @staticmethod
    def validarTelefone(telefone):
        limite_digitos = 11
        if telefone == '':
            raise ClinicError('O campo "telefone" é obrigatório')
        if len(telefone) != limite_digitos:
            raise ClinicError(f'Telefone deve possuir {limite_digitos} dígitos')
        if not telefone.isdigit():
            raise ClinicError('Telefone deve conter apenas números')
        
        return telefone
    
    @staticmethod
    def validarNumero(numero):
        limite_digitos = 5
        if len(numero) > limite_digitos:
            raise ClinicError(f'O número da casa deve ter no máximo {limite_digitos} dígitos')
        if not numero.isdigit():
            raise ClinicError('O número da casa é inválido')
            
        return int(numero)
    
    @staticmethod
    def validarAno(ano):
        agora = time.gmtime(time.time())
        
        if ano == '':
            raise ClinicError('O campo "Ano de graduação é obrigatório')
        if not ano.isdigit():
            raise ClinicError('O campo "Ano de graduação deve conter apenas números"')
        if int(ano) > agora[0]: #0 é a posicao do ano
            raise ClinicError(f'O campo "Ano de graduação" não pode ser maior que {agora[0]}')

        return int(ano)
    
    @staticmethod
    def validarSigla(sigla):
        if len(sigla) > 10:
            raise ClinicError('A Sigla deve ter no máximo 10 caracteres.')

    @staticmethod
    def validarCRM(crm):
        tamanho_limite = 20
        if not crm.isdigit():
            raise ClinicError('O CRM deve conter apenas números.')
        if len(crm) > tamanho_limite:
            raise ClinicError(f'O CRM deve conter no máximo {tamanho_limite} dígitos.')
    
    @staticmethod
    def validarEspecializacoes(especializacoes):
        tamanho_especializacao = 200
        if len(especializacoes) > tamanho_especializacao:
            raise ClinicError(f'As especializacoes devem ter no máximo {tamanho_especializacao} caracteres')    
    
    @staticmethod
    def validarPessoa(pessoa):
        Validacao.validarNome(pessoa.nome, 'nome')
        Validacao.validarRg(pessoa.rg)
        if isinstance(pessoa.telefone, list):
            for telefone in pessoa.telefone:
                Validacao.validarTelefone(telefone)
        else:
            Validacao.validarTelefone(pessoa.telefone)
    
    @staticmethod
    def validarEndereco(endereco):
        Validacao.validarRua(endereco.rua) #rua
        Validacao.validarNome(endereco.cidade, 'cidade') #cidade
        Validacao.validarEstado(endereco.estado)
        Validacao.validarNumero(endereco.numero)
    
    @staticmethod
    def validarEnfermeiro(enfermeiro):
        Validacao.validarPessoa(enfermeiro)
        Validacao.validarAno(enfermeiro.ano_graduacao)
        Validacao.validarNome(enfermeiro.nome_faculdade, "Faculdade de graduação")
    
    @staticmethod
    def validarConvenio(convenio):
        Validacao.validarNome(convenio.nome, 'nome')
        Validacao.validarSigla(convenio.sigla)
        Validacao.validarTelefone(convenio.telefone)
    
    @staticmethod
    def validarMedico(medico):
        Validacao.validarPessoa(medico)
        Validacao.validarEspecializacoes(medico.especializacoes)
        Validacao.validarCRM(medico.crm)
