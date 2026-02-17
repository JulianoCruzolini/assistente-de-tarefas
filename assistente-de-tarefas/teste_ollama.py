import ollama
import os

os.system('cls')
mensagem_humano = input('Mensagem para a IA: ')
resposta = ollama.chat(
    model='llama3.2',
    messages=[{
        'role': 'user',
        'content': mensagem_humano
    }]
)

print("IA:", resposta['message']['content'])