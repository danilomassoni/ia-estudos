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


def criar_mensagem(
    sessao_id,
    role,
    content,
    modelo=None
):
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


def buscar_mensagens_sessao(
    sessao_id
):
    """
    Retorna somente as mensagens
    pertencentes à sessão atual.
    """

    conversas = carregar_conversas()

    return [
        conversa
        for conversa in conversas
        if conversa.get("sessao_id")
        == sessao_id
    ]


def conversar(
    sessao_id,
    mensagem_usuario
):
    """
    Registra a mensagem do usuário,
    envia somente o histórico da sessão
    atual para a IA, registra a resposta
    e retorna o texto.
    """

    conversas = carregar_conversas()

    # ==============================
    # MENSAGEM DO USUÁRIO
    # ==============================

    mensagem_usuario_obj = criar_mensagem(
        sessao_id=sessao_id,
        role="user",
        content=mensagem_usuario
    )

    conversas.append(
        mensagem_usuario_obj
    )

    # ==============================
    # HISTÓRICO DA SESSÃO
    # ==============================

    mensagens_sessao = [
        conversa
        for conversa in conversas
        if conversa.get("sessao_id")
        == sessao_id
    ]

    # ==============================
    # PREPARAR CONTEXTO DA IA
    # ==============================

    mensagens_para_ia = [
        {
            "role": conversa["role"],
            "content": conversa["content"]
        }

        for conversa in mensagens_sessao
    ]

    # ==============================
    # ENVIAR PARA OLLAMA
    # ==============================

    resposta = enviar_mensagem(
        mensagens_para_ia
    )

    # ==============================
    # MENSAGEM DA IA
    # ==============================

    mensagem_assistente = criar_mensagem(
        sessao_id=sessao_id,
        role="assistant",
        content=resposta,
        modelo=NOME_MODELO
    )

    conversas.append(
        mensagem_assistente
    )

    # ==============================
    # SALVAR
    # ==============================

    salvar_conversas(
        conversas
    )

    return resposta