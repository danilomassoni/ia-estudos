from services.revisao_service import (
    carregar_revisoes,
    obter_progresso_revisao
)


revisoes = carregar_revisoes()

if not revisoes:
    raise ValueError(
        "Nenhuma revisão encontrada."
    )

revisao = revisoes[-1]

progresso = obter_progresso_revisao(
    revisao["id"]
)

print("=" * 60)
print("PROGRESSO DA REVISÃO")
print("=" * 60)

print(
    f"Revisão: {revisao['id']}"
)

print(
    f"Status: {revisao['status']}"
)

print(
    f"Total de perguntas: {progresso['total']}"
)

print(
    f"Respondidas: {progresso['respondidas']}"
)

print(
    f"Pendentes: {progresso['pendentes']}"
)

print(
    f"Progresso: {progresso['percentual']}%"
)