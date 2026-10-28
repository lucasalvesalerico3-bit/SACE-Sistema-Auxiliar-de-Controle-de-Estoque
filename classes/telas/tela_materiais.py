from queue import Empty, Queue
from threading import Thread
from tkinter import messagebox

import customtkinter as ctk
from mysql.connector import Error

from classes import cad_materiais
from classes.material import Material


class TelaMateriais(ctk.CTkScrollableFrame):
    AZUL = "#2451BC"
    AZUL_HOVER = "#1D3F94"

    def __init__(self, master):
        super().__init__(master, fg_color="#F3F4F6", corner_radius=0)
        self.id_em_edicao = None
        self.ocupado = False
        self.estoques = {}
        self.pesquisa_aplicada = ""
        self.controles = []
        self.botoes_linhas = []
        self.resultados = Queue()
        self.espera = None

        ctk.CTkLabel(
            self, text="Materiais", font=("Arial", 28, "bold"),
            text_color="#111827",
        ).pack(anchor="w", padx=20, pady=(24, 4))
        ctk.CTkLabel(
            self, text="Cadastro e consulta de materiais",
            font=("Arial", 15), text_color="#6B7280",
        ).pack(anchor="w", padx=20, pady=(0, 20))
        self._criar_pesquisa()
        self._criar_formulario()
        self._criar_lista()
        self.atualizar_lista()

    def _cartao(self):
        cartao = ctk.CTkFrame(
            self, fg_color="#FFFFFF", corner_radius=12,
            border_width=1, border_color="#D1D5DB",
        )
        cartao.pack(fill="x", padx=16, pady=(0, 16))
        return cartao

    def _botao(self, master, texto, comando, largura=140):
        botao = ctk.CTkButton(
            master, text=texto, command=comando, width=largura, height=34,
            font=("Arial", 13), fg_color=self.AZUL,
            hover_color=self.AZUL_HOVER, corner_radius=8,
        )
        self.controles.append(botao)
        return botao

    def _criar_pesquisa(self):
        cartao = self._cartao()
        cartao.grid_columnconfigure((0, 1), weight=1)
        self.pesquisa = ctk.CTkEntry(
            cartao, placeholder_text="Pesquisar material por nome ou código",
            height=36,
        )
        self.pesquisa.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 10))
        self.pesquisa.bind("<Return>", self.pesquisar)
        self.controles.append(self.pesquisa)
        self._botao(cartao, "Pesquisar", self.pesquisar).grid(
            row=1, column=0, sticky="w", padx=16, pady=(0, 16),
        )
        self._botao(cartao, "Limpar Pesquisa", self.limpar_pesquisa).grid(
            row=1, column=1, sticky="e", padx=16, pady=(0, 16),
        )

    def _criar_formulario(self):
        cartao = self._cartao()
        cartao.grid_columnconfigure((0, 1), weight=1, uniform="campos")
        self.titulo_formulario = ctk.CTkLabel(
            cartao, text="Cadastrar material", font=("Arial", 20, "bold"),
            text_color="#111827",
        )
        self.titulo_formulario.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 4))
        self.aviso_formulario = ctk.CTkLabel(
            cartao, text="* Campos obrigatórios. O saldo inicial será 0.",
            text_color="#6B7280", font=("Arial", 12), anchor="w",
        )
        self.aviso_formulario.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 8))

        for texto, linha, coluna in (
            ("Código *", 2, 0), ("Nome *", 2, 1),
            ("Estoque *", 4, 0), ("Estoque mínimo *", 4, 1),
            ("Descrição (opcional)", 6, 0),
        ):
            ctk.CTkLabel(cartao, text=texto, text_color="#374151").grid(
                row=linha, column=coluna, sticky="w", padx=16,
            )
        self.codigo = ctk.CTkEntry(cartao, height=34)
        self.nome = ctk.CTkEntry(cartao, height=34)
        self.estoque = ctk.CTkComboBox(cartao, values=["Selecione um estoque"], state="readonly", height=34)
        self.estoque.set("Selecione um estoque")
        self.minimo = ctk.CTkEntry(cartao, height=34)
        self.minimo.insert(0, "0")
        for widget, linha, coluna in (
            (self.codigo, 3, 0), (self.nome, 3, 1),
            (self.estoque, 5, 0), (self.minimo, 5, 1),
        ):
            widget.grid(row=linha, column=coluna, sticky="ew", padx=16, pady=(0, 8))
            self.controles.append(widget)
        self.descricao = ctk.CTkTextbox(cartao, height=70, border_width=1, border_color="#D1D5DB")
        self.descricao.grid(row=7, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))
        self.controles.append(self.descricao)
        self.botao_salvar = self._botao(cartao, "Cadastrar Material", self.salvar, 190)
        self.botao_salvar.grid(row=8, column=0, sticky="w", padx=16, pady=(0, 16))
        self.botao_limpar = self._botao(cartao, "Limpar Campos", self.limpar_formulario)
        self.botao_limpar.grid(row=8, column=1, sticky="e", padx=16, pady=(0, 16))

    def _criar_lista(self):
        cartao = self._cartao()
        cartao.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            cartao, text="Materiais cadastrados", font=("Arial", 20, "bold"),
            text_color="#111827",
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))
        self._botao(cartao, "Atualizar Lista", self.atualizar_lista).grid(
            row=0, column=1, sticky="e", padx=16, pady=(16, 8),
        )
        self.status = ctk.CTkLabel(cartao, text="", anchor="w", text_color="#6B7280", width=1, wraplength=550)
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 8))
        # A lista acompanha a rolagem da página, sem duas barras verticais aninhadas.
        self.tabela = ctk.CTkFrame(cartao, fg_color="white", corner_radius=0)
        self.tabela.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 16))
        self._cabecalho()

    def _cabecalho(self):
        colunas = (
            ("Código", 60), ("Nome", 110), ("Estoque", 82), ("Saldo", 42),
            ("Estoque\nmínimo", 65), ("Situação", 57), ("Ações", 90),
        )
        for coluna, (titulo, largura) in enumerate(colunas):
            self.tabela.grid_columnconfigure(coluna, minsize=largura, weight=1 if coluna in (1, 2) else 0)
            ctk.CTkLabel(
                self.tabela, text=titulo, font=("Arial", 12, "bold"),
                fg_color="#EFF3FA", text_color="#374151", height=42, width=1,
            ).grid(row=0, column=coluna, sticky="nsew", padx=2, pady=(0, 4))

    def _exibir_materiais(self, materiais):
        for widget in self.tabela.winfo_children():
            widget.destroy()
        self.botoes_linhas.clear()
        self._cabecalho()
        if not materiais:
            texto = "Nenhum material encontrado." if self.pesquisa_aplicada else "Nenhum material cadastrado."
            ctk.CTkLabel(self.tabela, text=texto, text_color="#6B7280").grid(
                row=1, column=0, columnspan=7, pady=24,
            )
        for linha, material in enumerate(materiais, start=1):
            ativo = bool(material["ativo"])
            fundo = "#F9FAFB" if linha % 2 else "#FFFFFF"
            valores = (
                material["codigo"], material["nome"], material["nome_estoque"] or "Não encontrado",
                material["saldo_estoque"], material["estoque_minimo"], "Ativo" if ativo else "Inativo",
            )
            for coluna, valor in enumerate(valores):
                cor = "#166534" if ativo else "#6B7280"
                label = ctk.CTkLabel(
                    self.tabela, text=str(valor), width=1, height=76,
                    font=("Arial", 12), fg_color=fundo,
                    text_color=cor if coluna == 5 else "#374151",
                    anchor="w" if coluna < 3 else "center",
                    wraplength=(54, 104, 76, 36, 59, 51)[coluna],
                )
                label.grid(row=linha, column=coluna, sticky="nsew", padx=2, pady=2)
            acoes = ctk.CTkFrame(self.tabela, fg_color=fundo, corner_radius=0)
            acoes.grid(row=linha, column=6, sticky="nsew", padx=2, pady=2)
            for texto, comando in (
                ("Editar", lambda m=material: self.editar(m["id_material"])),
                ("Desativar" if ativo else "Reativar", lambda m=material: self.alterar_situacao(m)),
            ):
                botao = ctk.CTkButton(
                    acoes, text=texto, width=82, height=28, font=("Arial", 12),
                    fg_color=self.AZUL, hover_color=self.AZUL_HOVER, command=comando,
                )
                botao.pack(padx=2, pady=4)
                self.botoes_linhas.append(botao)

    def _habilitar_controles(self):
        for widget in self.controles + self.botoes_linhas:
            widget.configure(state="disabled" if self.ocupado else "normal")
        if not self.ocupado:
            self.estoque.configure(state="readonly" if self.estoques else "disabled")
            if not self.estoques:
                self.botao_salvar.configure(state="disabled")

    def _executar(self, tarefa, ao_concluir, mensagem):
        if self.ocupado:
            return
        self.ocupado = True
        self._habilitar_controles()
        self.status.configure(text=mensagem, text_color="#6B7280")

        def trabalhar():
            try:
                self.resultados.put((True, tarefa()))
            except Exception as erro:
                self.resultados.put((False, erro))

        # Só a thread principal acessa os widgets; a thread de trabalho usa o MySQL.
        Thread(target=trabalhar, daemon=True).start()
        self.espera = self.after(80, lambda: self._aguardar(ao_concluir))

    def _aguardar(self, ao_concluir):
        self.espera = None
        try:
            sucesso, resultado = self.resultados.get_nowait()
        except Empty:
            self.espera = self.after(80, lambda: self._aguardar(ao_concluir))
            return
        self.ocupado = False
        self._habilitar_controles()
        if sucesso:
            self.status.configure(text="")
            ao_concluir(resultado)
        else:
            mensagem = self._mensagem_erro(resultado)
            self.status.configure(text="Operação não concluída. " + mensagem, text_color="#B91C1C")
            messagebox.showerror("Materiais", mensagem, parent=self)

    @staticmethod
    def _mensagem_erro(erro):
        if isinstance(erro, ValueError):
            return str(erro)
        if isinstance(erro, Error):
            if erro.errno == 1062:
                return "Já existe um material com esse código. Informe outro código."
            if erro.errno == 1452:
                return "O estoque selecionado não existe mais. Atualize a lista."
            if erro.errno in (1406, 1264):
                return "Um dos valores ultrapassa o limite permitido pelo banco. Revise os campos."
        return "Não foi possível concluir a operação. Verifique a conexão com o banco e tente novamente."

    def atualizar_lista(self, mensagem_sucesso=""):
        if self.ocupado:
            return
        pesquisa = self.pesquisa_aplicada

        def carregar():
            return cad_materiais.listar_estoques(), cad_materiais.listar_materiais(pesquisa)

        def exibir(resultado):
            estoques, materiais = resultado
            selecionado = self.estoques.get(self.estoque.get())
            self.estoques = {
                f'{e["nome"]} (#{e["id_estoque"]})' + (" — Inativo" if not e["ativo"] else ""): e["id_estoque"]
                for e in estoques
            }
            # CTkComboBox.set não altera o texto enquanto o campo está disabled.
            self.estoque.configure(
                values=list(self.estoques) or ["Nenhum estoque disponível"], state="readonly"
            )
            self.estoque.set(next(
                (nome for nome, identificador in self.estoques.items() if identificador == selecionado),
                "Selecione um estoque" if self.estoques else "Nenhum estoque disponível",
            ))
            self._exibir_materiais(materiais)
            resumo = f"{len(materiais)} material(is) listado(s)."
            if pesquisa:
                resumo += f' Pesquisa: "{pesquisa}".'
            if not estoques:
                resumo += " Cadastre um estoque antes de cadastrar materiais."
            self.status.configure(text=f"{mensagem_sucesso} {resumo}".strip(), text_color="#6B7280")
            self._habilitar_controles()

        self._executar(carregar, exibir, "Carregando materiais e estoques…")

    def pesquisar(self, event=None):
        if not self.ocupado:
            self.pesquisa_aplicada = self.pesquisa.get().strip()
            self.atualizar_lista()
        return "break"

    def limpar_pesquisa(self):
        if not self.ocupado:
            self.pesquisa.delete(0, "end")
            self.pesquisa_aplicada = ""
            self.atualizar_lista()

    def limpar_formulario(self):
        if self.ocupado:
            return
        self.id_em_edicao = None
        for campo in (self.codigo, self.nome, self.minimo):
            campo.delete(0, "end")
        self.minimo.insert(0, "0")
        self.descricao.delete("1.0", "end")
        self.estoque.set("Selecione um estoque" if self.estoques else "Nenhum estoque disponível")
        self.titulo_formulario.configure(text="Cadastrar material")
        self.aviso_formulario.configure(text="* Campos obrigatórios. O saldo inicial será 0.")
        self.botao_salvar.configure(text="Cadastrar Material")
        self.botao_limpar.configure(text="Limpar Campos")

    def salvar(self):
        if self.ocupado:
            return
        try:
            minimo = self.minimo.get().strip()
            if not minimo or not minimo.isascii() or not minimo.isdecimal():
                raise ValueError("O estoque mínimo deve ser um número inteiro maior ou igual a zero.")
            material = Material(
                self.codigo.get(), self.nome.get(), self.descricao.get("1.0", "end-1c"),
                self.estoques.get(self.estoque.get()), int(minimo),
            )
        except ValueError as erro:
            messagebox.showwarning("Revise os campos", str(erro), parent=self)
            return
        id_material = self.id_em_edicao

        def gravar():
            if id_material is None:
                return cad_materiais.cadastrar_material(material)
            return cad_materiais.atualizar_material(id_material, material)

        def concluir(_):
            self.limpar_formulario()
            mensagem = "Material cadastrado com sucesso!" if id_material is None else "Alterações salvas com sucesso!"
            messagebox.showinfo("Materiais", mensagem, parent=self)
            self.atualizar_lista(mensagem)

        self._executar(gravar, concluir, "Salvando material…")

    def editar(self, id_material):
        def preencher(material):
            self.limpar_formulario()
            self.id_em_edicao = material["id_material"]
            self.codigo.insert(0, material["codigo"])
            self.nome.insert(0, material["nome"])
            self.minimo.delete(0, "end")
            self.minimo.insert(0, str(material["estoque_minimo"]))
            self.descricao.insert("1.0", material["descricao"] or "")
            self.estoque.set(next(
                (nome for nome, identificador in self.estoques.items() if identificador == material["id_estoque"]),
                "Selecione um estoque",
            ))
            self.titulo_formulario.configure(text="Editar material")
            situacao = "Ativo" if material["ativo"] else "Inativo"
            self.aviso_formulario.configure(text=f'Saldo atual: {material["saldo_estoque"]} (somente leitura). Situação: {situacao}.')
            self.botao_salvar.configure(text="Salvar Alterações")
            self.botao_limpar.configure(text="Cancelar Edição")
            self._parent_canvas.yview_moveto(0)
            self.codigo.focus_set()

        self._executar(lambda: cad_materiais.obter_material(id_material), preencher, "Carregando material…")

    def alterar_situacao(self, material):
        if self.ocupado:
            return
        novo_ativo = not bool(material["ativo"])
        if not novo_ativo and not messagebox.askyesno(
            "Desativar material",
            f'Desativar o material {material["codigo"]} — {material["nome"]}?\nO histórico será preservado.',
            parent=self,
        ):
            return

        def concluir(_):
            if self.id_em_edicao == material["id_material"]:
                self.limpar_formulario()
            mensagem = "Material reativado com sucesso!" if novo_ativo else "Material desativado com sucesso!"
            messagebox.showinfo("Materiais", mensagem, parent=self)
            self.atualizar_lista(mensagem)

        self._executar(
            lambda: cad_materiais.definir_material_ativo(material["id_material"], novo_ativo),
            concluir, "Atualizando situação…",
        )

    def destroy(self):
        if self.espera is not None:
            self.after_cancel(self.espera)
        super().destroy()
