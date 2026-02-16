import utils
import arquivo


def exibir_tarefas_a_concluir():
    lista_tarefas = arquivo.ler_arquivo()
    lista_tarefas_a_concluir = [t for t in lista_tarefas if t["situacao"] != "concluído"]
    print("print a concluir", lista_tarefas_a_concluir)

    indice_maior_tamanho = len(str(len(lista_tarefas)))
    titulo_maior_tamanho = max(len(t["titulo"]) for t in lista_tarefas)
    # prioridade_maior_tamanho = max(len(t["prioridade"]) for t in lista_tarefas)
    situacao_maior_tamanho = max(len(t["situacao"]) for t in lista_tarefas)
    print(f"{'Indice':<{indice_maior_tamanho + 1}}  {'Situacao':<{situacao_maior_tamanho + 1}}  {'Título':<{titulo_maior_tamanho + 1}}  Prioridade")
    for indice, tarefa in enumerate(lista_tarefas):
        print(f"{indice + 1:<{indice_maior_tamanho + 6}} {tarefa['situacao']:<{situacao_maior_tamanho + 2}} {tarefa['titulo']:<{titulo_maior_tamanho + 2}} {tarefa['prioridade'].upper()}")
    print()


def exibir_tarefas(lista_tarefas):
    if utils.checar_lista_vazia(lista_tarefas):
        return
    indice_maior_tamanho = len(str(len(lista_tarefas)))
    titulo_maior_tamanho = max(len(t["titulo"]) for t in lista_tarefas)
    # prioridade_maior_tamanho = max(len(t["prioridade"]) for t in lista_tarefas)
    situacao_maior_tamanho = max(len(t["situacao"]) for t in lista_tarefas)
    print(f"{'Indice':<{indice_maior_tamanho + 1}}  {'Situacao':<{situacao_maior_tamanho + 1}}  {'Título':<{titulo_maior_tamanho + 1}}  Prioridade")
    for indice, tarefa in enumerate(lista_tarefas):
        print(f"{indice + 1:<{indice_maior_tamanho + 6}} {tarefa['situacao']:<{situacao_maior_tamanho + 2}} {tarefa['titulo']:<{titulo_maior_tamanho + 2}} {tarefa['prioridade'].upper()}")
    print()


def exibir_opcoes(lista_opcoes):
    for indice, opcao in enumerate(lista_opcoes):
        print(f"{indice + 1}. {opcao['nome']}")
