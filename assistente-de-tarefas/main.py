import funcoes
funcoes.limpar_tela()

lista_opcoes = [
    {"id": 1, "nome": "apagar", "funcao": funcoes.apagar},
    {"id": 2, "nome": "editar", "funcao": funcoes.editar},
    {"id": 3, "nome": "exibir", "funcao": funcoes.exibir},
    {"id": 4, "nome": "avançar situação", "funcao": funcoes.avancar},
    {"id": 5, "nome": "buscar tarefas", "funcao": funcoes.buscar},
]
while True:
    opcao_desejada = funcoes.perguntar_opcoes_e_retornar_opcao(lista_opcoes)
    if funcoes.checar_sair(opcao_desejada):
        break

    funcoes.limpar_tela()
    if len(opcao_desejada) > 1:
        funcoes.inserir(opcao_desejada)
    elif len(funcoes.ler_arquivo()) == 0:
        funcoes.print2n("Lista vazia!")
        continue
    else:
        try:
            opcao_desejada = int(opcao_desejada) 
            for opcao in lista_opcoes:
                if opcao_desejada == opcao["id"]:
                    opcao["funcao"]()
                    break
        except ValueError:
            funcoes.print2n("Um caractere só é paia")
