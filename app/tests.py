horarios = []

for i in range(0, 24):
    horarios.append(i)

for h in horarios:
    print(str(h) + ':00')



opcoes = [int(opcao) for opcao in input('Digite algo').split(' ')]
print(opcoes)