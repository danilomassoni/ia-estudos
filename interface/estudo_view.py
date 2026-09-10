import customtkinter as ctk

from services.estudo_service import registrar_estudo


class EstudoView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.criar_interface()

    def criar_interface(self):

        # ==============================
        # CONFIGURAÇÃO
        # ==============================

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

        titulo = ctk.CTkLabel(
            self,
            text="📚 Registrar estudo",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 20)
        )

        # ==============================
        # FORMULÁRIO
        # ==============================

        formulario = ctk.CTkScrollableFrame(
            self
        )

        formulario.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        formulario.grid_columnconfigure(
            0,
            weight=1
        )

        # ==============================
        # ASSUNTO
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="Assunto",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.entry_assunto = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: Java, Python, Machine Learning..."
        )

        self.entry_assunto.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==============================
        # TÓPICO
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="Tópico",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.entry_topico = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: Streams, Pandas, Redes Neurais..."
        )

        self.entry_topico.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==============================
        # CONTEÚDO
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="O que você estudou?",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.text_conteudo = ctk.CTkTextbox(
            formulario,
            height=120
        )

        self.text_conteudo.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==============================
        # DURAÇÃO
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="Quanto tempo você estudou?",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.entry_duracao = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 90"
        )

        self.entry_duracao.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==============================
        # COMPREENSÃO
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="Como você avalia sua compreensão?",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.compreensao = ctk.CTkComboBox(
            formulario,
            values=[
                "1 - Não entendi",
                "2 - Entendi pouco",
                "3 - Entendi parcialmente",
                "4 - Entendi bem",
                "5 - Consigo explicar para outra pessoa"
            ]
        )

        self.compreensao.set(
            "3 - Entendi parcialmente"
        )

        self.compreensao.pack(
            fill="x",
            pady=(0, 15)
        )

        # ==============================
        # DIFICULDADES
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="Quais foram suas dificuldades?",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.text_dificuldades = ctk.CTkTextbox(
            formulario,
            height=80
        )

        self.text_dificuldades.pack(
            fill="x",
            pady=(0, 5)
        )

        ctk.CTkLabel(
            formulario,
            text="Ex.: Tive dificuldade para entender o reduce.",
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # ==============================
        # APRENDIZADOS
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="O que você aprendeu?",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.text_aprendizados = ctk.CTkTextbox(
            formulario,
            height=80
        )

        self.text_aprendizados.pack(
            fill="x",
            pady=(0, 5)
        )

        ctk.CTkLabel(
            formulario,
            text="Ex.: Entendi como map e filter funcionam.",
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # ==============================
        # PRÓXIMO PASSO
        # ==============================

        ctk.CTkLabel(
            formulario,
            text="Qual deve ser seu próximo passo?",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        self.text_proximo_passo = ctk.CTkTextbox(
            formulario,
            height=80
        )

        self.text_proximo_passo.pack(
            fill="x",
            pady=(0, 20)
        )

        # ==============================
        # BOTÃO
        # ==============================

        self.botao_salvar = ctk.CTkButton(
            formulario,
            text="💾 Salvar estudo",
            height=45,
            command=self.salvar_estudo
        )

        self.botao_salvar.pack(
            fill="x",
            pady=(0, 20)
        )

        # ==============================
        # MENSAGEM
        # ==============================

        self.label_status = ctk.CTkLabel(
            formulario,
            text=""
        )

        self.label_status.pack(
            pady=(0, 20)
        )

    # ==============================
    # SALVAR
    # ==============================

    def salvar_estudo(self):

        try:

            assunto = self.entry_assunto.get().strip()

            topico = self.entry_topico.get().strip()

            conteudo = self.text_conteudo.get(
                "1.0",
                "end"
            ).strip()

            duracao_texto = (
                self.entry_duracao.get().strip()
            )

            compreensao_texto = (
                self.compreensao.get()
            )

            dificuldades = (
                self.text_dificuldades
                .get("1.0", "end")
                .strip()
            )

            aprendizados = (
                self.text_aprendizados
                .get("1.0", "end")
                .strip()
            )

            proximo_passo = (
                self.text_proximo_passo
                .get("1.0", "end")
                .strip()
            )

            # ==============================
            # CONVERSÃO
            # ==============================

            duracao_minutos = int(
                duracao_texto
            )

            compreensao = int(
                compreensao_texto[0]
            )

            # ==============================
            # REGISTRAR
            # ==============================

            estudo = registrar_estudo(
                assunto=assunto,
                topico=topico,
                conteudo=conteudo,
                duracao_minutos=duracao_minutos,
                compreensao=compreensao,
                dificuldades=(
                    [dificuldades]
                    if dificuldades
                    else []
                ),
                aprendizados=(
                    [aprendizados]
                    if aprendizados
                    else []
                ),
                proximo_passo=(
                    proximo_passo
                    if proximo_passo
                    else None
                )
            )

            # ==============================
            # SUCESSO
            # ==============================

            self.label_status.configure(
                text=(
                    f"✅ Estudo salvo com sucesso! "
                    f"{estudo['data']} às "
                    f"{estudo['hora_inicio']}"
                )
            )

            self.limpar_formulario()

        except ValueError as erro:

            self.label_status.configure(
                text=f"⚠️ {erro}"
            )

        except Exception as erro:

            self.label_status.configure(
                text=f"❌ Erro ao salvar: {erro}"
            )

    # ==============================
    # LIMPAR FORMULÁRIO
    # ==============================

    def limpar_formulario(self):

        self.entry_assunto.delete(
            0,
            "end"
        )

        self.entry_topico.delete(
            0,
            "end"
        )

        self.text_conteudo.delete(
            "1.0",
            "end"
        )

        self.entry_duracao.delete(
            0,
            "end"
        )

        self.compreensao.set(
            "3 - Entendi parcialmente"
        )

        self.text_dificuldades.delete(
            "1.0",
            "end"
        )

        self.text_aprendizados.delete(
            "1.0",
            "end"
        )

        self.text_proximo_passo.delete(
            "1.0",
            "end"
        )