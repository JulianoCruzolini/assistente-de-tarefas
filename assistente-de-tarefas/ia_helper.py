# ia_helper.py (novo arquivo)
import arquivo
import ollama
import ia_config
import utils

def sugerir_proxima_acao():
    lista_tarefas = arquivo.ler_arquivo()
    """IA sugere o que fazer com a tarefa"""
    SYSTEM_PROMPT = ia_config.SYSTEM_PROMPT
    prompt = f"""
    Quantidade total de tarfas: {len(lista_tarefas)}
    Todas as tarefas: {[tarefa["titulo"] for tarefa in lista_tarefas]}
    Pendente: {[tarefa for tarefa in lista_tarefas if tarefa["situacao"] == 'pendente']}
    Em Progresso: {[tarefa for tarefa in lista_tarefas if tarefa["situacao"] == 'em progresso']}
    Concluído: {[tarefa for tarefa in lista_tarefas if tarefa["situacao"] == 'concluído']}
    Altas: {[tarefa for tarefa in lista_tarefas if tarefa["prioridade"] == 'alta']}
    Media: {[tarefa for tarefa in lista_tarefas if tarefa["prioridade"] == 'media']}
    Baixa: {[tarefa for tarefa in lista_tarefas if tarefa["prioridade"] == 'baixa']}

    """
    mensagem_usuario = input('O que você quer falar para a IA?: ')
    
    resposta = ollama.chat(
        model='llama3.2',
        messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt + "\n" + mensagem_usuario}
            ]
    )
    
    return resposta['message']['content']

# Uso no menu:
def modo_ia():
    lista_tarefas = arquivo.ler_arquivo()
    
    # Pega primeira pendente
    pendente = next((t for t in lista_tarefas if t["situacao"] == "pendente"), None)
    em_progresso = next((t for t in lista_tarefas if t["situacao"] == "em progresso"), None)
    concluido = next((t for t in lista_tarefas if t["situacao"] == "concluído"), None)
    
    if not pendente and not em_progresso and not concluido:
        print("✅ Tudo concluído!")
        return
    
    print("🤖 Analisando tarefa...")
    sugestao = sugerir_proxima_acao()
    
    print("\n💡 Sugestão da IA:")
    print(f"   {sugestao}\n")