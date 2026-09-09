import json
import os
from datetime import datetime

from config import ARQUIVO_MEMORIA
from ai.ollama_client import enviar_mensagem


def criar_estrutura_memoria():
    """
    Cria a estrutura padrão da memória.
    """

    return {
        "versao": 1,
        "memoria": {
            "pontos_fortes": [],
            "dificuldades_recorrentes": [],
            "lacunas_conhecimento": [],
            "padroes_aprendizagem": [],
            "preferencias_observadas": [],
            "assuntos_para_revisar": [],
            "evolucao_conhecimentos": [],
            "observacoes_importantes": []
        }
    }


def carregar_memoria():
    """
    Carrega a memória atual.
    """

    if not os.path.exists(ARQUIVO_MEMORIA):
        return criar_estrutura_memoria()

    with open(
        ARQUIVO_MEMORIA,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)


def salvar_memoria(memoria):
    """
    Salva a memória consolidada.
    """

    with open(
        ARQUIVO_MEMORIA,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            memoria,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def montar_prompt_memoria(memoria_atual, relatorio):
    """
    Solicita apenas novas observações para a memória.
    """

    memoria_json = json.dumps(
        memoria_atual["memoria"],
        ensure_ascii=False,
        indent=4
    )

    relatorio_json = json.dumps(
        relatorio,
        ensure_ascii=False,
        indent=4
    )

    prompt = f"""
Você é responsável por identificar novas informações
sobre o aprendizado de um estudante.

MEMÓRIA ATUAL:

{memoria_json}


NOVO RELATÓRIO:

{relatorio_json}


Sua tarefa NÃO é recriar toda a memória.

Identifique apenas informações novas ou atualizações
importantes que podem ser adicionadas à memória.

Não invente informações.

Uma dificuldade deve ser considerada recorrente apenas
quando existirem evidências suficientes de repetição.

Retorne SOMENTE JSON válido.

Utilize exatamente esta estrutura:

{{
    "novas_observacoes": {{
        "pontos_fortes": [],
        "dificuldades_recorrentes": [],
        "lacunas_conhecimento": [],
        "padroes_aprendizagem": [],
        "preferencias_observadas": [],
        "assuntos_para_revisar": [],
        "evolucao_conhecimentos": [],
        "observacoes_importantes": []
    }}
}}

Cada item deve ser um objeto JSON.

Se não houver novas informações em uma categoria,
retorne uma lista vazia.
"""

    return prompt


def extrair_json(resposta):
    """
    Converte a resposta da IA em JSON.
    """

    resposta = resposta.strip()

    if resposta.startswith("```json"):

        resposta = resposta.replace(
            "```json",
            "",
            1
        )

        resposta = resposta.rsplit(
            "```",
            1
        )[0]

    elif resposta.startswith("```"):

        resposta = resposta.replace(
            "```",
            "",
            1
        )

        resposta = resposta.rsplit(
            "```",
            1
        )[0]

    return json.loads(
        resposta.strip()
    )

def normalizar_novas_observacoes(dados):
    """
    Garante que todas as categorias esperadas
    existam na resposta da IA.
    """

    categorias = [
        "pontos_fortes",
        "dificuldades_recorrentes",
        "lacunas_conhecimento",
        "padroes_aprendizagem",
        "preferencias_observadas",
        "assuntos_para_revisar",
        "evolucao_conhecimentos",
        "observacoes_importantes"
    ]

    if "novas_observacoes" not in dados:

        dados["novas_observacoes"] = {}

    for categoria in categorias:

        if categoria not in dados["novas_observacoes"]:

            dados["novas_observacoes"][
                categoria
            ] = []

    return dados


def validar_novas_observacoes(dados):
    """
    Valida a estrutura retornada pela IA.
    """

    if not isinstance(dados, dict):
        raise ValueError(
            "A resposta da IA não é um objeto JSON."
        )

    if "novas_observacoes" not in dados:

        raise ValueError(
            "Campo 'novas_observacoes' não encontrado."
        )

    observacoes = dados["novas_observacoes"]

    if not isinstance(observacoes, dict):

        raise ValueError(
            "O campo 'novas_observacoes' deve ser um objeto."
        )

    campos_obrigatorios = [
        "pontos_fortes",
        "dificuldades_recorrentes",
        "lacunas_conhecimento",
        "padroes_aprendizagem",
        "preferencias_observadas",
        "assuntos_para_revisar",
        "evolucao_conhecimentos",
        "observacoes_importantes"
    ]

    for campo in campos_obrigatorios:

        if campo not in observacoes:

            raise ValueError(
                f"Campo obrigatório ausente: {campo}"
            )

        if not isinstance(
            observacoes[campo],
            list
        ):

            raise ValueError(
                f"O campo '{campo}' deve ser uma lista."
            )

    return True


def item_ja_existe(lista, novo_item):
    """
    Verifica se um item equivalente já existe na memória.
    """

    novo_item_json = json.dumps(
        novo_item,
        ensure_ascii=False,
        sort_keys=True
    )

    for item in lista:

        item_json = json.dumps(
            item,
            ensure_ascii=False,
            sort_keys=True
        )

        if item_json == novo_item_json:
            return True

    return False


def consolidar_memoria(memoria_atual, novas_observacoes):
    """
    Adiciona novas informações sem apagar a memória anterior.
    """

    memoria = memoria_atual["memoria"]

    for categoria, novos_itens in novas_observacoes.items():

        for novo_item in novos_itens:

            if not item_ja_existe(
                memoria[categoria],
                novo_item
            ):

                memoria[categoria].append(
                    novo_item
                )

    return memoria_atual


def atualizar_memoria(relatorio):
    """
    Analisa o relatório e consolida novas informações
    na memória existente.
    """

    dados_memoria = carregar_memoria()

    prompt = montar_prompt_memoria(
        dados_memoria,
        relatorio
    )

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um sistema de análise de aprendizagem. "
                "Responda exclusivamente com JSON válido."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    resposta = enviar_mensagem(
        mensagens
    )

    dados_ia = extrair_json(
        resposta
    )

    dados_ia = normalizar_novas_observacoes(
        dados_ia
    )

    validar_novas_observacoes(
        dados_ia
    )

    memoria_atualizada = consolidar_memoria(
        dados_memoria,
        dados_ia["novas_observacoes"]
    )

    salvar_memoria(
        memoria_atualizada
    )

    return memoria_atualizada