import utils
import ui
import arquivo

from enum import Enum


class Prioridade(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


RETENTATIVA = "Digite uma das opções abaixo."
LISTA_SITUACOES = ["pendente", "em progresso", "concluído"]


def contar_situacoes():
    lista_tarefas = arquivo.ler_arquivo()
    pendentes = len([t for t in lista_tarefas if t["situacao"] == "pendente"])
    em_progresso = len([t for t in lista_tarefas if t["situacao"] == "em progresso"])
    concluidas = len([t for t in lista_tarefas if t["situacao"] == "concluído"])
    print("Pendentes:", pendentes)
    print("Em progresso:", em_progresso)
    utils.print2n(f"Concluídas: {concluidas}")


def exibir():
    lista_tarefas = arquivo.ler_arquivo()
    ui.exibir_tarefas(lista_tarefas)


def editar():
    editar_tarefa()


def perguntar_opcoes_e_retornar_opcao(lista_opcoes):
    while True:
        print("--- Menu ---")
        ui.exibir_opcoes(lista_opcoes)

        entrada = input("\nOpção: ").strip()
        utils.limpar_tela()

        if not entrada:
            utils.print2n("❌ Digite algo!")
            continue

        if entrada.startswith("-"):
            utils.print2n("❌ Números negativos não são permitidos!")
            continue

        if entrada.isdigit():
            if utils.checar_indice(entrada, lista_opcoes):
                return entrada
            else:
                utils.print2n(f"❌ Opção {entrada} não existe!")
                continue

        if len(entrada) > 1:
            return entrada

        utils.print2n("Digite número do menu ou texto para tarefa!")


def perguntar_prioridade():
    while True:
        resposta = input("Prioridade - [a]lta, [m]édia, [b]aixa\nResposta: ").lower()
        if utils.checar_sair(resposta):
            return "sair"
        if resposta in ["a", "alta"]:
            return Prioridade.ALTA
        elif resposta in ["m", "media", "média"]:
            return Prioridade.MEDIA
        elif resposta in ["b", "baixa"]:
            return Prioridade.BAIXA
        elif len(resposta) == 0:
            return None
        utils.limpar_tela()
        utils.print2n(RETENTATIVA)


def avancar_situacao_tarefa():
    while True:
        lista_tarefas = arquivo.ler_arquivo()
        lista_tarefas_a_concluir = [tarefa for tarefa in lista_tarefas if tarefa["situacao"] != "concluído"]
        lista_tarefas_concluida = [tarefa for tarefa in lista_tarefas if tarefa["situacao"] == "concluído"]
        if utils.checar_lista_vazia(lista_tarefas_a_concluir):
            utils.limpar_tela()
            print("Não tem tarefa para avançar!")
            break
        ui.exibir_tarefas(lista_tarefas_a_concluir)
        indice_tarefa = input("Digite o índice da tarefa que será avançada: ")
        utils.limpar_tela()
        if utils.checar_sair(indice_tarefa):
            break
        if not utils.checar_indice(indice_tarefa, lista_tarefas_a_concluir):
            utils.print2n(RETENTATIVA)
            continue
        indice_tarefa = int(indice_tarefa) - 1
        tarefa_a_concluir = lista_tarefas_a_concluir[indice_tarefa]
        indice_atual = LISTA_SITUACOES.index(tarefa_a_concluir["situacao"])
        lista_tarefas_a_concluir[indice_tarefa]["situacao"] = LISTA_SITUACOES[indice_atual + 1]
        lista_completa = lista_tarefas_a_concluir + lista_tarefas_concluida
        arquivo.escrever_arquivo(lista_completa)
        utils.print2n(f'Tarefa "{tarefa_a_concluir["titulo"]}" avançada!')
        return


def avancar():
    avancar_situacao_tarefa()


def buscar():
    buscar_tarefa()


def apagar():
    apagar_tarefa()


def editar_tarefa():
    lista_tarefas = arquivo.ler_arquivo()
    if utils.checar_lista_vazia(lista_tarefas):
        return
    while True:
        ui.exibir_tarefas(lista_tarefas)
        indice_tarefa = input("Digite o índice da tarefa que será editada: ")
        utils.limpar_tela()
        if utils.checar_sair(indice_tarefa):
            return

        if not utils.checar_indice(indice_tarefa, lista_tarefas):
            utils.print2n(RETENTATIVA)
            continue

        tarefa = lista_tarefas[int(indice_tarefa) - 1]

        antigo_nome_tarefa = tarefa["titulo"]
        antiga_propriedade_tarefa = tarefa["prioridade"]

        print("Nome antigo:", antigo_nome_tarefa)
        utils.print2n(f"Prioridade antiga: {antiga_propriedade_tarefa}")

        novo_nome_tarefa = input("Digite o novo nome da tarefa: ")
        if utils.checar_sair(novo_nome_tarefa):
            return
        print("Digite a nova prioridade da tarefa")
        nova_prioridade_tarefa = perguntar_prioridade()

        novo_nome_tarefa = antigo_nome_tarefa if len(novo_nome_tarefa) == 0 else novo_nome_tarefa
        nova_prioridade_tarefa = antiga_propriedade_tarefa if nova_prioridade_tarefa is None else nova_prioridade_tarefa.value

        tarefa["titulo"] = novo_nome_tarefa
        tarefa["prioridade"] = nova_prioridade_tarefa

        arquivo.escrever_arquivo([tarefa])
        utils.limpar_tela()
        print(f'A tarefa "{antigo_nome_tarefa}" foi editada!')
        return


def inserir(tarefa_titulo):
    while True:
        prioridade = perguntar_prioridade()
        if prioridade is None:
            print(RETENTATIVA)
            continue
        if prioridade == "sair":
            return
        break

    nova_tarefa = {
        "titulo": tarefa_titulo,
        "prioridade": prioridade.value,
        "situacao": LISTA_SITUACOES[0],
    }

    arquivo.escrever_arquivo(nova_tarefa)
    utils.print2n(f'A tarefa "{nova_tarefa["titulo"]}" com a prioridade "{nova_tarefa["prioridade"]}" foi adicionada!')


def buscar_tarefa():
    lista_opcoes_busca = [
        {"nome": "Titulo", "funcao": utils.filtrar_tarefas_titulo},
        {"nome": "Prioridade", "funcao": utils.filtrar_tarefas_prioridade},
    ]
    lista_tarefas = arquivo.ler_arquivo()
    if utils.checar_lista_vazia(lista_tarefas):
        return
    while True:
        print("Buscar tarefa por:")
        ui.exibir_opcoes(lista_opcoes_busca)
        opcao_desejada = input("\nOpção: ")
        if utils.checar_sair(opcao_desejada):
            break
        if not utils.checar_indice(opcao_desejada, lista_opcoes_busca):
            utils.limpar_tela()
            utils.print2n(RETENTATIVA)
            continue
        lista_tarefas_filtradas = lista_opcoes_busca[int(opcao_desejada) - 1]["funcao"](lista_tarefas)
        if len(lista_tarefas_filtradas) > 0:
            ui.exibir_tarefas(lista_tarefas_filtradas)
        else:
            utils.print2n("Tarefas não encontradas!")


def apagar_tarefa():
    lista_tarefas = arquivo.ler_arquivo()
    if utils.checar_lista_vazia(lista_tarefas):
        return
    while True:
        ui.exibir_tarefas(lista_tarefas)
        indice_tarefa = input("Digite o índice da tarefa que será apagada: ")
        utils.limpar_tela()
        if utils.checar_sair(indice_tarefa):
            return
        if not utils.checar_indice(indice_tarefa, lista_tarefas):
            utils.print2n(RETENTATIVA)
            continue
        tarefa_removida = lista_tarefas.pop(int(indice_tarefa) - 1)
        arquivo.escrever_arquivo(lista_tarefas)
        print(f'A tarefa "{tarefa_removida["titulo"]}" foi removida!')
        return
