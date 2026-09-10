import json
import os
import uuid
from datetime import datetime
from ai.revisao_ai import gerar_perguntas, avaliar_resposta


from config import ARQUIVO_REVISOES
from services.estudo_service import (
    buscar_estudos_por_periodo
)


def carregar_revisoes():
    """
    Carrega todas as revisões realizadas.
    """

    if not os.path.exists(ARQUIVO_REVISOES):
        return []

    with open(
        ARQUIVO_REVISOES,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    return dados.get(
        "revisoes",
        []
    )


def salvar_revisoes(revisoes):
    """
    Salva todas as revisões.
    """

    dados = {
        "versao": 1,
        "revisoes": revisoes
    }

    with open(
        ARQUIVO_REVISOES,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def buscar_conteudo_revisao(
    data_inicio,
    data_fim,
    assunto
):
    """
    Busca os estudos de determinado assunto
    dentro de um período.

    Retorna somente os estudos que podem
    servir como base para uma revisão.
    """

    estudos = buscar_estudos_por_periodo(
        data_inicio,
        data_fim
    )

    estudos_assunto = [
        estudo
        for estudo in estudos
        if estudo["assunto"].lower()
        == assunto.lower()
    ]

    return estudos_assunto


def listar_assuntos_disponiveis(
    data_inicio,
    data_fim
):
    """
    Retorna os assuntos que realmente foram
    estudados dentro do período informado.
    """

    estudos = buscar_estudos_por_periodo(
        data_inicio,
        data_fim
    )

    assuntos = sorted(
        set(
            estudo["assunto"]
            for estudo in estudos
        )
    )

    return assuntos


def listar_topicos_disponiveis(
    data_inicio,
    data_fim,
    assunto
):
    """
    Retorna os tópicos estudados para um
    determinado assunto dentro do período.
    """

    estudos = buscar_conteudo_revisao(
        data_inicio,
        data_fim,
        assunto
    )

    topicos = sorted(
        set(
            estudo["topico"]
            for estudo in estudos
            if estudo.get("topico")
        )
    )

    return topicos


def criar_revisao(
    data_inicio,
    data_fim,
    assunto,
    topicos,
    quantidade_perguntas,
    dificuldade="adaptativa"
):
    """
    Cria a estrutura inicial de uma revisão.

    A geração das perguntas será realizada
    posteriormente pela IA.
    """

    if not assunto:
        raise ValueError(
            "O assunto da revisão é obrigatório."
        )

    if not topicos:
        raise ValueError(
            "Selecione pelo menos um tópico."
        )

    if quantidade_perguntas <= 0:
        raise ValueError(
            "A quantidade de perguntas deve ser maior que zero."
        )

    estudos = buscar_conteudo_revisao(
        data_inicio,
        data_fim,
        assunto
    )

    if not estudos:
        raise ValueError(
            "Não existem estudos desse assunto no período informado."
        )

    topicos_disponiveis = {
        estudo["topico"]
        for estudo in estudos
    }

    for topico in topicos:

        if topico not in topicos_disponiveis:

            raise ValueError(
                f"O tópico '{topico}' não foi estudado no período informado."
            )

    revisao = {
        "id": str(uuid.uuid4()),

        "data_criacao": datetime.now().isoformat(),

        "periodo": {
            "inicio": data_inicio,
            "fim": data_fim
        },

        "assunto": assunto,

        "topicos": topicos,

        "quantidade_perguntas": quantidade_perguntas,

        "dificuldade": dificuldade,

        "perguntas": [],

        "respostas": [],

        "resultado": None,

        "status": "criada"
    }

    revisoes = carregar_revisoes()

    revisoes.append(
        revisao
    )

    salvar_revisoes(
        revisoes
    )

    return revisao

def gerar_revisao(
    data_inicio,
    data_fim,
    assunto,
    topicos,
    quantidade_perguntas,
    dificuldade="adaptativa"
):
    """
    Cria uma revisão e gera suas perguntas.
    """

    estudos = buscar_conteudo_revisao(
        data_inicio,
        data_fim,
        assunto
    )

    if not estudos:

        raise ValueError(
            "Não existem estudos para essa revisão."
        )

    perguntas = gerar_perguntas(
        estudos=estudos,
        topicos=topicos,
        quantidade_perguntas=quantidade_perguntas,
        dificuldade=dificuldade
    )

    revisao = criar_revisao(
        data_inicio=data_inicio,
        data_fim=data_fim,
        assunto=assunto,
        topicos=topicos,
        quantidade_perguntas=quantidade_perguntas,
        dificuldade=dificuldade
    )

    revisao["perguntas"] = perguntas
    revisao["status"] = "perguntas_geradas"

    revisoes = carregar_revisoes()

    for indice, item in enumerate(revisoes):

        if item["id"] == revisao["id"]:

            revisoes[indice] = revisao
            break

    salvar_revisoes(
        revisoes
    )

    return revisao

def obter_proxima_pergunta(revisao_id):
    revisao = buscar_revisao(revisao_id)

    perguntas = revisao.get("perguntas", [])
    respostas = revisao.get("respostas", [])

    perguntas_respondidas = {
        resposta["pergunta_id"]
        for resposta in respostas
    }

    for pergunta in perguntas:
        if pergunta["id"] not in perguntas_respondidas:
            return pergunta

    return None

def registrar_resposta(
    revisao_id,
    pergunta_id,
    resposta_aluno,
    avaliacao
):
    revisoes = carregar_revisoes()

    for revisao in revisoes:

        if revisao["id"] != revisao_id:
            continue

        pergunta_existe = any(
            pergunta["id"] == pergunta_id
            for pergunta in revisao.get("perguntas", [])
        )

        if not pergunta_existe:
            raise ValueError(
                f"A pergunta '{pergunta_id}' "
                f"não pertence a esta revisão."
            )

        pergunta_respondida = any(
            resposta["pergunta_id"] == pergunta_id
            for resposta in revisao.get("respostas", [])
        )

        if pergunta_respondida:
            raise ValueError(
                f"A pergunta '{pergunta_id}' "
                f"já foi respondida."
            )

        if not resposta_aluno or not resposta_aluno.strip():
            raise ValueError(
                "A resposta do estudante não pode estar vazia."
            )

        resposta = {
            "pergunta_id": pergunta_id,
            "resposta": resposta_aluno.strip(),
            "avaliacao": avaliacao,
            "data_resposta": datetime.now().isoformat()
        }

        revisao["respostas"].append(resposta)

        quantidade_perguntas = len(
            revisao.get("perguntas", [])
        )

        quantidade_respostas = len(
            revisao.get("respostas", [])
        )

        if quantidade_respostas >= quantidade_perguntas:
            revisao["status"] = "pronta_para_finalizar"
        else:
            revisao["status"] = "em_andamento"

        salvar_revisoes(revisoes)

        return resposta

    raise ValueError(
        f"Revisão não encontrada: {revisao_id}"
    )

def buscar_revisao(revisao_id):
    revisoes = carregar_revisoes()

    for revisao in revisoes:
        if revisao["id"] == revisao_id:
            return revisao

    raise ValueError(
        f"Revisão não encontrada: {revisao_id}"
    )

def responder_pergunta(
    revisao_id,
    pergunta_id,
    resposta_aluno
):
    revisao = buscar_revisao(revisao_id)

    pergunta = None

    for item in revisao.get("perguntas", []):
        if item["id"] == pergunta_id:
            pergunta = item
            break

    if pergunta is None:
        raise ValueError(
            f"Pergunta não encontrada: {pergunta_id}"
        )

    perguntas_respondidas = {
        resposta["pergunta_id"]
        for resposta in revisao.get("respostas", [])
    }

    if pergunta_id in perguntas_respondidas:
        raise ValueError(
            f"A pergunta '{pergunta_id}' "
            f"já foi respondida."
        )

    estudos = buscar_conteudo_revisao(
        revisao["periodo"]["inicio"],
        revisao["periodo"]["fim"],
        revisao["assunto"]
    )

    avaliacao = avaliar_resposta(
        pergunta=pergunta,
        resposta_aluno=resposta_aluno,
        estudos=estudos
    )

    resposta = registrar_resposta(
        revisao_id=revisao_id,
        pergunta_id=pergunta_id,
        resposta_aluno=resposta_aluno,
        avaliacao=avaliacao
    )

    return resposta

def calcular_resultado_revisao(revisao_id):
    revisao = buscar_revisao(revisao_id)

    respostas = revisao.get("respostas", [])
    perguntas = revisao.get("perguntas", [])

    if not respostas:
        raise ValueError(
            "A revisão ainda não possui respostas."
        )

    pontuacoes = [
        resposta["avaliacao"]["pontuacao"]
        for resposta in respostas
    ]

    pontuacao_media = (
        sum(pontuacoes) / len(pontuacoes)
    )

    acertos = sum(
        1
        for resposta in respostas
        if resposta["avaliacao"]["classificacao"] == "correta"
    )

    parciais = sum(
        1
        for resposta in respostas
        if resposta["avaliacao"]["classificacao"] == "parcial"
    )

    erros = sum(
        1
        for resposta in respostas
        if resposta["avaliacao"]["classificacao"] == "incorreta"
    )

    por_topico = {}

    for pergunta in perguntas:
        topico = pergunta["topico"]

        if topico not in por_topico:
            por_topico[topico] = {
                "perguntas": 0,
                "respondidas": 0,
                "pontuacao_total": 0,
                "pontuacao_media": 0,
                "acertos": 0,
                "parciais": 0,
                "erros": 0
            }

        por_topico[topico]["perguntas"] += 1

    for resposta in respostas:
        pergunta_id = resposta["pergunta_id"]

        pergunta = next(
            (
                pergunta
                for pergunta in perguntas
                if pergunta["id"] == pergunta_id
            ),
            None
        )

        if pergunta is None:
            continue

        topico = pergunta["topico"]
        avaliacao = resposta["avaliacao"]

        por_topico[topico]["respondidas"] += 1
        por_topico[topico]["pontuacao_total"] += (
            avaliacao["pontuacao"]
        )

        classificacao = avaliacao["classificacao"]

        if classificacao == "correta":
            por_topico[topico]["acertos"] += 1

        elif classificacao == "parcial":
            por_topico[topico]["parciais"] += 1

        elif classificacao == "incorreta":
            por_topico[topico]["erros"] += 1

    for dados in por_topico.values():
        if dados["respondidas"] > 0:
            dados["pontuacao_media"] = round(
                dados["pontuacao_total"]
                / dados["respondidas"],
                2
            )

    pontos_fracos = []

    for topico, dados in por_topico.items():
        if dados["pontuacao_media"] < 7:
            pontos_fracos.append(topico)

    resultado = {
        "total_perguntas": len(perguntas),
        "total_respondidas": len(respostas),
        "acertos": acertos,
        "parciais": parciais,
        "erros": erros,
        "pontuacao_media": round(
            pontuacao_media,
            2
        ),
        "por_topico": por_topico,
        "pontos_fracos": pontos_fracos
    }

    return resultado

def finalizar_revisao(revisao_id):
    revisoes = carregar_revisoes()

    for revisao in revisoes:

        if revisao["id"] != revisao_id:
            continue

        quantidade_perguntas = len(
            revisao.get("perguntas", [])
        )

        quantidade_respostas = len(
            revisao.get("respostas", [])
        )

        if quantidade_respostas < quantidade_perguntas:
            raise ValueError(
                "A revisão ainda possui perguntas "
                "sem resposta."
            )

        resultado = calcular_resultado_revisao(
            revisao_id
        )

        revisao["resultado"] = resultado
        revisao["status"] = "concluida"

        salvar_revisoes(revisoes)

        return revisao

    raise ValueError(
        f"Revisão não encontrada: {revisao_id}"
    )

def obter_progresso_revisao(revisao_id):
    revisao = buscar_revisao(revisao_id)

    total = len(
        revisao.get("perguntas", [])
    )

    respondidas = len(
        revisao.get("respostas", [])
    )

    pendentes = total - respondidas

    if total > 0:
        percentual = round(
            (respondidas / total) * 100
        )
    else:
        percentual = 0

    return {
        "total": total,
        "respondidas": respondidas,
        "pendentes": pendentes,
        "percentual": percentual
    }

