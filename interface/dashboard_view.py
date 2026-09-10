import customtkinter as ctk

from services.dashboard_service import (
    gerar_resumo_dashboard
)


class DashboardView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.criar_interface()

    def criar_interface(self):

        # ==============================
        # CABEÇALHO
        # ==============================

        titulo = ctk.CTkLabel(
            self,
            text="🏠 Dashboard",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        subtitulo = ctk.CTkLabel(
            self,
            text="Visão geral dos seus estudos nos últimos 7 dias",
            font=ctk.CTkFont(
                size=14
            ),
            text_color="gray"
        )

        subtitulo.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        # ==============================
        # CONTAINER PRINCIPAL
        # ==============================

        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.carregar_dashboard()

    def carregar_dashboard(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        dados = gerar_resumo_dashboard()

        estatisticas = dados[
            "estatisticas"
        ]

        # ==============================
        # CARDS
        # ==============================

        cards = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=(0, 20)
        )

        cards.grid_columnconfigure(
            0,
            weight=1
        )

        cards.grid_columnconfigure(
            1,
            weight=1
        )

        cards.grid_columnconfigure(
            2,
            weight=1
        )

        self.criar_card(
            cards,
            "📚 SESSÕES",
            str(
                estatisticas["sessoes"]
            ),
            0
        )

        self.criar_card(
            cards,
            "⏱️ TEMPO",
            f'{estatisticas["tempo_total_horas"]}h',
            1
        )

        self.criar_card(
            cards,
            "🎯 COMPREENSÃO",
            f'{estatisticas["compreensao_media"]}/5',
            2
        )

        # ==============================
        # ASSUNTOS
        # ==============================

        self.criar_secao(
            "📚 Assuntos mais estudados"
        )

        assuntos = dados[
            "assuntos_mais_estudados"
        ]

        if assuntos:

            maior_quantidade = max(
                quantidade
                for _, quantidade in assuntos
            )

            for assunto, quantidade in assuntos:

                linha = ctk.CTkFrame(
                    self.container,
                    fg_color="transparent"
                )

                linha.pack(
                    fill="x",
                    pady=5
                )

                nome = ctk.CTkLabel(
                    linha,
                    text=assunto,
                    width=180,
                    anchor="w"
                )

                nome.pack(
                    side="left"
                )

                barra = ctk.CTkProgressBar(
                    linha
                )

                barra.pack(
                    side="left",
                    fill="x",
                    expand=True,
                    padx=10
                )

                barra.set(
                    quantidade /
                    maior_quantidade
                )

                total = ctk.CTkLabel(
                    linha,
                    text=str(quantidade)
                )

                total.pack(
                    side="right"
                )

        else:

            self.criar_texto_vazio(
                "Nenhum estudo registrado nos últimos 7 dias."
            )

        # ==============================
        # PONTOS DE ATENÇÃO
        # ==============================

        self.criar_secao(
            "⚠️ Pontos que precisam de atenção"
        )

        pontos = dados[
            "pontos_atencao"
        ]

        if pontos:

            for ponto in pontos:

                if "dificuldade" in ponto:

                    texto = (
                        f'• {ponto["assunto"]} — '
                        f'{ponto["topico"]}: '
                        f'{ponto["dificuldade"]}'
                    )

                else:

                    texto = (
                        f'• {ponto["assunto"]} — '
                        f'{ponto["topico"]} '
                        f'(compreensão '
                        f'{ponto["compreensao"]}/5)'
                    )

                self.criar_texto(
                    texto
                )

        else:

            self.criar_texto_vazio(
                "Nenhum ponto de atenção identificado."
            )

        # ==============================
        # PRIORIDADES
        # ==============================

        self.criar_secao(
            "🎯 Próximas prioridades"
        )

        prioridades = dados[
            "prioridades"
        ]

        if prioridades:

            for indice, prioridade in enumerate(
                prioridades,
                start=1
            ):

                self.criar_texto(
                    f"{indice}. {self.formatar_item(prioridade)}"
                )

        else:

            self.criar_texto_vazio(
                "Ainda não existem prioridades definidas."
            )

        # ==============================
        # ESTUDOS RECENTES
        # ==============================

        self.criar_secao(
            "🕐 Estudos recentes"
        )

        estudos = dados[
            "estudos_recentes"
        ]

        if estudos:

            for estudo in estudos:

                texto = (
                    f'📚 {estudo["assunto"]} — '
                    f'{estudo["topico"]}\n'
                    f'   {estudo["data"]} às '
                    f'{estudo["hora_inicio"]} • '
                    f'{estudo["duracao_minutos"]} min • '
                    f'compreensão '
                    f'{estudo["compreensao"]}/5'
                )

                self.criar_texto(
                    texto
                )

        else:

            self.criar_texto_vazio(
                "Nenhum estudo registrado."
            )

    def criar_card(
        self,
        parent,
        titulo,
        valor,
        coluna
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=coluna,
            sticky="nsew",
            padx=5
        )

        label_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        label_titulo.pack(
            pady=(15, 5)
        )

        label_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        label_valor.pack(
            pady=(0, 15)
        )

    def criar_secao(self, titulo):

        label = ctk.CTkLabel(
            self.container,
            text=titulo,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        label.pack(
            anchor="w",
            pady=(15, 10)
        )

    def criar_texto(self, texto):

        label = ctk.CTkLabel(
            self.container,
            text=texto,
            justify="left",
            anchor="w",
            wraplength=850
        )

        label.pack(
            fill="x",
            anchor="w",
            pady=3
        )

    def criar_texto_vazio(self, texto):

        label = ctk.CTkLabel(
            self.container,
            text=texto,
            text_color="gray",
            anchor="w"
        )

        label.pack(
            fill="x",
            anchor="w",
            pady=5
        )

    def formatar_item(self, item):

        if isinstance(item, str):
            return item

        if isinstance(item, dict):

            partes = []

            for chave, valor in item.items():

                partes.append(
                    f"{chave}: {valor}"
                )

            return " | ".join(
                partes
            )

        return str(item)