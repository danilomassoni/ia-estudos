import json

from ai.ollama_client import enviar_mensagem


def montar_contexto_estudos(estudos, topicos):
    """
    Monta o contexto dos estudos que será enviado à IA.

    Somente os tópicos selecionados pelo usuário
    são incluídos.
    """

    estudos_filtrados = [
        estudo
        for estudo in estudos
        if estudo.get("topico") in topicos
    ]

    contexto = []

    for estudo in estudos_filtrados:

        contexto.append({
            "data": estudo.get("data"),
            "assunto": estudo.get("assunto"),
            "topico": estudo.get("topico"),
            "conteudo": estudo.get("conteudo"),
            "dificuldades": estudo.get(
                "dificuldades",
                []
            ),
            "aprendizados": estudo.get(
                "aprendizados",
                []
            ),
            "compreensao": estudo.get(
                "compreensao"
            )
        })

    return contexto


def montar_prompt_perguntas(
    estudos,
    topicos,
    quantidade_perguntas,
    dificuldade
):
    """
    Monta o prompt responsável pela geração
    das perguntas da revisão.
    """

    contexto = montar_contexto_estudos(
        estudos,
        topicos
    )

    contexto_json = json.dumps(
        contexto,
        ensure_ascii=False,
        indent=4
    )

    prompt = f"""
Você é um professor responsável por criar
uma revisão personalizada de aprendizagem.

O estudante realizou estudos anteriormente.

Sua tarefa é criar perguntas para verificar
se o estudante realmente compreendeu os
conteúdos estudados.

IMPORTANTE:

As perguntas devem ser baseadas EXCLUSIVAMENTE
nos estudos fornecidos abaixo.

Não introduza assuntos que não estejam presentes
nos estudos.

Não utilize conhecimentos externos para cobrar
conteúdos que o estudante não estudou.

CONTEXTO DOS ESTUDOS:

{contexto_json}


TÓPICOS SELECIONADOS:

{json.dumps(
    topicos,
    ensure_ascii=False
)}


QUANTIDADE DE PERGUNTAS:

{quantidade_perguntas}


NÍVEL DE DIFICULDADE:

{dificuldade}


REGRAS:

1. Gere exatamente a quantidade de perguntas solicitada.

2. Todas as perguntas devem ser baseadas exclusivamente
   nos conteúdos fornecidos.

3. Não introduza conceitos que não estejam presentes
   nos estudos.

4. Cada pergunta deve testar um conhecimento diferente
   sempre que houver conteúdo suficiente para isso.

5. Evite perguntas redundantes.

6. Não crie várias perguntas que apenas reformulem
   a mesma questão.

7. Dê maior atenção aos conteúdos registrados como
   dificuldades, mas sem repetir excessivamente
   o mesmo conceito.

8. Utilize diferentes tipos de pergunta quando houver
   conteúdo suficiente:
   - conceitual
   - aplicação
   - análise
   - código
   - explicação

9. Perguntas de explicação devem pedir ao estudante
   que explique um conceito com suas próprias palavras.

10. Perguntas de aplicação devem apresentar uma situação
    relacionada ao conteúdo estudado.

11. Perguntas de análise podem apresentar código ou
    situações práticas quando isso estiver presente
    no conteúdo estudado.

12. O campo "enunciado" deve conter uma pergunta completa.

13. Nunca coloque uma instrução como enunciado.

    INCORRETO:
    "Explicar o conceito de reduce."

    CORRETO:
    "Como você explicaria o conceito de reduce()?"
    Sempre que possível, termine o enunciado com "?".

14. Evite perguntas que possam ser respondidas apenas
    com "sim" ou "não", salvo quando esse formato for
    realmente apropriado.

15. Não revele a resposta correta.

16. A dificuldade deve ser coerente com o conteúdo
    realmente estudado.

17. Se um conceito aparece como dificuldade do estudante,
    pelo menos uma pergunta deve avaliar esse conceito.

18. Não faça uma pergunta sobre algo que não possa ser
    respondido utilizando as informações dos estudos.

19. Não invente exemplos que dependam de conceitos
    externos aos estudos.

20. O objetivo é avaliar compreensão, não simplesmente
    memorização.

Retorne SOMENTE JSON válido.

Utilize exatamente esta estrutura:

Retorne SOMENTE JSON válido.

Utilize exatamente esta estrutura:

{{
    "perguntas": [
        {{
            "id": 1,
            "estudo_origem": "ID_DO_ESTUDO",
            "topico": "Streams",
            "tipo": "conceitual",
            "enunciado": "Qual é a diferença entre map() e filter() em Java Streams?",
            "dificuldade": "media"
        }}
    ]
}}

O campo "estudo_origem" deve conter EXATAMENTE
o valor do campo "id" de um dos estudos fornecidos
no contexto.

O nome do campo deve ser escrito EXATAMENTE assim:

"estudo_origem"

Não utilize variações como:

"estudo_origen"
"estudo_origem_id"
"origem_estudo"
"estudo"

Não invente IDs.

O campo "enunciado" deve sempre ser uma pergunta
completa e natural.

Não inclua respostas, explicações ou gabaritos.

TODOS os objetos dentro de "perguntas" devem obrigatoriamente
possuir TODOS os seguintes campos:

- id
- estudo_origem
- topico
- tipo
- enunciado
- dificuldade

Nunca omita nenhum desses campos.

O campo "dificuldade" deve obrigatoriamente possuir
um destes valores:

- "facil"
- "media"
- "alta"

Antes de gerar cada pergunta, verifique mentalmente:

1. Qual conhecimento do estudo esta pergunta avalia?
2. O estudante precisa utilizar esse conhecimento para respondê-la?
3. Existe outra pergunta que avalia praticamente o mesmo conhecimento?

Se a resposta para 2 for "não", reformule a pergunta.

Se a resposta para 3 for "sim", crie uma pergunta diferente.
"""

    return prompt


def extrair_json(resposta):
    """
    Extrai JSON da resposta da IA.
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


def validar_perguntas(dados):
    if not isinstance(dados, dict):
        raise ValueError("A resposta da IA não é um objeto JSON.")

    if "perguntas" not in dados:
        raise ValueError("Campo 'perguntas' não encontrado.")

    perguntas = dados["perguntas"]

    if not isinstance(perguntas, list):
        raise ValueError("O campo 'perguntas' deve ser uma lista.")

    if not perguntas:
        raise ValueError("A IA não gerou nenhuma pergunta.")

    for pergunta in perguntas:

        if "estudo_origen" in pergunta and "estudo_origem" not in pergunta:
            pergunta["estudo_origem"] = pergunta.pop("estudo_origen")

        campos = [
            "id",
            "estudo_origem",
            "topico",
            "tipo",
            "enunciado",
            "dificuldade"
        ]

        for campo in campos:
            if campo not in pergunta:
                raise ValueError(
                    f"Campo obrigatório ausente: {campo}. "
                    f"Pergunta recebida: {pergunta}"
                )

        if not isinstance(pergunta["enunciado"], str):
            raise ValueError(
                "O enunciado da pergunta deve ser texto."
            )

        if not pergunta["enunciado"].strip():
            raise ValueError(
                "Uma pergunta possui enunciado vazio."
            )

        enunciado = pergunta["enunciado"].strip()

        if not enunciado:
            raise ValueError(
                "Uma pergunta possui enunciado vazio."
            )

        pergunta["enunciado"] = enunciado

        dificuldades_validas = [
            "facil",
            "media",
            "alta"
        ]

        if pergunta["dificuldade"].lower() not in dificuldades_validas:
            raise ValueError(
                f"Dificuldade inválida: "
                f"{pergunta['dificuldade']}"
            )

    return True


def gerar_perguntas(
    estudos,
    topicos,
    quantidade_perguntas,
    dificuldade="adaptativa"
):
    """
    Gera perguntas utilizando a IA com base
    nos estudos selecionados.
    """

    if not estudos:

        raise ValueError(
            "Não existem estudos para gerar a revisão."
        )

    prompt = montar_prompt_perguntas(
        estudos=estudos,
        topicos=topicos,
        quantidade_perguntas=quantidade_perguntas,
        dificuldade=dificuldade
    )

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um sistema de avaliação "
                "educacional. "
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

    dados = extrair_json(
        resposta
    )

    validar_perguntas(
        dados
    )

    return dados["perguntas"]

def montar_prompt_avaliacao(
    pergunta,
    resposta_aluno,
    estudos
):
    contexto = montar_contexto_estudos(
        estudos,
        [pergunta["topico"]]
    )

    contexto_json = json.dumps(
        contexto,
        ensure_ascii=False,
        indent=4
    )

    pergunta_json = json.dumps(
        pergunta,
        ensure_ascii=False,
        indent=4
    )

    prompt = f"""
Você é um professor responsável por avaliar
a resposta de um estudante.

Sua avaliação deve ser baseada exclusivamente
no conteúdo estudado fornecido abaixo.

CONTEXTO DO ESTUDO:

{contexto_json}

PERGUNTA:

{pergunta_json}

RESPOSTA DO ESTUDANTE:

{resposta_aluno}

Avalie se a resposta demonstra compreensão
do conteúdo estudado.

IMPORTANTE:

1. Não exija palavras exatamente iguais às do estudo.

2. Considere respostas corretas mesmo quando
   o estudante utilizar palavras diferentes,
   desde que demonstre o conhecimento esperado.

3. Não considere uma resposta correta apenas
   porque contém palavras-chave.

4. Se a resposta estiver parcialmente correta,
   identifique o que está correto e o que está faltando.

5. Não utilize conhecimentos externos para exigir
   informações que não estejam presentes no estudo.

6. Seja objetivo.

7. Explique brevemente o motivo da avaliação.

8. Dê uma pontuação de 0 a 10.

Classifique a resposta como:

- "correta"
- "parcial"
- "incorreta"

RETORNE SOMENTE JSON VÁLIDO.

Utilize exatamente esta estrutura:

{{
    "avaliacao": {{
        "classificacao": "correta",
        "pontuacao": 10,
        "feedback": "A resposta demonstra compreensão do conceito.",
        "pontos_corretos": [
            "..."
        ],
        "pontos_faltantes": [
            "..."
        ]
    }}
}}
"""

    return prompt


def validar_avaliacao(dados):
    if not isinstance(dados, dict):
        raise ValueError(
            "A resposta da IA não é um objeto JSON."
        )

    if "avaliacao" not in dados:
        raise ValueError(
            "Campo 'avaliacao' não encontrado."
        )

    avaliacao = dados["avaliacao"]

    campos = [
        "classificacao",
        "pontuacao",
        "feedback",
        "pontos_corretos",
        "pontos_faltantes"
    ]

    for campo in campos:
        if campo not in avaliacao:
            raise ValueError(
                f"Campo obrigatório ausente: {campo}"
            )

    classificacoes_validas = [
        "correta",
        "parcial",
        "incorreta"
    ]

    if avaliacao["classificacao"] not in classificacoes_validas:
        raise ValueError(
            f"Classificação inválida: "
            f"{avaliacao['classificacao']}"
        )

    pontuacao = avaliacao["pontuacao"]

    if not isinstance(pontuacao, (int, float)):
        raise ValueError(
            "A pontuação deve ser numérica."
        )

    if not 0 <= pontuacao <= 10:
        raise ValueError(
            "A pontuação deve estar entre 0 e 10."
        )

    if not isinstance(
        avaliacao["pontos_corretos"],
        list
    ):
        raise ValueError(
            "pontos_corretos deve ser uma lista."
        )

    if not isinstance(
        avaliacao["pontos_faltantes"],
        list
    ):
        raise ValueError(
            "pontos_faltantes deve ser uma lista."
        )

    return True


def avaliar_resposta(
    pergunta,
    resposta_aluno,
    estudos
):

    if not resposta_aluno or not resposta_aluno.strip():

        raise ValueError(
            "A resposta do estudante não pode estar vazia."
        )

    prompt = montar_prompt_avaliacao(
        pergunta=pergunta,
        resposta_aluno=resposta_aluno,
        estudos=estudos
    )

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um avaliador educacional. "
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

    dados = extrair_json(
        resposta
    )

    validar_avaliacao(
        dados
    )

    avaliacao = dados["avaliacao"]

    return avaliacao