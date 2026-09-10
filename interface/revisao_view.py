import customtkinter as ctk


from services.revisao_service import (
    listar_assuntos_disponiveis,
    listar_topicos_disponiveis,
    gerar_revisao,
    obter_proxima_pergunta,
    obter_progresso_revisao,
    responder_pergunta
)

class RevisaoView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.assuntos = []
        self.topicos = []

        self.revisao_atual = None
        self.progresso_atual = None

        self.criar_interface()

    def criar_interface(self):

        titulo = ctk.CTkLabel(
            self,
            text="Revisão Inteligente",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        subtitulo = ctk.CTkLabel(
            self,
            text=(
                "Revise seus estudos com perguntas "
                "geradas pela IA."
            ),
            font=ctk.CTkFont(size=14)
        )

        subtitulo.pack(
            anchor="w",
            padx=30,
            pady=(0, 25)
        )

        self.criar_periodo()

        self.criar_selecao_assunto()

        self.criar_selecao_topicos()

        self.criar_opcoes()

        self.criar_botao()

        self.criar_status()

    def criar_periodo(self):

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        titulo = ctk.CTkLabel(
            frame,
            text="Período",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        campos = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        campos.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        self.data_inicio = ctk.CTkEntry(
            campos,
            placeholder_text="DD/MM/AAAA"
        )

        self.data_inicio.pack(
            side="left",
            padx=(0, 10)
        )

        self.data_fim = ctk.CTkEntry(
            campos,
            placeholder_text="DD/MM/AAAA"
        )

        self.data_fim.pack(
            side="left",
            padx=10
        )

        botao = ctk.CTkButton(
            campos,
            text="Carregar estudos",
            command=self.carregar_estudos
        )

        botao.pack(
            side="left",
            padx=10
        )

    def criar_selecao_assunto(self):

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        titulo = ctk.CTkLabel(
            frame,
            text="Assunto",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        self.assunto_combo = ctk.CTkComboBox(
            frame,
            values=["Carregue um período primeiro"],
            command=self.assunto_selecionado
        )

        self.assunto_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

    def criar_selecao_topicos(self):

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        titulo = ctk.CTkLabel(
            frame,
            text="Tópicos",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        self.topicos_combo = ctk.CTkComboBox(
            frame,
            values=["Selecione um assunto"]
        )

        self.topicos_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

    def criar_opcoes(self):

        frame = ctk.CTkFrame(self)

        frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        titulo = ctk.CTkLabel(
            frame,
            text="Configurações da revisão",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        linha = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        linha.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        quantidade_label = ctk.CTkLabel(
            linha,
            text="Perguntas:"
        )

        quantidade_label.pack(
            side="left",
            padx=(0, 10)
        )

        self.quantidade_combo = ctk.CTkComboBox(
            linha,
            values=[
                "5",
                "10",
                "15",
                "20"
            ]
        )

        self.quantidade_combo.set("5")

        self.quantidade_combo.pack(
            side="left",
            padx=(0, 30)
        )

        dificuldade_label = ctk.CTkLabel(
            linha,
            text="Dificuldade:"
        )

        dificuldade_label.pack(
            side="left",
            padx=(0, 10)
        )

        self.dificuldade_combo = ctk.CTkComboBox(
            linha,
            values=[
                "adaptativa",
                "facil",
                "media",
                "alta"
            ]
        )

        self.dificuldade_combo.set(
            "adaptativa"
        )

        self.dificuldade_combo.pack(
            side="left"
        )

    def criar_botao(self):

        self.botao_iniciar = ctk.CTkButton(
            self,
            text="Iniciar Revisão",
            height=45,
            command=self.iniciar_revisao
        )

        self.botao_iniciar.pack(
            padx=30,
            pady=20
        )

    def criar_status(self):

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13)
        )

        self.status_label.pack(
            padx=30,
            pady=(0, 20)
        )

    def carregar_estudos(self):

        data_inicio = self.converter_data(
            self.data_inicio.get()
        )

        data_fim = self.converter_data(
            self.data_fim.get()
        )

        if not data_inicio or not data_fim:
            self.mostrar_status(
                "Informe as duas datas."
            )
            return

        try:

            assuntos = listar_assuntos_disponiveis(
                data_inicio,
                data_fim
            )

            self.assuntos = assuntos

            if not assuntos:
                self.assunto_combo.configure(
                    values=["Nenhum estudo encontrado"]
                )

                self.mostrar_status(
                    "Nenhum estudo encontrado nesse período."
                )

                return

            self.assunto_combo.configure(
                values=assuntos
            )

            self.assunto_combo.set(
                assuntos[0]
            )

            self.assunto_selecionado(
                assuntos[0]
            )

            self.mostrar_status(
                f"{len(assuntos)} assunto(s) encontrado(s)."
            )

        except Exception as erro:

            self.mostrar_status(
                f"Erro: {erro}"
            )

    def assunto_selecionado(self, assunto):

        if not assunto:
            return

        data_inicio = self.converter_data(
            self.data_inicio.get()
        )

        data_fim = self.converter_data(
            self.data_fim.get()
        )

        if not data_inicio or not data_fim:
            return

        try:

            topicos = listar_topicos_disponiveis(
                data_inicio,
                data_fim,
                assunto
            )

            self.topicos = topicos

            if not topicos:

                self.topicos_combo.configure(
                    values=["Nenhum tópico encontrado"]
                )

                return

            self.topicos_combo.configure(
                values=topicos
            )

            self.topicos_combo.set(
                topicos[0]
            )

        except Exception as erro:

            self.mostrar_status(
                f"Erro: {erro}"
            )

    def iniciar_revisao(self):

        data_inicio = self.converter_data(
            self.data_inicio.get()
        )

        data_fim = self.converter_data(
            self.data_fim.get()
        )

        assunto = self.assunto_combo.get()

        topico = self.topicos_combo.get()

        quantidade = int(
            self.quantidade_combo.get()
        )

        dificuldade = self.dificuldade_combo.get()

        if not data_inicio or not data_fim:
            self.mostrar_status(
                "Informe o período da revisão."
            )
            return

        if not assunto or assunto in [
            "Nenhum estudo encontrado",
            "Carregue um período primeiro"
        ]:
            self.mostrar_status(
                "Selecione um assunto."
            )
            return

        if not topico or topico in [
            "Nenhum tópico encontrado",
            "Selecione um assunto"
        ]:
            self.mostrar_status(
                "Selecione um tópico."
            )
            return

        try:

            self.mostrar_status(
                "Gerando perguntas..."
            )

            self.update_idletasks()

            revisao = gerar_revisao(
                data_inicio=data_inicio,
                data_fim=data_fim,
                assunto=assunto,
                topicos=[topico],
                quantidade_perguntas=quantidade,
                dificuldade=dificuldade
            )

            self.revisao_atual = revisao

            self.mostrar_pergunta()

        except Exception as erro:

            self.mostrar_status(
                f"Erro ao criar revisão: {erro}"
            )

    def converter_data(self, data):

        try:

            partes = data.strip().split("/")

            if len(partes) != 3:
                return None

            dia, mes, ano = partes

            return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"

        except Exception:

            return None

    def mostrar_status(self, mensagem):

        try:

            self.status_label.configure(
                text=mensagem
            )

        except Exception:

            pass

    def mostrar_pergunta(self):

        self.limpar_interface()

        if not self.revisao_atual:
            return

        revisao_id = self.revisao_atual["id"]

        pergunta = obter_proxima_pergunta(
            revisao_id
        )

        if pergunta is None:
            self.mostrar_resultado()
            return

        progresso = obter_progresso_revisao(
            revisao_id
        )

        self.progresso_atual = progresso

        titulo = ctk.CTkLabel(
            self,
            text="🧠 Revisão Inteligente",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        subtitulo = ctk.CTkLabel(
            self,
            text=(
                f"{self.revisao_atual['assunto']} "
                f"• {', '.join(self.revisao_atual['topicos'])}"
            ),
            font=ctk.CTkFont(
                size=15
            )
        )

        subtitulo.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        progresso_texto = ctk.CTkLabel(
            self,
            text=(
                f"Pergunta "
                f"{progresso['respondidas'] + 1} "
                f"de {progresso['total']}"
            ),
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        progresso_texto.pack(
            anchor="w",
            padx=30
        )

        barra = ctk.CTkProgressBar(
            self
        )

        barra.pack(
            fill="x",
            padx=30,
            pady=(8, 25)
        )

        barra.set(
            progresso["percentual"] / 100
        )

        card = ctk.CTkFrame(
            self
        )

        card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        info = ctk.CTkLabel(
            card,
            text=(
                f"Tópico: {pergunta['topico']}    "
                f"•    Tipo: {pergunta['tipo']}    "
                f"•    Dificuldade: {pergunta['dificuldade']}"
            ),
            font=ctk.CTkFont(
                size=13
            )
        )

        info.pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        enunciado = ctk.CTkLabel(
            card,
            text=pergunta["enunciado"],
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            wraplength=800,
            justify="left",
            anchor="w"
        )

        enunciado.pack(
            fill="x",
            padx=25,
            pady=(10, 25)
        )

        self.resposta_textbox = ctk.CTkTextbox(
            card,
            height=180
        )

        self.resposta_textbox.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        self.botao_responder = ctk.CTkButton(
            card,
            text="Responder",
            height=45,
            command=lambda: self.enviar_resposta(
                pergunta
            )
        )

        self.botao_responder.pack(
            padx=25,
            pady=(15, 25)
        )

    def limpar_interface(self):

        for widget in self.winfo_children():
            widget.destroy()

    def enviar_resposta(self, pergunta):

        resposta = self.resposta_textbox.get(
            "1.0",
            "end"
        ).strip()

        if not resposta:
            self.mostrar_status(
                "Digite uma resposta antes de continuar."
            )
            return

        try:

            self.botao_responder.configure(
                state="disabled",
                text="Avaliando..."
            )

            self.update_idletasks()

            resultado = responder_pergunta(
                revisao_id=self.revisao_atual["id"],
                pergunta_id=pergunta["id"],
                resposta_aluno=resposta
            )

        except Exception as erro:

            try:
                self.botao_responder.configure(
                    state="normal",
                    text="Responder"
                )
            except Exception:
                pass

            self.mostrar_status(
                f"Erro ao avaliar resposta: {erro}"
            )

            return

        self.mostrar_avaliacao(
            resultado["avaliacao"]
        )

    def mostrar_avaliacao(self, avaliacao):

        campos_obrigatorios = [
            "classificacao",
            "pontuacao",
            "feedback",
            "pontos_corretos",
            "pontos_faltantes"
        ]

        for campo in campos_obrigatorios:

            if campo not in avaliacao:
                self.mostrar_erro_avaliacao(
                    f"A avaliação retornada pela IA não possui "
                    f"o campo obrigatório: {campo}"
                )
                return

        self.limpar_interface()

        titulo = ctk.CTkLabel(
            self,
            text="📋 Avaliação",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 20)
        )

        classificacao = avaliacao["classificacao"]

        if classificacao == "correta":

            texto_classificacao = "✅ Correta"

        elif classificacao == "parcial":

            texto_classificacao = "🟡 Parcial"

        else:

            texto_classificacao = "❌ Incorreta"

        resultado = ctk.CTkLabel(
            self,
            text=texto_classificacao,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        resultado.pack(
            pady=10
        )

        pontuacao = ctk.CTkLabel(
            self,
            text=f"{avaliacao['pontuacao']:.1f} / 10",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        pontuacao.pack(
            pady=10
        )

        feedback = ctk.CTkLabel(
            self,
            text=avaliacao["feedback"],
            font=ctk.CTkFont(
                size=16
            ),
            wraplength=750,
            justify="left"
        )

        feedback.pack(
            padx=30,
            pady=20
        )

        if avaliacao["pontos_corretos"]:

            corretos = ctk.CTkLabel(
                self,
                text=(
                    "Pontos corretos:\n• "
                    + "\n• ".join(
                        avaliacao["pontos_corretos"]
                    )
                ),
                justify="left",
                anchor="w",
                wraplength=750
            )

            corretos.pack(
                anchor="w",
                padx=50,
                pady=10
            )

        if avaliacao["pontos_faltantes"]:

            faltantes = ctk.CTkLabel(
                self,
                text=(
                    "Pontos a melhorar:\n• "
                    + "\n• ".join(
                        avaliacao["pontos_faltantes"]
                    )
                ),
                justify="left",
                anchor="w",
                wraplength=750
            )

            faltantes.pack(
                anchor="w",
                padx=50,
                pady=10
            )

        botao = ctk.CTkButton(
            self,
            text="Próxima pergunta",
            height=45,
            command=self.mostrar_pergunta
        )

        botao.pack(
            pady=30
        )

    def mostrar_erro_avaliacao(self, mensagem):

        self.limpar_interface()

        titulo = ctk.CTkLabel(
            self,
            text="⚠️ Erro na avaliação",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(80, 20)
        )

        texto = ctk.CTkLabel(
            self,
            text=mensagem,
            font=ctk.CTkFont(
                size=16
            ),
            wraplength=750,
            justify="center"
        )

        texto.pack(
            padx=30,
            pady=20
        )

        botao = ctk.CTkButton(
            self,
            text="Voltar para a pergunta",
            height=45,
            command=self.mostrar_pergunta
        )

        botao.pack(
            pady=30
        )

    def mostrar_resultado(self):

        self.limpar_interface()

        titulo = ctk.CTkLabel(
            self,
            text="🎉 Revisão concluída!",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(80, 20)
        )

        texto = ctk.CTkLabel(
            self,
            text=(
                "Todas as perguntas foram respondidas.\n\n"
                "A tela de resultados será implementada "
                "na próxima etapa."
            ),
            font=ctk.CTkFont(
                size=16
            ),
            justify="center"
        )

        texto.pack(
            pady=20
        )

    