import funcoes
funcoes.limpar_tela()

lista_opcoes = [
    {"nome": "apagar", "funcao": funcoes.apagar},
    {"nome": "editar", "funcao": funcoes.editar},
    {"nome": "exibir", "funcao": funcoes.exibir},
    {"nome": "avançar situação", "funcao": funcoes.avancar},
    {"nome": "buscar tarefas", "funcao": funcoes.buscar}
]

while True:
    opcao_desejada = funcoes.perguntar_opcoes_e_retornar_opcao(lista_opcoes)
    if funcoes.checar_sair(opcao_desejada):
        break
    if len(opcao_desejada) > 1:
        funcoes.inserir(opcao_desejada)
        continue
    if len(funcoes.ler_arquivo()) == 0:
        funcoes.print2n("Lista vazia!")
        continue

    lista_opcoes[int(opcao_desejada)-1]["funcao"]()
