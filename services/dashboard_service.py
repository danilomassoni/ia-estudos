from datetime import datetime, timedelta

from services.estudo_service import (
    buscar_estudos_por_periodo,
    calcular_estatisticas
)

from services.memoria_service import (
    carregar_memoria
)


def gerar_resumo_dashboard(dias=7):
    """
    Gera os dados necessários para a Dashboard.

    A Dashboard não utiliza IA diretamente.
    Os dados são calculados a partir dos estudos
    registrados e da memória consolidada.
    """

    # ==============================
    # PERÍODO
    # ==============================

    hoje = datetime.now().date()

    data_inicio = hoje - timedelta(
        days=dias - 1
    )

    estudos = buscar_estudos_por_periodo(
        data_inicio.strftime("%Y-%m-%d"),
        hoje.strftime("%Y-%m-%d")
    )

    # ==============================
    # ESTATÍSTICAS
    # ==============================

    estatisticas = calcular_estatisticas(
        estudos
    )

    # ==============================
    # ASSUNTOS MAIS ESTUDADOS
    # ==============================

    assuntos = {}

    for estudo in estudos:

        assunto = estudo["assunto"]

        assuntos[assunto] = (
            assuntos.get(assunto, 0) + 1
        )

    assuntos_ordenados = sorted(
        assuntos.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # ==============================
    # PONTOS DE ATENÇÃO
    # ==============================

    pontos_atencao = []

    for estudo in estudos:

        # Compreensão baixa
        if estudo["compreensao"] <= 2:

            pontos_atencao.append({
                "assunto": estudo["assunto"],
                "topico": estudo["topico"],
                "compreensao": estudo["compreensao"]
            })

        # Dificuldades registradas
        dificuldades = estudo.get(
            "dificuldades",
            []
        )

        for dificuldade in dificuldades:

            pontos_atencao.append({
                "assunto": estudo["assunto"],
                "topico": estudo["topico"],
                "dificuldade": dificuldade
            })

    # ==============================
    # MEMÓRIA / PRIORIDADES
    # ==============================

    prioridades = []

    memoria = carregar_memoria()

    memoria_dados = memoria.get(
        "memoria",
        {}
    )

    prioridades_memoria = memoria_dados.get(
        "assuntos_para_revisar",
        []
    )

    for prioridade in prioridades_memoria:

        if prioridade not in prioridades:

            prioridades.append(
                prioridade
            )

    # ==============================
    # FALLBACK
    # ==============================

    # Se ainda não houver prioridades
    # na memória, utiliza os próximos
    # passos registrados nos estudos.

    if not prioridades:

        for estudo in estudos:

            proximo_passo = estudo.get(
                "proximo_passo"
            )

            if (
                proximo_passo
                and proximo_passo not in prioridades
            ):

                prioridades.append(
                    proximo_passo
                )

    # ==============================
    # ESTUDOS RECENTES
    # ==============================

    estudos_recentes = sorted(
        estudos,
        key=lambda estudo: (
            estudo["data"],
            estudo["hora_inicio"]
        ),
        reverse=True
    )

    estudos_recentes = estudos_recentes[:5]

    # ==============================
    # RESULTADO
    # ==============================

    return {
        "periodo": {
            "inicio": data_inicio.strftime(
                "%Y-%m-%d"
            ),
            "fim": hoje.strftime(
                "%Y-%m-%d"
            )
        },

        "estatisticas": estatisticas,

        "assuntos_mais_estudados": (
            assuntos_ordenados[:5]
        ),

        "pontos_atencao": (
            pontos_atencao[:5]
        ),

        "prioridades": (
            prioridades[:5]
        ),

        "estudos_recentes": (
            estudos_recentes
        )
    }