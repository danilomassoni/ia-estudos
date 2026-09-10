import uuid

import customtkinter as ctk

from services.conversa_service import conversar


class ChatView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.sessao_id = str(uuid.uuid4())

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

        self.grid_rowconfigure(
            2,
            weight=0
        )

        # ==============================
        # CABEÇALHO
        # ==============================

        titulo = ctk.CTkLabel(
            self,
            text="💬 Chat IA",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 15)
        )

        # ==============================
        # ÁREA DO CHAT
        # ==============================

        self.area_chat = ctk.CTkTextbox(
            self,
            wrap="word",
            state="disabled"
        )

        self.area_chat.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(0, 15)
        )

        # ==============================
        # ÁREA DE ENVIO
        # ==============================

        area_envio = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        area_envio.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        area_envio.grid_columnconfigure(
            0,
            weight=1
        )

        self.entrada = ctk.CTkEntry(
            area_envio,
            height=45,
            placeholder_text=(
                "Digite sua dúvida ou o que você está estudando..."
            )
        )

        self.entrada.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self.botao_enviar = ctk.CTkButton(
            area_envio,
            text="Enviar",
            width=100,
            height=45,
            command=self.enviar_mensagem
        )

        self.botao_enviar.grid(
            row=0,
            column=1
        )

        # Permite enviar com Enter
        self.entrada.bind(
            "<Return>",
            self.enviar_com_enter
        )

        # ==============================
        # MENSAGEM INICIAL
        # ==============================

        self.adicionar_mensagem(
            "IA",
            (
                "Olá! 👋\n\n"
                "Sou sua IA de Estudos. "
                "Você pode tirar dúvidas, explicar o que "
                "está estudando ou conversar sobre seus "
                "estudos.\n\n"
                "Por onde começamos?"
            )
        )

    # ==============================
    # ADICIONAR MENSAGEM
    # ==============================

    def adicionar_mensagem(
        self,
        remetente,
        mensagem
    ):

        self.area_chat.configure(
            state="normal"
        )

        self.area_chat.insert(
            "end",
            f"{remetente}:\n"
        )

        self.area_chat.insert(
            "end",
            f"{mensagem}\n\n"
        )

        self.area_chat.see(
            "end"
        )

        self.area_chat.configure(
            state="disabled"
        )

    # ==============================
    # ENVIAR COM ENTER
    # ==============================

    def enviar_com_enter(self, event):

        self.enviar_mensagem()

        return "break"

    # ==============================
    # ENVIAR MENSAGEM
    # ==============================

    def enviar_mensagem(self):

        mensagem = self.entrada.get().strip()

        if not mensagem:
            return

        # ==============================
        # MOSTRAR MENSAGEM DO USUÁRIO
        # ==============================

        self.adicionar_mensagem(
            "Você",
            mensagem
        )

        self.entrada.delete(
            0,
            "end"
        )

        # ==============================
        # BLOQUEAR ENVIO
        # ==============================

        self.botao_enviar.configure(
            state="disabled",
            text="Pensando..."
        )

        self.entrada.configure(
            state="disabled"
        )

        # ==============================
        # EXECUTAR IA
        # ==============================

        self.after(
            100,
            lambda: self.processar_mensagem(
                mensagem
            )
        )

    # ==============================
    # PROCESSAR
    # ==============================

    def processar_mensagem(
        self,
        mensagem
    ):

        try:

            resposta = conversar(
                sessao_id=self.sessao_id,
                mensagem_usuario=mensagem
            )

            self.adicionar_mensagem(
                "IA",
                resposta
            )

        except Exception as erro:

            self.adicionar_mensagem(
                "Sistema",
                f"❌ Erro ao conversar com a IA:\n{erro}"
            )

        finally:

            self.botao_enviar.configure(
                state="normal",
                text="Enviar"
            )

            self.entrada.configure(
                state="normal"
            )

            self.entrada.focus()