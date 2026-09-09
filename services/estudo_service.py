import json
import os
import uuid
from datetime import datetime

from config import ARQUIVO_ESTUDOS


def carregar_estudos():
    """
    Carrega todos os estudos armazenados.
    """

    if not os.path.exists(ARQUIVO_ESTUDOS):
        return []

    with open(
        ARQUIVO_ESTUDOS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    return dados.get("estudos", [])


def salvar_estudos(estudos):
    """
    Salva todos os estudos no arquivo JSON.
    """

    dados = {
        "versao": 1,
        "estudos": estudos
    }

    with open(
        ARQUIVO_ESTUDOS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def registrar_estudo(
    assunto,
    topico,
    conteudo,
    duracao_minutos,
    compreensao,
    dificuldades=None,
    aprendizados=None,
    proximo_passo=None,
    tags=None,
    status="concluido"
):
    """
    Registra uma nova sessão de estudo.
    """

    estudos = carregar_estudos()

    agora = datetime.now()

    estudo = {
        "id": str(uuid.uuid4()),
        "data": agora.strftime("%Y-%m-%d"),
        "hora_inicio": agora.strftime("%H:%M"),
        "duracao_minutos": duracao_minutos,

        "assunto": assunto,
        "topico": topico,

        "conteudo": conteudo,

        "compreensao": compreensao,

        "dificuldades": dificuldades or [],
        "aprendizados": aprendizados or [],

        "proximo_passo": proximo_passo,

        "tags": tags or [],

        "status": status
    }

    estudos.append(estudo)

    salvar_estudos(estudos)

    return estudo


def listar_estudos():
    """
    Retorna todos os estudos registrados.
    """

    return carregar_estudos()


def buscar_estudos_por_assunto(assunto):
    """
    Retorna estudos relacionados a um determinado assunto.
    """

    estudos = carregar_estudos()

    return [
        estudo
        for estudo in estudos
        if estudo["assunto"].lower() == assunto.lower()
    ]


def buscar_estudos_por_periodo(data_inicio, data_fim):
    """
    Retorna os estudos realizados entre duas datas.

    As datas devem estar no formato:
    YYYY-MM-DD
    """

    estudos = carregar_estudos()

    inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

    estudos_periodo = []

    for estudo in estudos:

        data_estudo = datetime.strptime(
            estudo["data"],
            "%Y-%m-%d"
        ).date()

        if inicio <= data_estudo <= fim:
            estudos_periodo.append(estudo)

    return estudos_periodo


def calcular_estatisticas(estudos):
    """
    Calcula estatísticas básicas de um conjunto de estudos.
    """

    if not estudos:
        return {
            "sessoes": 0,
            "tempo_total_minutos": 0,
            "tempo_total_horas": 0,
            "compreensao_media": 0,
            "assuntos_estudados": [],
            "topicos_estudados": []
        }

    tempo_total = sum(
        estudo["duracao_minutos"]
        for estudo in estudos
    )

    compreensao_media = sum(
        estudo["compreensao"]
        for estudo in estudos
    ) / len(estudos)

    assuntos = sorted(
        set(
            estudo["assunto"]
            for estudo in estudos
        )
    )

    topicos = sorted(
        set(
            estudo["topico"]
            for estudo in estudos
            if estudo["topico"]
        )
    )

    return {
        "sessoes": len(estudos),

        "tempo_total_minutos": tempo_total,

        "tempo_total_horas": round(
            tempo_total / 60,
            2
        ),

        "compreensao_media": round(
            compreensao_media,
            2
        ),

        "assuntos_estudados": assuntos,

        "topicos_estudados": topicos
    }


def gerar_resumo_periodo(data_inicio, data_fim):
    """
    Busca os estudos de um período e gera
    um resumo estruturado para análise.
    """

    estudos = buscar_estudos_por_periodo(
        data_inicio,
        data_fim
    )

    estatisticas = calcular_estatisticas(
        estudos
    )

    return {
        "periodo": {
            "inicio": data_inicio,
            "fim": data_fim
        },

        "estatisticas": estatisticas,

        "estudos": estudos
    }