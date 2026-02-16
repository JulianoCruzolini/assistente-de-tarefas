import os
import json
from enum import Enum


class Prioridade(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


lista_situacoes = ["pendente", "em progresso", "concluído"]


def inserir(tarefa_titulo):
    while True:
        prioridade = perguntar_prioridade()
        if prioridade is None:
            continue
        break

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
        return True
    return False


def checar_numero_positivo(numero):
    limpar_tela()
    if numero > 0:
        return True
    else:
        return False


def editar():
    editar_tarefa()


def avancar():
    avancar_situacao_tarefa()

def buscar():
    buscar_tarefa()

def filtrar_tarefas_titulo():
    lista_tarefas = ler_arquivo()
    palavra = input ('Digite uma palavra: ')
    limpar_tela()
    lista_tarefas_titulo = [tarefa for tarefa in lista_tarefas if palavra in tarefa["titulo"]]
    if len(lista_tarefas_titulo) > 0:
        exibir_tarefas(lista_tarefas_titulo)
    else:
        print2n('Não existem tarefas com essa palavra!')


def filtrar_tarefas_prioridade():
    lista_tarefas = ler_arquivo()
    prioridade = perguntar_prioridade()
    limpar_tela()
    lista_tarefas_prioridade = [tarefa for tarefa in lista_tarefas if tarefa["prioridade"] == prioridade.value]
    if len(lista_tarefas_prioridade) > 0:
        exibir_tarefas(lista_tarefas_prioridade)
    else:
        print2n('Não existem tarefas com essa prioridade!')


def buscar_tarefa():
    lista_opcoes_busca = [
        {"nome": "Titulo", "funcao": filtrar_tarefas_titulo},
        {"nome": "Prioridade", "funcao": filtrar_tarefas_prioridade}
    ]
    
    while True:
        print("Buscar tarefa por:")
        exibir_opcoes(lista_opcoes_busca)
        opcao_desejada = input('\nOpção: ')
        if checar_sair(opcao_desejada):
            break
        if not checar_indice(opcao_desejada, lista_opcoes_busca):
            limpar_tela()
            print2n('Escolha uma das opções abaixo ')
            continue
        lista_opcoes_busca[int(opcao_desejada)-1]["funcao"]()


def exibir():
    lista_tarefas = ler_arquivo()
    exibir_tarefas(lista_tarefas)

def checar_indice(indice, lista):
    return indice in list(map(str, range(1, len(lista)+1)))

def editar_tarefa():
    while True:
        lista_tarefas = ler_arquivo()
        exibir_tarefas(lista_tarefas)
        indice_tarefa = input("Digite o índice da tarefa que será editada: ")
        limpar_tela()
        if checar_sair(indice_tarefa):
            break

        if not checar_indice(indice_tarefa, lista_tarefas):
            print("Digite novamente")
            continue

        indice_tarefa = int(indice_tarefa)
        indice_tarefa-=1
        tarefa = lista_tarefas[indice_tarefa]

        print('Nome antigo:',tarefa["titulo"])
        print2n(f'Prioridade antiga: {tarefa["prioridade"]}')

        antigo_nome_tarefa = tarefa["titulo"]
        antiga_propriedade_tarefa = tarefa["prioridade"]

        novo_nome_tarefa = input('Digite o novo nome da tarefa: ')
        print("Digite a nova prioridade da tarefa")
        nova_prioridade_tarefa = perguntar_prioridade()

        novo_nome_tarefa = antigo_nome_tarefa if len(novo_nome_tarefa) == 0 else novo_nome_tarefa
        nova_prioridade_tarefa = antiga_propriedade_tarefa if nova_prioridade_tarefa is None else nova_prioridade_tarefa.value

        tarefa["titulo"] = novo_nome_tarefa
        tarefa["prioridade"] = nova_prioridade_tarefa

        escrever_arquivo([tarefa])
        limpar_tela()
        print((f'A tarefa "{antigo_nome_tarefa}" foi editada!'))
        return

def avancar_situacao_tarefa():
    while True:
        lista_tarefas = ler_arquivo()
        lista_tarefas_a_concluir = [tarefa for tarefa in lista_tarefas if tarefa["situacao"] != "concluído"]
        lista_tarefas_concluida = [tarefa for tarefa in lista_tarefas if tarefa["situacao"] == "concluído"]
        if len(lista_tarefas_a_concluir) == 0:
            print("Não tem tarefa para avançar!")
            break

        exibir_tarefas(lista_tarefas_a_concluir)
        indice_tarefa = input("Digite o índice da tarefa que será avançada: ")
        limpar_tela()
        if checar_sair(indice_tarefa):
            break
        if not checar_indice(indice_tarefa, lista_tarefas_a_concluir):
            continue
        indice_tarefa = int(indice_tarefa)
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

def exibir_opcoes(lista_opcoes):
    for indice, opcao in enumerate(lista_opcoes):
        print(f"{indice+1}. {opcao['nome']}")

def criar_opcao(nome, funcao):
    return {"nome": nome, "funcao": funcao}

def perguntar_opcoes_e_retornar_opcao(lista_opcoes):
    """
    Exibe menu e retorna opção escolhida.
    
    Returns:
        str: ID da opção OU texto para adicionar tarefa
    """
    
    while True:
        # Exibe menu
        print("--- Menu ---")
        exibir_opcoes(lista_opcoes)
       
        
        # Pede entrada
        entrada = input("\nOpção: ").strip()
        limpar_tela()
        
        # Valida vazio
        if not entrada:
            print2n("❌ Digite algo!")
            continue
        
        # Valida negativo
        if entrada.startswith('-'):
            print2n("❌ Números negativos não são permitidos!")
            continue
        
        # Se é número puro (digitos)
        if entrada.isdigit():
            if checar_indice(entrada, lista_opcoes):
                return entrada  # Opção válida
            else:
                print2n(f"❌ Opção {entrada} não existe!")
                continue
        
        # Se é texto
        if len(entrada) > 1:
            return entrada  # Adicionar tarefa
        
        # 1 letra inválida
        print2n("⚠️ Digite número do menu ou texto para tarefa!")

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
    print()


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
        indice_tarefa = input("Digite o índice da tarefa que será apagada: ")
        limpar_tela()
        if checar_sair(indice_tarefa):
            break
        if not checar_indice(indice_tarefa, lista_tarefas):
            continue
        indice_tarefa = int(indice_tarefa)
        indice_tarefa -= 1
        tarefa_removida = lista_tarefas.pop(indice_tarefa)
        escrever_arquivo(lista_tarefas)
        print((f'A tarefa "{tarefa_removida["titulo"]}" foi removida!'))
        return


def perguntar_prioridade():
    while True:
        resposta = input("Prioridade - [a]lta, [m]édia, [b]aixa\nResposta: ").lower()
        if checar_sair(resposta):
            break
        if resposta in ["a", "alta"]:
            return Prioridade.ALTA
        elif resposta in ["m", "media", "média"]:
            return Prioridade.MEDIA
        elif resposta in ["b", "baixa"]:
            return Prioridade.BAIXA
        elif len(resposta) == 0:
            return None
        print("Opção inválida!")


def escrever_arquivo(tarefa_ou_lista):
    lista_tarefas_arquivo = ler_arquivo()
    if isinstance(tarefa_ou_lista, dict):
        lista_tarefas_arquivo.append(tarefa_ou_lista)
    else:
        lista_tarefas_arquivo = tarefa_ou_lista

    with open("tarefas.json", "w", encoding="utf-8") as arquivo_tarefas:
        json.dump(lista_tarefas_arquivo, arquivo_tarefas, indent=4, ensure_ascii=False)
