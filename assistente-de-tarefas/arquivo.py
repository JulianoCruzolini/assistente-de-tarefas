import json


def escrever_arquivo(tarefa_ou_lista):
    lista_tarefas_arquivo = ler_arquivo()
    if isinstance(tarefa_ou_lista, dict):
        lista_tarefas_arquivo.append(tarefa_ou_lista)
    else:
        lista_tarefas_arquivo = tarefa_ou_lista

    with open("tarefas.json", "w", encoding="utf-8") as arquivo_tarefas:
        json.dump(lista_tarefas_arquivo, arquivo_tarefas, indent=4, ensure_ascii=False)


def ler_arquivo() -> list:
    try:
        with open("tarefas.json", "r", encoding="utf-8") as arquivo_tarefas_json:
            return json.load(arquivo_tarefas_json)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
