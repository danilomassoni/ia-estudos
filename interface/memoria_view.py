import customtkinter as ctk

from services.memoria_service import carregar_memoria


class MemoriaView(ctk.CTkFrame):

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
            text="🧠 Minha memória",
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
        # ÁREA DA MEMÓRIA
        # ==============================

        self.area_memoria = ctk.CTkScrollableFrame(
            self
        )

        self.area_memoria.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.carregar()

    # ==============================
    # CARREGAR MEMÓRIA
    # ==============================

    def carregar(self):

        for widget in self.area_memoria.winfo_children():

            widget.destroy()

        try:

            dados = carregar_memoria()

            memoria = dados.get(
                "memoria",
                {}
            )

            self.mostrar_memoria(
                memoria
            )

        except Exception as erro:

            erro_label = ctk.CTkLabel(
                self.area_memoria,
                text=(
                    "❌ Erro ao carregar memória:\n\n"
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
    # MOSTRAR MEMÓRIA
    # ==============================

    def mostrar_memoria(
        self,
        memoria
    ):

        categorias = [
            (
                "💪",
                "Pontos fortes",
                "pontos_fortes"
            ),
            (
                "⚠️",
                "Dificuldades recorrentes",
                "dificuldades_recorrentes"
            ),
            (
                "🔎",
                "Lacunas de conhecimento",
                "lacunas_conhecimento"
            ),
            (
                "🧩",
                "Padrões de aprendizagem",
                "padroes_aprendizagem"
            ),
            (
                "👀",
                "Preferências observadas",
                "preferencias_observadas"
            ),
            (
                "📚",
                "Assuntos para revisar",
                "assuntos_para_revisar"
            ),
            (
                "📈",
                "Evolução dos conhecimentos",
                "evolucao_conhecimentos"
            ),
            (
                "📝",
                "Observações importantes",
                "observacoes_importantes"
            )
        ]

        for icone, titulo, chave in categorias:

            itens = memoria.get(
                chave,
                []
            )

            self.criar_categoria(
                icone=icone,
                titulo=titulo,
                itens=itens
            )

    # ==============================
    # CATEGORIA
    # ==============================

    def criar_categoria(
        self,
        icone,
        titulo,
        itens
    ):

        # ==============================
        # CONTAINER
        # ==============================

        card = ctk.CTkFrame(
            self.area_memoria
        )

        card.pack(
            fill="x",
            padx=10,
            pady=6
        )

        # ==============================
        # TÍTULO
        # ==============================

        titulo_label = ctk.CTkLabel(
            card,
            text=f"{icone}  {titulo}",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            anchor="w"
        )

        titulo_label.pack(
            fill="x",
            padx=20,
            pady=(15, 8)
        )

        # ==============================
        # CONTEÚDO
        # ==============================

        if not itens:

            vazio = ctk.CTkLabel(
                card,
                text="Nenhuma informação registrada ainda.",
                font=ctk.CTkFont(
                    size=13
                ),
                anchor="w"
            )

            vazio.pack(
                fill="x",
                padx=20,
                pady=(0, 15)
            )

            return

        for item in itens:

            texto = self.formatar_item(
                item
            )

            item_label = ctk.CTkLabel(
                card,
                text=f"• {texto}",
                font=ctk.CTkFont(
                    size=14
                ),
                justify="left",
                anchor="w",
                wraplength=750
            )

            item_label.pack(
                fill="x",
                padx=25,
                pady=(2, 5)
            )

        # Espaçamento final

        ctk.CTkLabel(
            card,
            text=""
        ).pack(
            pady=5
        )

    # ==============================
    # FORMATAR ITEM
    # ==============================

    def formatar_item(
        self,
        item
    ):

        if isinstance(
            item,
            str
        ):

            return item

        if isinstance(
            item,
            dict
        ):

            partes = []

            for chave, valor in item.items():

                nome = (
                    chave
                    .replace("_", " ")
                    .capitalize()
                )

                partes.append(
                    f"{nome}: {valor}"
                )

            return " | ".join(
                partes
            )

        return str(item)