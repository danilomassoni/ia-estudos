import customtkinter as ctk
from datetime import datetime, timedelta

from services.relatorio_service import gerar_relatorio
from services.memoria_service import atualizar_memoria


class RelatorioView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.criar_interface()

    # ==============================
    # INTERFACE
    # ==============================

    def criar_interface(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # ==============================
        # CABEÇALHO
        # ==============================

        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        cabecalho.grid_columnconfigure(
            0,
            weight=1
        )

        titulo = ctk.CTkLabel(
            cabecalho,
            text="📊 Relatório semanal",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.botao_gerar = ctk.CTkButton(
            cabecalho,
            text="🔄 Gerar relatório",
            width=160,
            height=40,
            command=self.gerar
        )

        self.botao_gerar.grid(
            row=0,
            column=1,
            padx=(10, 0)
        )

        # ==============================
        # ÁREA DO RELATÓRIO
        # ==============================

        self.area_relatorio = ctk.CTkScrollableFrame(
            self
        )

        self.area_relatorio.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.mostrar_mensagem_inicial()

    # ==============================
    # MENSAGEM INICIAL
    # ==============================

    def mostrar_mensagem_inicial(self):

        mensagem = ctk.CTkLabel(
            self.area_relatorio,
            text=(
                "Seu relatório semanal aparecerá aqui.\n\n"
                "Clique em 'Gerar relatório' para analisar "
                "seus estudos dos últimos 7 dias."
            ),
            font=ctk.CTkFont(
                size=15
            ),
            justify="left"
        )

        mensagem.pack(
            anchor="w",
            padx=20,
            pady=30
        )

    # ==============================
    # LIMPAR
    # ==============================

    def limpar_relatorio(self):

        for widget in self.area_relatorio.winfo_children():

            widget.destroy()

    # ==============================
    # GERAR
    # ==============================

    def gerar(self):

        self.botao_gerar.configure(
            state="disabled",
            text="Gerando..."
        )

        self.limpar_relatorio()

        carregando = ctk.CTkLabel(
            self.area_relatorio,
            text="🤖 Analisando seus estudos...",
            font=ctk.CTkFont(
                size=16
            )
        )

        carregando.pack(
            anchor="w",
            padx=20,
            pady=30
        )

        self.after(
            100,
            self.processar_relatorio
        )

    # ==============================
    # PROCESSAR
    # ==============================

    def processar_relatorio(self):

        try:

            hoje = datetime.now().date()

            data_inicio = (
                hoje - timedelta(days=6)
            )

            relatorio = gerar_relatorio(
                data_inicio=data_inicio.strftime(
                    "%Y-%m-%d"
                ),
                data_fim=hoje.strftime(
                    "%Y-%m-%d"
                )
            )

            # ==============================
            # ATUALIZAR MEMÓRIA
            # ==============================

            atualizar_memoria(
                relatorio
            )

            # ==============================
            # MOSTRAR
            # ==============================

            self.mostrar_relatorio(
                relatorio
            )

        except Exception as erro:

            self.limpar_relatorio()

            erro_label = ctk.CTkLabel(
                self.area_relatorio,
                text=(
                    "❌ Não foi possível gerar "
                    f"o relatório.\n\n{erro}"
                ),
                font=ctk.CTkFont(
                    size=15
                ),
                justify="left"
            )

            erro_label.pack(
                anchor="w",
                padx=20,
                pady=30
            )

        finally:

            self.botao_gerar.configure(
                state="normal",
                text="🔄 Gerar relatório"
            )

    # ==============================
    # MOSTRAR RELATÓRIO
    # ==============================

    def mostrar_relatorio(
        self,
        relatorio
    ):

        self.limpar_relatorio()

        periodo = relatorio.get(
            "periodo",
            {}
        )

        estatisticas = relatorio.get(
            "estatisticas",
            {}
        )

        analise = relatorio.get(
            "analise",
            {}
        )

        # ==============================
        # PERÍODO
        # ==============================

        self.criar_secao(
            "📅 Período"
        )

        periodo_texto = (
            f"{periodo.get('inicio', '-')} "
            f"até "
            f"{periodo.get('fim', '-')}"
        )

        self.criar_texto(
            periodo_texto
        )

        # ==============================
        # ESTATÍSTICAS
        # ==============================

        self.criar_secao(
            "📈 Estatísticas"
        )

        sessoes = estatisticas.get(
            "sessoes",
            0
        )

        tempo_horas = estatisticas.get(
            "tempo_total_horas",
            0
        )

        compreensao = estatisticas.get(
            "compreensao_media",
            0
        )

        assuntos = estatisticas.get(
            "assuntos_estudados",
            []
        )

        texto_estatisticas = (
            f"Sessões: {sessoes}\n"
            f"Tempo estudado: {tempo_horas} horas\n"
            f"Compreensão média: {compreensao} / 5\n"
            f"Assuntos: {', '.join(assuntos) if assuntos else 'Nenhum'}"
        )

        self.criar_texto(
            texto_estatisticas
        )

        # ==============================
        # FATOS
        # ==============================

        self.criar_secao(
            "🔎 Fatos observados"
        )

        self.criar_lista(
            analise.get(
                "fatos_observados",
                []
            )
        )

        # ==============================
        # INTERPRETAÇÕES
        # ==============================

        self.criar_secao(
            "🧠 Interpretações"
        )

        self.criar_lista(
            analise.get(
                "interpretacoes",
                []
            )
        )

        # ==============================
        # RECOMENDAÇÕES
        # ==============================

        self.criar_secao(
            "💡 Recomendações"
        )

        self.criar_lista(
            analise.get(
                "recomendacoes",
                []
            )
        )

        # ==============================
        # PRIORIDADES
        # ==============================

        self.criar_secao(
            "🎯 Prioridades"
        )

        prioridades = analise.get(
            "prioridades",
            []
        )

        if prioridades:

            for prioridade in prioridades:

                card = ctk.CTkFrame(
                    self.area_relatorio
                )

                card.pack(
                    fill="x",
                    padx=10,
                    pady=5
                )

                texto = ctk.CTkLabel(
                    card,
                    text=f"🎯  {prioridade}",
                    font=ctk.CTkFont(
                        size=14,
                        weight="bold"
                    ),
                    anchor="w"
                )

                texto.pack(
                    fill="x",
                    padx=15,
                    pady=15
                )

        else:

            self.criar_texto(
                "Nenhuma prioridade identificada."
            )

        # ==============================
        # FIM
        # ==============================

        final = ctk.CTkLabel(
            self.area_relatorio,
            text="✅ Relatório atualizado e memória processada.",
            font=ctk.CTkFont(
                size=13
            )
        )

        final.pack(
            anchor="w",
            padx=20,
            pady=30
        )

    # ==============================
    # SEÇÃO
    # ==============================

    def criar_secao(
        self,
        titulo
    ):

        label = ctk.CTkLabel(
            self.area_relatorio,
            text=titulo,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            anchor="w"
        )

        label.pack(
            fill="x",
            padx=10,
            pady=(20, 8)
        )

    # ==============================
    # TEXTO
    # ==============================

    def criar_texto(
        self,
        texto
    ):

        label = ctk.CTkLabel(
            self.area_relatorio,
            text=texto,
            font=ctk.CTkFont(
                size=14
            ),
            justify="left",
            anchor="w"
        )

        label.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

    # ==============================
    # LISTA
    # ==============================

    def criar_lista(
        self,
        itens
    ):

        if not itens:

            self.criar_texto(
                "Nenhuma informação registrada."
            )

            return

        for item in itens:

            label = ctk.CTkLabel(
                self.area_relatorio,
                text=f"• {item}",
                font=ctk.CTkFont(
                    size=14
                ),
                justify="left",
                anchor="w",
                wraplength=750
            )

            label.pack(
                fill="x",
                padx=25,
                pady=3
            )