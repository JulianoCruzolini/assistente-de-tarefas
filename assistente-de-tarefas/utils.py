import os
import menu


def limpar_tela():
    os.system("cls")


def checar_indice(indice, lista):
    return indice in list(map(str, range(1, len(lista) + 1)))


def checar_sair(input):
    if input.lower().find("sair") == 0:
        limpar_tela()
        return True
    return False


def checar_lista_vazia(lista):
    if not lista:
        print("Lista vazia!")
        return True
    return False


def print2n(texto):
    print(texto, end="\n\n")


def filtrar_tarefas_titulo(lista_tarefas):
    palavra = input("Digite uma palavra: ")
    limpar_tela()
    return [tarefa for tarefa in lista_tarefas if palavra in tarefa["titulo"]]


def filtrar_tarefas_prioridade(lista_tarefas):
    prioridade = menu.perguntar_prioridade()
    limpar_tela()
    return [tarefa for tarefa in lista_tarefas if tarefa["prioridade"] == prioridade.value]
