import json
import os
import uuid
from datetime import datetime

from config import ARQUIVO_RELATORIOS, NOME_MODELO
from services.estudo_service import gerar_resumo_periodo
from ai.ollama_client import enviar_mensagem


def criar_estrutura_relatorio():
    """
    Cria a estrutura padrão de um relatório.
    """

    return {
        "fatos_observados": [],
        "interpretacoes": [],
        "recomendacoes": [],
        "prioridades": []
    }


def carregar_relatorios():
    """
    Carrega todos os relatórios armazenados.
    """

    if not os.path.exists(ARQUIVO_RELATORIOS):
        return []

    with open(
        ARQUIVO_RELATORIOS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    return dados.get("relatorios", [])


def salvar_relatorios(relatorios):
    """
    Salva todos os relatórios no arquivo JSON.
    """

    dados = {
        "versao": 1,
        "relatorios": relatorios
    }

    with open(
        ARQUIVO_RELATORIOS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def montar_prompt_relatorio(resumo):
    """
    Monta o prompt que será enviado para a IA
    para análise do período de estudos.
    """

    dados = json.dumps(
        resumo,
        ensure_ascii=False,
        indent=4
    )

    prompt = f"""
    Você é um mentor pessoal de estudos.

    Analise os dados de estudo abaixo.

    DADOS DOS ESTUDOS:

    {dados}


    IMPORTANTE:

    Você deve separar claramente aquilo que é um fato
    daquilo que é uma interpretação ou recomendação.

    Não invente informações.

    Não transforme uma hipótese em fato.

    Não afirme que o estudante superou uma dificuldade
    se isso não estiver explicitamente registrado.

    Não considere uma dificuldade recorrente sem evidências
    de repetição em diferentes estudos ou períodos.

    Se não houver dados suficientes para uma conclusão,
    não faça a afirmação.


    RETORNE SOMENTE UM JSON VÁLIDO.

    Utilize exatamente esta estrutura:

    {{
        "fatos_observados": [],
        "interpretacoes": [],
        "recomendacoes": [],
        "prioridades": []
    }}


    ### FATOS OBSERVADOS

    Inclua somente informações diretamente presentes
    nos dados fornecidos.

    Exemplos:

    - quantidade de sessões;
    - tempo total estudado;
    - assuntos estudados;
    - tópicos estudados;
    - nível médio de compreensão;
    - dificuldades explicitamente registradas;
    - aprendizados explicitamente registrados.


    ### INTERPRETAÇÕES

    Inclua somente interpretações diretamente sustentadas
    pelos dados observados.

    As interpretações devem responder perguntas como:

    - Quais tópicos parecem exigir mais atenção?
    - Existem sinais de dificuldade?
    - Existem sinais de evolução?
    - Existe algum padrão que aparece em mais de uma sessão?
    - Existem assuntos que precisam de continuidade?

    REGRAS IMPORTANTES:

    - Não transforme uma hipótese em fato.
    - Não invente sentimentos do estudante.
    - Não invente motivação.
    - Não invente esforço.
    - Não invente intenção.
    - Não invente objetivos.
    - Não afirme que o estudante está inseguro, desmotivado,
    confiante, cansado ou interessado se isso não estiver
    explicitamente registrado.
    - Não considere uma dificuldade recorrente quando ela
    apareceu apenas uma vez.
    - Para considerar algo recorrente, deve existir evidência
    em diferentes sessões ou períodos.
    - Não interprete palavras isoladas como "difícil",
    "confuso" ou "complicado" como evidência de um estado
    emocional ou psicológico.
    - Não atribua significado que não esteja presente nos dados.
    - Não diga que houve evolução se não houver comparação
    suficiente entre registros.
    - Se os dados forem insuficientes, diga que não há
    evidências suficientes para concluir.

    Exemplo:

    DADO:
    "dificuldades": ["reduce"]

    INTERPRETAÇÃO CORRETA:
    "A compreensão de reduce ainda merece atenção."

    INTERPRETAÇÃO INCORRETA:
    "O estudante possui dificuldade recorrente em reduce."

    A segunda afirmação somente seria válida caso reduce
    aparecesse como dificuldade em diferentes sessões.

    Outro exemplo:

    DADO:
    "dificuldades": ["difícil"]

    INTERPRETAÇÃO CORRETA:
    "A dificuldade foi registrada de forma genérica e não há
    informações suficientes para identificar qual conceito
    específico exige atenção."

    INTERPRETAÇÃO INCORRETA:
    "O estudante está inseguro em relação ao conteúdo."


    ### RECOMENDAÇÕES

    Sugira ações práticas para melhorar o aprendizado.

    As recomendações devem estar relacionadas aos
    dados observados.

    Não invente dificuldades que não aparecem nos dados.


    ### PRIORIDADES

    Liste somente assuntos ou tópicos que devem receber
    atenção na próxima semana.

    As prioridades NÃO devem conter ações.

    CORRETO:

    [
        "Java Streams - reduce",
        "Python para uso com IA"
    ]

    INCORRETO:

    [
        "Praticar reduce com exemplos reais",
        "Continuar aprimorando o projeto"
    ]

    As ações devem aparecer somente em RECOMENDAÇÕES.

    Priorize:

    1. tópicos com dificuldades registradas;
    2. tópicos com baixa compreensão;
    3. tópicos que precisam de continuidade;
    4. tópicos importantes que ainda estão em desenvolvimento.

    Não crie prioridades que não estejam relacionadas
    aos dados dos estudos.

    ### REGRA FUNDAMENTAL

    Nunca invente:

    - objetivos;
    - motivações;
    - sentimentos;
    - esforço;
    - evolução não registrada;
    - dificuldades não mencionadas;
    - superação de dificuldades;
    - padrões recorrentes sem evidências.

    Quando uma conclusão depender de informações que não estão
    nos dados, não faça a afirmação como fato.
    """

    return prompt


def extrair_json(resposta):
    """
    Converte a resposta da IA em JSON.

    Também remove blocos Markdown caso o modelo
    retorne ```json ... ```.
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


def normalizar_relatorio(dados):
    """
    Garante que todas as categorias esperadas
    existam na resposta da IA.
    """

    categorias = [
        "fatos_observados",
        "interpretacoes",
        "recomendacoes",
        "prioridades"
    ]

    for categoria in categorias:

        if categoria not in dados:

            dados[categoria] = []

        if not isinstance(
            dados[categoria],
            list
        ):

            dados[categoria] = []

    return dados


def validar_relatorio(dados):
    """
    Valida a estrutura do relatório retornado pela IA.
    """

    categorias = [
        "fatos_observados",
        "interpretacoes",
        "recomendacoes",
        "prioridades"
    ]

    for categoria in categorias:

        if categoria not in dados:

            raise ValueError(
                f"Campo obrigatório ausente: {categoria}"
            )

        if not isinstance(
            dados[categoria],
            list
        ):

            raise ValueError(
                f"O campo '{categoria}' deve ser uma lista."
            )

        for item in dados[categoria]:

            if not isinstance(
                item,
                str
            ):

                raise ValueError(
                    f"Os itens de '{categoria}' "
                    "devem ser textos."
                )

    return True


def gerar_relatorio(data_inicio, data_fim):
    """
    Gera um relatório de estudos utilizando a IA.
    """

    resumo = gerar_resumo_periodo(
        data_inicio,
        data_fim
    )

    prompt = montar_prompt_relatorio(
        resumo
    )

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um mentor pessoal de estudos. "
                "Analise somente as informações fornecidas. "
                "Separe fatos de interpretações e recomendações. "
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

    dados_ia = normalizar_relatorio(
        dados_ia
    )

    validar_relatorio(
        dados_ia
    )

    relatorios = carregar_relatorios()

    relatorio = {
        "id": str(uuid.uuid4()),

        "periodo": {
            "inicio": data_inicio,
            "fim": data_fim
        },

        "gerado_em": datetime.now().isoformat(),

        "modelo": NOME_MODELO,

        "estatisticas": resumo["estatisticas"],

        "analise": dados_ia
    }

    relatorios.append(
        relatorio
    )

    salvar_relatorios(
        relatorios
    )

    return relatorio