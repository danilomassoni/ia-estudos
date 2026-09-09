import uuid
from datetime import datetime, timedelta

from services.conversa_service import conversar

from services.estudo_service import (
    registrar_estudo
)

from services.relatorio_service import (
    gerar_relatorio
)

from services.memoria_service import (
    carregar_memoria,
    atualizar_memoria
)


def iniciar_sessao():
    """
    Cria um identificador único para a sessão atual.
    """

    return str(uuid.uuid4())


def mostrar_menu():
    """
    Mostra os comandos disponíveis.
    """

    print("""
===================================
         IA DE ESTUDOS
===================================

Comandos disponíveis:

/estudar   - Registrar um estudo
/relatorio - Gerar relatório semanal
/memoria   - Visualizar memória
/ajuda     - Mostrar comandos
/sair      - Encerrar programa

Você também pode conversar normalmente
com a IA.
""")


def registrar_estudo_manual():
    """
    Solicita os dados de estudo ao usuário
    e registra uma nova sessão.
    """

    print("\n===================================")
    print("      REGISTRAR ESTUDO")
    print("===================================\n")

    assunto = input("Assunto (Área geral estudada. Ex: Python, Java, Machine Learning): ")

    topico = input("Tópico (Conteúdo específico estudado. Ex.: Streams, POO, Pandas, Redes Neurais.) ")

    conteudo = input(
        "O que você estudou? (Resumo do que foi estudado. Ex.: Estudei map, filter e reduce.): "
    )

    while True:

        try:

            duracao_minutos = int(
                input(
                    "Duração em minutos: "
                )
            )

            break

        except ValueError:

            print(
                "Digite apenas um número."
            )

    while True:

        try:

            compreensao = int(
                input(
                    "Compreensão (1 a 5): "
                )
            )

            if 1 <= compreensao <= 5:
                break

            print(
                "Digite um número entre 1 e 5.(1 = não entendi | 3 = entendi parcialmente | 5 = consigo explicar)"
            )

        except ValueError:

            print(
                "Digite apenas um número."
            )

    dificuldades_texto = input(
        "Dificuldades (separe por vírgula)(Conceitos ou conteúdos que apresentaram dificuldade.): "
    )

    aprendizados_texto = input(
        "Aprendizados (separe por vírgula)(Conceitos ou conteúdos que foram compreendidos.): "
    )

    proximo_passo = input(
        "Próximo passo (O que deve ser feito posteriormente.(ex.: praticar reduce com exercícios)):"
    )

    dificuldades = [
        dificuldade.strip()
        for dificuldade in dificuldades_texto.split(",")
        if dificuldade.strip()
    ]

    aprendizados = [
        aprendizado.strip()
        for aprendizado in aprendizados_texto.split(",")
        if aprendizado.strip()
    ]

    estudo = registrar_estudo(
        assunto=assunto,
        topico=topico,
        conteudo=conteudo,
        duracao_minutos=duracao_minutos,
        compreensao=compreensao,
        dificuldades=dificuldades,
        aprendizados=aprendizados,
        proximo_passo=proximo_passo
    )

    print("\nEstudo registrado com sucesso!")

    print(
        f"\nAssunto: {estudo['assunto']}"
    )

    print(
        f"Tópico: {estudo['topico']}"
    )

    print(
        f"Duração: "
        f"{estudo['duracao_minutos']} minutos"
    )

def mostrar_relatorio(relatorio):
    """
    Exibe o relatório semanal de forma organizada.
    """

    analise = relatorio["analise"]

    print("\n===================================")
    print("          RELATÓRIO SEMANAL")
    print("===================================")

    print(
        f"\nPeríodo: "
        f"{relatorio['periodo']['inicio']} "
        f"até "
        f"{relatorio['periodo']['fim']}"
    )

    estatisticas = relatorio["estatisticas"]

    print("\n-----------------------------------")
    print("RESUMO DOS ESTUDOS")
    print("-----------------------------------")

    print(
        f"Sessões realizadas: "
        f"{estatisticas['sessoes']}"
    )

    print(
        f"Tempo total: "
        f"{estatisticas['tempo_total_horas']} horas"
    )

    print(
        f"Compreensão média: "
        f"{estatisticas['compreensao_media']}/5"
    )

    print(
        "\nAssuntos estudados:"
    )

    for assunto in estatisticas["assuntos_estudados"]:

        print(
            f"  • {assunto}"
        )

    print(
        "\nTópicos estudados:"
    )

    for topico in estatisticas["topicos_estudados"]:

        print(
            f"  • {topico}"
        )

    print("\n-----------------------------------")
    print("FATOS OBSERVADOS")
    print("-----------------------------------")

    if not analise["fatos_observados"]:

        print("Nenhum fato registrado.")

    else:

        for fato in analise["fatos_observados"]:

            print(
                f"  • {fato}"
            )

    print("\n-----------------------------------")
    print("INTERPRETAÇÕES")
    print("-----------------------------------")

    if not analise["interpretacoes"]:

        print("Nenhuma interpretação disponível.")

    else:

        for interpretacao in analise["interpretacoes"]:

            print(
                f"  • {interpretacao}"
            )

    print("\n-----------------------------------")
    print("RECOMENDAÇÕES")
    print("-----------------------------------")

    if not analise["recomendacoes"]:

        print("Nenhuma recomendação disponível.")

    else:

        for recomendacao in analise["recomendacoes"]:

            print(
                f"  • {recomendacao}"
            )

    print("\n-----------------------------------")
    print("PRIORIDADES PARA A PRÓXIMA SEMANA")
    print("-----------------------------------")

    if not analise["prioridades"]:

        print("Nenhuma prioridade definida.")

    else:

        for prioridade in analise["prioridades"]:

            print(
                f"  • {prioridade}"
            )

    print("\n===================================")


def gerar_relatorio_semana():
    """
    Gera o relatório dos últimos 7 dias
    e atualiza a memória.
    """

    hoje = datetime.now().date()

    data_inicio = hoje - timedelta(days=6)

    print("\nGerando relatório...")

    relatorio = gerar_relatorio(
        data_inicio=data_inicio.strftime(
            "%Y-%m-%d"
        ),

        data_fim=hoje.strftime(
            "%Y-%m-%d"
        )
    )

    print("\n===================================")
    print("       RELATÓRIO SEMANAL")
    print("===================================\n")

    mostrar_relatorio(relatorio)

    print("\nAtualizando memória...")

    atualizar_memoria(
        relatorio
    )

    print(
        "Memória atualizada com sucesso!"
    )


def mostrar_memoria():
    """
    Mostra as informações atualmente
    armazenadas na memória.
    """

    dados_memoria = carregar_memoria()

    memoria = dados_memoria["memoria"]

    print("\n===================================")
    print("          MINHA MEMÓRIA")
    print("===================================")

    for categoria, itens in memoria.items():

        nome_categoria = (
            categoria
            .replace("_", " ")
            .upper()
        )

        print(
            f"\n{nome_categoria}"
        )

        if not itens:

            print(
                "Nenhuma informação registrada."
            )

        else:

            for item in itens:

                print(f"- {item}")


def processar_comando(
    comando,
    sessao_id
):
    """
    Processa comandos especiais
    do sistema.
    """

    if comando == "/ajuda":

        mostrar_menu()

        return True

    if comando == "/estudar":

        registrar_estudo_manual()

        return True

    if comando == "/relatorio":

        gerar_relatorio_semana()

        return True

    if comando == "/memoria":

        mostrar_memoria()

        return True

    if comando == "/sair":

        print(
            "\nEncerrando a IA de Estudos."
        )

        return False

    return None


def main():

    sessao_id = iniciar_sessao()

    mostrar_menu()

    while True:

        mensagem = input(
            "\nVocê: "
        ).strip()

        if not mensagem:
            continue

        if mensagem.startswith("/"):

            resultado = processar_comando(
                mensagem.lower(),
                sessao_id
            )

            if resultado is False:
                break

            if resultado is True:
                continue

            print(
                "\nComando não reconhecido."
            )

            print(
                "Digite /ajuda para ver os comandos."
            )

            continue

        try:

            print(
                "\nIA: Pensando..."
            )

            resposta = conversar(
                sessao_id=sessao_id,
                mensagem_usuario=mensagem
            )

            print(
                f"\nIA: {resposta}"
            )

        except Exception as erro:

            print(
                f"\nErro ao conversar com a IA: {erro}"
            )


if __name__ == "__main__":
    main()