class ClinicError(Exception):
    pass

class Validacao:
    @staticmethod
    def validarRg(rg):
        if rg == '':
            raise ClinicError('O campo "rg" é obrigatório')
        if not rg.isdigit():
            raise ClinicError('Rg deve conter apenas números')
        return rg

    @staticmethod
    def validarNome(nome, nome_campo):
        if nome == '':
            raise ClinicError(f'O campo "{nome_campo}" é obrigatório')
        
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
        if telefone == '':
            raise ClinicError('O campo "telefone" é obrigatório')
        if len(telefone) != 11:
            raise ClinicError('Telefone deve possuir 11 dígitos')
        if not telefone.isdigit():
            raise ClinicError('Telefone deve conter apenas números')
        
        return telefone
    
    @staticmethod
    def validarNumero(numero):
        if not numero.isdigit():
            raise ClinicError('O número da casa é inválido')
            
        return int(numero)
    
    @staticmethod
    def validarPessoa(pessoa):
        Validacao.validarNome(pessoa.nome, 'nome')
        Validacao.validarRg(pessoa.rg)
        Validacao.validarTelefone(pessoa.telefone)
    
    @staticmethod
    def validarEndereco(endereco):
        Validacao.validarRua(endereco.rua) #rua
        Validacao.validarNome(endereco.cidade, 'cidade') #cidade
        Validacao.validarEstado(endereco.estado)
        Validacao.validarNumero(endereco.numero)

