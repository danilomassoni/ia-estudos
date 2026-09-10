import customtkinter as ctk
from interface.estudo_view import EstudoView
from interface.chat_view import ChatView
from interface.relatorio_view import RelatorioView
from interface.memoria_view import MemoriaView
from interface.historico_view import HistoricoView
from interface.dashboard_view import DashboardView


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==============================
        # CONFIGURAÇÃO DA JANELA
        # ==============================

        self.title("IA de Estudos")

        self.geometry("1100x700")

        self.minsize(
            900,
            600
        )

        # Aparência
        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme(
            "blue"
        )

        # ==============================
        # CONFIGURAÇÃO DO GRID
        # ==============================

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # ==============================
        # COMPONENTES
        # ==============================

        self.criar_menu_lateral()

        self.criar_area_principal()

        # Página inicial
        self.mostrar_dashboard()

    # ==============================
    # MENU LATERAL
    # ==============================

    def criar_menu_lateral(self):

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.menu_lateral.grid_propagate(
            False
        )

        # ==============================
        # TÍTULO
        # ==============================

        titulo = ctk.CTkLabel(
            self.menu_lateral,
            text="🤖 IA DE ESTUDOS",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        titulo.pack(
            padx=20,
            pady=(30, 40)
        )

        # ==============================
        # BOTÕES
        # ==============================

        self.criar_botao_menu(
            "🏠  Início",
            self.mostrar_dashboard
        )

        self.criar_botao_menu(
            "📚  Estudar",
            self.mostrar_estudar
        )

        self.criar_botao_menu(
            "💬  Chat IA",
            self.mostrar_chat
        )

        self.criar_botao_menu(
            "📊  Relatório",
            self.mostrar_relatorio
        )

        self.criar_botao_menu(
            "🧠  Memória",
            self.mostrar_memoria
        )

        self.criar_botao_menu(
            "📈  Histórico",
            self.mostrar_historico
        )

        # ==============================
        # ESPAÇO
        # ==============================

        espaco = ctk.CTkLabel(
            self.menu_lateral,
            text=""
        )

        espaco.pack(
            expand=True
        )

        # ==============================
        # CONFIGURAÇÕES
        # ==============================

        self.criar_botao_menu(
            "⚙️  Configurações",
            self.mostrar_configuracoes
        )

    def criar_botao_menu(
        self,
        texto,
        comando
    ):

        botao = ctk.CTkButton(
            self.menu_lateral,
            text=texto,
            command=comando,
            height=45,
            anchor="w",
            fg_color="transparent",
            hover_color=(
                "#2b2b2b"
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        botao.pack(
            fill="x",
            padx=12,
            pady=4
        )

    # ==============================
    # ÁREA PRINCIPAL
    # ==============================

    def criar_area_principal(self):

        self.area_principal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )

        self.area_principal.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=30
        )

        self.area_principal.grid_columnconfigure(
            0,
            weight=1
        )

        self.area_principal.grid_rowconfigure(
            1,
            weight=1
        )

    # ==============================
    # LIMPAR ÁREA
    # ==============================

    def limpar_area(self):

        for widget in self.area_principal.winfo_children():

            widget.destroy()

    # ==============================
    # PÁGINA GENÉRICA
    # ==============================

    def mostrar_pagina(
        self,
        titulo,
        descricao
    ):

        self.limpar_area()

        titulo_label = ctk.CTkLabel(
            self.area_principal,
            text=titulo,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            anchor="w"
        )

        titulo_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        descricao_label = ctk.CTkLabel(
            self.area_principal,
            text=descricao,
            font=ctk.CTkFont(
                size=15
            ),
            anchor="w"
        )

        descricao_label.grid(
            row=1,
            column=0,
            sticky="nw"
        )

    # ==============================
    # INÍCIO
    # ==============================

    def mostrar_inicio(self):

        self.limpar_area()

        titulo = ctk.CTkLabel(
            self.area_principal,
            text="Olá, Danilo! 👋",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            anchor="w"
        )

        titulo.pack(
            anchor="w",
            pady=(0, 5)
        )

        subtitulo = ctk.CTkLabel(
            self.area_principal,
            text="Vamos continuar seus estudos?",
            font=ctk.CTkFont(
                size=16
            ),
            anchor="w"
        )

        subtitulo.pack(
            anchor="w",
            pady=(0, 30)
        )

        # ==============================
        # CARDS
        # ==============================

        cards = ctk.CTkFrame(
            self.area_principal,
            fg_color="transparent"
        )

        cards.pack(
            fill="x"
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
            "📚",
            "Estudos",
            "0 sessões",
            0
        )

        self.criar_card(
            cards,
            "⏱️",
            "Tempo estudado",
            "0 horas",
            1
        )

        self.criar_card(
            cards,
            "🎯",
            "Compreensão",
            "0,0 / 5",
            2
        )

        # ==============================
        # PRÓXIMOS ESTUDOS
        # ==============================

        prioridade = ctk.CTkFrame(
            self.area_principal
        )

        prioridade.pack(
            fill="both",
            expand=True,
            pady=(30, 0)
        )

        titulo_prioridade = ctk.CTkLabel(
            prioridade,
            text="🎯 Próximos passos",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        titulo_prioridade.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        texto = ctk.CTkLabel(
            prioridade,
            text=(
                "Ainda não existem dados suficientes "
                "para definir suas próximas prioridades.\n\n"
                "Comece registrando uma sessão de estudo."
            ),
            justify="left",
            anchor="w"
        )

        texto.pack(
            anchor="w",
            padx=20,
            pady=10
        )

    def criar_card(
        self,
        parent,
        icone,
        titulo,
        valor,
        coluna
    ):

        card = ctk.CTkFrame(
            parent,
            height=130
        )

        card.grid(
            row=0,
            column=coluna,
            sticky="nsew",
            padx=5
        )

        icone_label = ctk.CTkLabel(
            card,
            text=icone,
            font=ctk.CTkFont(
                size=25
            )
        )

        icone_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        titulo_label = ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(
                size=13
            )
        )

        titulo_label.pack(
            anchor="w",
            padx=20
        )

        valor_label = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        valor_label.pack(
            anchor="w",
            padx=20
        )

    # ==============================
    # ESTUDAR
    # ==============================

    def mostrar_estudar(self):

        self.limpar_area()

        self.estudo_view = EstudoView(
            self.area_principal
        )

        self.estudo_view.pack(
            fill="both",
            expand=True
        )

    def mostrar_chat(self):

        self.limpar_area()

        self.chat_view = ChatView(
            self.area_principal
        )

        self.chat_view.pack(
            fill="both",
            expand=True
        )

    # ==============================
    # RELATÓRIO
    # ==============================

    def mostrar_relatorio(self):

        self.limpar_area()

        self.relatorio_view = RelatorioView(
            self.area_principal
        )

        self.relatorio_view.pack(
            fill="both",
            expand=True
        )

    # ==============================
    # MEMÓRIA
    # ==============================

    def mostrar_memoria(self):

        self.limpar_area()

        self.memoria_view = MemoriaView(
            self.area_principal
        )

        self.memoria_view.pack(
            fill="both",
            expand=True
        )

    # ==============================
    # HISTÓRICO
    # ==============================

    def mostrar_historico(self):

        self.limpar_area()

        self.historico_view = HistoricoView(
            self.area_principal
        )

        self.historico_view.pack(
            fill="both",
            expand=True
        )
    # ==============================
    # CONFIGURAÇÕES
    # ==============================

    def mostrar_configuracoes(self):

        self.mostrar_pagina(
            "⚙️ Configurações",
            "Aqui ficarão as configurações da aplicação."
        )

    # ==============================
        # DASHBOARD
    # ==============================

    def mostrar_dashboard(self):

        self.limpar_area()

        self.dashboard_view = DashboardView(
            self.area_principal
        )

        self.dashboard_view.pack(
            fill="both",
            expand=True
        )


# ==============================
# EXECUÇÃO
# ==============================

if __name__ == "__main__":

    app = App()

    app.mainloop()