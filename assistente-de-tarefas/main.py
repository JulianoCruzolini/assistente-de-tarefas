import funcoes

lista_opcoes = [
    {"id": 1, "nome": "apagar", "funcao": funcoes.apagar},
    {"id": 2, "nome": "editar", "funcao": funcoes.editar},
    {"id": 3, "nome": "exibir", "funcao": funcoes.exibir},
    {"id": 4, "nome": "avançar situação", "funcao": funcoes.avancar},
]

while True:
    opcao_desejada = funcoes.perguntar_opcoes_e_retornar_opcao(lista_opcoes)
    if funcoes.checar_sair(opcao_desejada):
        break

    funcoes.limpar_tela()
    if len(opcao_desejada) > 1:
        funcoes.inserir(opcao_desejada)
    elif len(funcoes.ler_arquivo()) == 0:
        print("Lista vazia!")
        continue
    else:
        try:
            for opcao in lista_opcoes:
                if int(opcao_desejada) == opcao["id"]:
                    opcao["funcao"]()
                    break
        except ValueError:
            print("Um caractere só é paia")
