import json
import os
import uuid
from datetime import datetime

from config import ARQUIVO_CONVERSAS, NOME_MODELO
from ai.ollama_client import enviar_mensagem


def carregar_conversas():
    """
    Carrega todas as mensagens armazenadas.
    """

    if not os.path.exists(ARQUIVO_CONVERSAS):
        return []

    with open(
        ARQUIVO_CONVERSAS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    return dados.get("conversas", [])


def salvar_conversas(conversas):
    """
    Salva todas as mensagens no arquivo JSON.
    """

    dados = {
        "versao": 1,
        "conversas": conversas
    }

    with open(
        ARQUIVO_CONVERSAS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def criar_mensagem(sessao_id, role, content, modelo=None):
    """
    Cria uma nova mensagem padronizada.
    """

    return {
        "id": str(uuid.uuid4()),
        "sessao_id": sessao_id,
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content,
        "modelo": modelo
    }


def conversar(sessao_id, mensagem_usuario):
    """
    Registra a mensagem do usuário,
    envia o histórico para a IA,
    registra a resposta e retorna o texto.
    """

    conversas = carregar_conversas()

    mensagem_usuario_obj = criar_mensagem(
        sessao_id=sessao_id,
        role="user",
        content=mensagem_usuario
    )

    conversas.append(mensagem_usuario_obj)

    mensagens_para_ia = [
        {
            "role": conversa["role"],
            "content": conversa["content"]
        }
        for conversa in conversas
    ]

    resposta = enviar_mensagem(mensagens_para_ia)

    mensagem_assistente = criar_mensagem(
        sessao_id=sessao_id,
        role="assistant",
        content=resposta,
        modelo="llama3.2:latest"
    )

    conversas.append(mensagem_assistente)

    salvar_conversas(conversas)

    return resposta