import ollama

from config import NOME_MODELO


def enviar_mensagem(mensagens):
    """
    Envia uma lista de mensagens para o modelo Ollama
    e retorna apenas o texto da resposta.
    """

    resposta = ollama.chat(
        model=NOME_MODELO,
        messages=mensagens
    )

    return resposta["message"]["content"]