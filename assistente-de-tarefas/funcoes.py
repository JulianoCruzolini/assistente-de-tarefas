import os
import json
from enum import Enum


class Prioridade(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


lista_situacoes = ["pendente", "em progresso", "concluído"]


def inserir(tarefa_titulo):

    prioridade = perguntar_prioridade()
    if prioridade is None:
        return

    nova_tarefa = {
        "titulo": tarefa_titulo,
        "prioridade": prioridade.value,
        "situacao": lista_situacoes[0],
    }

    escrever_arquivo(nova_tarefa)
    print2n(
        f'A tarefa "{nova_tarefa["titulo"]}" com a prioridade "{nova_tarefa["prioridade"]}" foi adicionada!'
    )


def apagar():
    apagar_tarefa()


def checar_sair(input):
    if input.lower().find("sair") == 0:
        limpar_tela()
        print("Até mais!")
        return True
    return False


def checar_numero_positivo(numero):
    limpar_tela()
    if numero > 0:
        return True
    else:
        print2n("Insira um número positivo")
        return False


def editar(): ...


def avancar():
    avancar_situacao_tarefa()


def exibir():
    lista_terefas = ler_arquivo()
    exibir_tarefas(lista_terefas)


def avancar_situacao_tarefa():
    while True:
        lista_tarefas = ler_arquivo()
        lista_tarefas_a_concluir = [t for t in lista_tarefas if t["situacao"] != "concluído"]
        lista_tarefas_concluida = [t for t in lista_tarefas if t["situacao"] == "concluído"]
        if len(lista_tarefas_a_concluir) == 0:
            print("Não tem tarefa para avançar!")
            break

        exibir_tarefas(lista_tarefas_a_concluir)
        indice_tarefa = input("\nDigite o índice da tarefa que será avançada: ")
        limpar_tela()
        if checar_sair(indice_tarefa):
            break
        try:
            indice_tarefa = int(indice_tarefa)
        except ValueError:
            print2n("Insira um número")
            continue

        if not checar_numero_positivo(indice_tarefa):
            continue
        indice_tarefa-=1
        try:
            for indice, situacao in enumerate(lista_situacoes):
                if situacao == lista_tarefas_a_concluir[indice_tarefa]["situacao"]:
                    if situacao != lista_situacoes[-1]:
                        lista_tarefas_a_concluir[indice_tarefa]["situacao"] = lista_situacoes[indice+1]
                        escrever_arquivo(lista_tarefas_a_concluir + lista_tarefas_concluida)
                        print2n(
                            f'A tarefa "{lista_tarefas_a_concluir[indice_tarefa]["titulo"]}" foi avançada!'
                        )
                        return
                    else:
                        print2n(
                            f'A tarefa "{lista_tarefas_a_concluir[indice_tarefa]["titulo"]}" já está concluída!'
                        )

        except IndexError:
            print2n('Você digitou um número, mas não o certo. ¬_¬"')
            continue


def perguntar_opcoes_e_retornar_opcao(lista_opcoes):
    while True:
        print("-Opções disponíveis-")
        for opcao in lista_opcoes:
            print(f"{opcao['id']}. {opcao['nome']}")
        try:
            opcao_desejada = input("Opção: ")
            opcao_desejada = int(opcao_desejada)
            if not checar_numero_positivo(opcao_desejada):
                continue
            return str(lista_opcoes[opcao_desejada - 1]["id"])
        except IndexError:
            limpar_tela()
            print("Opção digitada inválida, tente novamente. :)")
        except ValueError:
            return opcao_desejada


def limpar_tela():
    os.system("cls")


def ler_arquivo() -> list:
    try:
        with open("tarefas.json", "r", encoding="utf-8") as arquivo_tarefas_json:
            return json.load(arquivo_tarefas_json)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def exibir_tarefas(lista_tarefas):

    indice_maior_tamanho = len(str(len(lista_tarefas)))
    titulo_maior_tamanho = max(len(t["titulo"]) for t in lista_tarefas)
    # prioridade_maior_tamanho = max(len(t["prioridade"]) for t in lista_tarefas)
    situacao_maior_tamanho = max(len(t["situacao"]) for t in lista_tarefas)
    print(
        f"{'Indice':<{indice_maior_tamanho + 1}}  {'Situacao':<{situacao_maior_tamanho + 1}}  {'Título':<{titulo_maior_tamanho + 1}}  Prioridade"
    )
    for indice, tarefa in enumerate(lista_tarefas):
        print(
            f"{indice + 1:<{indice_maior_tamanho + 6}} {tarefa['situacao']:<{situacao_maior_tamanho + 2}} {tarefa['titulo']:<{titulo_maior_tamanho + 2}} {tarefa['prioridade'].upper()}"
        )


def exibir_tarefas_a_concluir():
    lista_tarefas = ler_arquivo()
    lista_tarefas_a_concluir = [
        t for t in lista_tarefas if t["situacao"] != "concluído"
    ]
    print("print a concluir", lista_tarefas_a_concluir)

    indice_maior_tamanho = len(str(len(lista_tarefas)))
    titulo_maior_tamanho = max(len(t["titulo"]) for t in lista_tarefas)
    # prioridade_maior_tamanho = max(len(t["prioridade"]) for t in lista_tarefas)
    situacao_maior_tamanho = max(len(t["situacao"]) for t in lista_tarefas)
    print(
        f"{'Indice':<{indice_maior_tamanho + 1}}  {'Situacao':<{situacao_maior_tamanho + 1}}  {'Título':<{titulo_maior_tamanho + 1}}  Prioridade"
    )
    for indice, tarefa in enumerate(lista_tarefas):
        print(
            f"{indice + 1:<{indice_maior_tamanho + 6}} {tarefa['situacao']:<{situacao_maior_tamanho + 2}} {tarefa['titulo']:<{titulo_maior_tamanho + 2}} {tarefa['prioridade'].upper()}"
        )
    print()

def print2n(texto):
    print(texto, end='\n\n')


def apagar_tarefa():
    while True:
        lista_tarefas = ler_arquivo()
        exibir_tarefas(lista_tarefas)
        indice_tarefa = input("\nDigite o índice da tarefa que será apagada: ")
        limpar_tela()
        if checar_sair(indice_tarefa):
            break
        try:
            indice_tarefa = int(indice_tarefa)
            if not checar_numero_positivo(indice_tarefa):
                continue
            indice_tarefa-=1
        except ValueError:
            print2n("Digita um número ai, carai")
            continue
        try:
            tarefa_removida = lista_tarefas.pop(indice_tarefa)
        except IndexError:
            print('Você digitou um número, mas não o certo. ¬_¬"')
            continue
        escrever_arquivo(lista_tarefas)
        print((f'A tarefa "{tarefa_removida["titulo"]}" foi removida!'))
        return


def perguntar_prioridade():
    while True:
        resposta = input("Prioridade [a]lta, [m]édia, [b]aixa: ").lower()
        limpar_tela()
        if checar_sair(resposta):
            break
        if resposta in ["a", "alta"]:
            return Prioridade.ALTA
        elif resposta in ["m", "media", "média"]:
            return Prioridade.MEDIA
        elif resposta in ["b", "baixa"]:
            return Prioridade.BAIXA
        print("Opção inválida!")


def escrever_arquivo(tarefa_ou_lista):
    lista_tarefas_arquivo = ler_arquivo()
    if isinstance(tarefa_ou_lista, dict):
        lista_tarefas_arquivo.append(tarefa_ou_lista)
    else:
        lista_tarefas_arquivo = tarefa_ou_lista

    with open("tarefas.json", "w", encoding="utf-8") as arquivo_tarefas:
        json.dump(lista_tarefas_arquivo, arquivo_tarefas, indent=4, ensure_ascii=False)
