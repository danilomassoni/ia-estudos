import customtkinter as ctk

from services.estudo_service import listar_estudos


class HistoricoView(ctk.CTkFrame):

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
            text="📈 Histórico de estudos",
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

        botao_atualizar = ctk.CTkButton(
            cabecalho,
            text="🔄 Atualizar",
            width=120,
            height=40,
            command=self.carregar
        )

        botao_atualizar.grid(
            row=0,
            column=1
        )

        # ==============================
        # ÁREA DO HISTÓRICO
        # ==============================

        self.area_historico = ctk.CTkScrollableFrame(
            self
        )

        self.area_historico.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.carregar()

    # ==============================
    # CARREGAR
    # ==============================

    def carregar(self):

        for widget in self.area_historico.winfo_children():

            widget.destroy()

        try:

            estudos = listar_estudos()

            # Mais recentes primeiro
            estudos = sorted(
                estudos,
                key=lambda estudo: (
                    estudo.get("data", ""),
                    estudo.get("hora_inicio", "")
                ),
                reverse=True
            )

            self.mostrar_estudos(
                estudos
            )

        except Exception as erro:

            erro_label = ctk.CTkLabel(
                self.area_historico,
                text=(
                    "❌ Erro ao carregar histórico:\n\n"
                    f"{erro}"
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

    # ==============================
    # MOSTRAR ESTUDOS
    # ==============================

    def mostrar_estudos(
        self,
        estudos
    ):

        if not estudos:

            vazio = ctk.CTkLabel(
                self.area_historico,
                text=(
                    "📚 Nenhum estudo registrado ainda.\n\n"
                    "Comece registrando sua primeira sessão."
                ),
                font=ctk.CTkFont(
                    size=15
                ),
                justify="left"
            )

            vazio.pack(
                anchor="w",
                padx=20,
                pady=30
            )

            return

        # ==============================
        # RESUMO
        # ==============================

        resumo = ctk.CTkLabel(
            self.area_historico,
            text=(
                f"Total de sessões registradas: "
                f"{len(estudos)}"
            ),
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        resumo.pack(
            anchor="w",
            padx=10,
            pady=(5, 15)
        )

        # ==============================
        # CARDS
        # ==============================

        for estudo in estudos:

            self.criar_card_estudo(
                estudo
            )

    # ==============================
    # CARD DE ESTUDO
    # ==============================

    def criar_card_estudo(
        self,
        estudo
    ):

        card = ctk.CTkFrame(
            self.area_historico
        )

        card.pack(
            fill="x",
            padx=10,
            pady=6
        )

        # ==============================
        # CABEÇALHO DO CARD
        # ==============================

        cabecalho = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        cabecalho.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        cabecalho.grid_columnconfigure(
            0,
            weight=1
        )

        assunto = estudo.get(
            "assunto",
            "Sem assunto"
        )

        topico = estudo.get(
            "topico",
            "Sem tópico"
        )

        titulo = ctk.CTkLabel(
            cabecalho,
            text=f"📚 {assunto} — {topico}",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            anchor="w"
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w"
        )

        data = estudo.get(
            "data",
            "-"
        )

        hora = estudo.get(
            "hora_inicio",
            "-"
        )

        data_label = ctk.CTkLabel(
            cabecalho,
            text=f"{data}  •  {hora}",
            font=ctk.CTkFont(
                size=12
            )
        )

        data_label.grid(
            row=0,
            column=1,
            padx=(10, 0)
        )

        # ==============================
        # INFORMAÇÕES
        # ==============================

        duracao = estudo.get(
            "duracao_minutos",
            0
        )

        compreensao = estudo.get(
            "compreensao",
            0
        )

        informacoes = ctk.CTkLabel(
            card,
            text=(
                f"⏱️ {duracao} minutos    "
                f"•    🎯 Compreensão: "
                f"{compreensao}/5"
            ),
            font=ctk.CTkFont(
                size=13
            ),
            anchor="w"
        )

        informacoes.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # ==============================
        # CONTEÚDO
        # ==============================

        conteudo = estudo.get(
            "conteudo",
            ""
        )

        if conteudo:

            self.criar_campo(
                card,
                "📖 O que estudou",
                conteudo
            )

        # ==============================
        # DIFICULDADES
        # ==============================

        dificuldades = estudo.get(
            "dificuldades",
            []
        )

        if dificuldades:

            self.criar_campo(
                card,
                "⚠️ Dificuldades",
                self.formatar_lista(
                    dificuldades
                )
            )

        # ==============================
        # APRENDIZADOS
        # ==============================

        aprendizados = estudo.get(
            "aprendizados",
            []
        )

        if aprendizados:

            self.criar_campo(
                card,
                "💡 Aprendizados",
                self.formatar_lista(
                    aprendizados
                )
            )

        # ==============================
        # PRÓXIMO PASSO
        # ==============================

        proximo_passo = estudo.get(
            "proximo_passo"
        )

        if proximo_passo:

            self.criar_campo(
                card,
                "🎯 Próximo passo",
                proximo_passo
            )

        # ==============================
        # ESPAÇAMENTO
        # ==============================

        ctk.CTkLabel(
            card,
            text=""
        ).pack(
            pady=5
        )

    # ==============================
    # CAMPO
    # ==============================

    def criar_campo(
        self,
        parent,
        titulo,
        texto
    ):

        titulo_label = ctk.CTkLabel(
            parent,
            text=titulo,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            anchor="w"
        )

        titulo_label.pack(
            fill="x",
            padx=20,
            pady=(3, 2)
        )

        texto_label = ctk.CTkLabel(
            parent,
            text=texto,
            font=ctk.CTkFont(
                size=13
            ),
            justify="left",
            anchor="w",
            wraplength=750
        )

        texto_label.pack(
            fill="x",
            padx=30,
            pady=(0, 6)
        )

    # ==============================
    # FORMATAR LISTA
    # ==============================

    def formatar_lista(
        self,
        itens
    ):

        return "\n".join(
            f"• {item}"
            for item in itens
        )