import menu
import utils
utils.limpar_tela()

lista_opcoes = [
    {"nome": "apagar", "funcao": menu.apagar},
    {"nome": "editar", "funcao": menu.editar},
    {"nome": "exibir", "funcao": menu.exibir},
    {"nome": "avançar situação", "funcao": menu.avancar},
    {"nome": "contar situação das tarefas", "funcao": menu.contar_situacoes},
    {"nome": "buscar tarefas", "funcao": menu.buscar},
]

while True:
    opcao_desejada = menu.perguntar_opcoes_e_retornar_opcao(lista_opcoes)
    if utils.checar_sair(opcao_desejada):
        break
    if len(opcao_desejada) > 1:
        menu.inserir(opcao_desejada)
        continue
    lista_opcoes[int(opcao_desejada)-1]["funcao"]()
