import customtkinter as ctk


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(2.0)
ctk.set_window_scaling(2.0)

class SACE(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SACE - Sistema Auxiliar de Controle de Estoque")
        self.geometry("900x600")
        self.minsize(900, 600)

        self.configure(fg_color="#F3F4F6")

        # Organização da janela
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#DEDEDE"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(7, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="SACE",
            font=("Arial", 26, "bold"),
            text_color="#1D4ED8"
        )
        self.logo.grid(row=0, column=0, padx=15, pady=(25, 5))

        self.subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Sistema Auxiliar de\nControle de Estoque",
            font=("Arial", 12),
            text_color="#374151"
        )
        self.subtitulo.grid(row=1, column=0, padx=10, pady=(0, 35))

        # Botões da sidebar
        botoes = [
            "Materiais",
            "Estoques",
            "Movimentações",
            "Relatórios",
            "Configurações"
        ]

        for indice, nome in enumerate(botoes):
            botao = ctk.CTkButton(
                self.sidebar,
                text=nome,
                height=45,
                font=("Arial", 15),
                fg_color="#2451BC",
                hover_color="#1D3F94",
                corner_radius=8
            )

            botao.grid(
                row=indice + 2,
                column=0,
                padx=15,
                pady=7,
                sticky="ew"
            )

        self.botao_sair = ctk.CTkButton(
            self.sidebar,
            text="Sair",
            height=45,
            font=("Arial", 15),
            fg_color="#2451BC",
            hover_color="#1D3F94",
            corner_radius=8
        )
        self.botao_sair.grid(
            row=8,
            column=0,
            padx=15,
            pady=20,
            sticky="ew"
        )

        self.conteudo = ctk.CTkFrame(
            self,
            fg_color="#F3F4F6",
            corner_radius=0
        )
        self.conteudo.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.titulo = ctk.CTkLabel(
            self.conteudo,
            text="Bem-vindo ao SACE",
            font=("Arial", 28, "bold"),
            text_color="#111827"
        )
        self.titulo.pack(
            anchor="w",
            padx=30,
            pady=(35, 5)
        )

        self.descricao = ctk.CTkLabel(
            self.conteudo,
            text="Sistema Auxiliar de Controle de Estoque",
            font=("Arial", 15),
            text_color="#6B7280"
        )
        self.descricao.pack(
            anchor="w",
            padx=30
        )

        # Painel principal
        self.painel = ctk.CTkFrame(
            self.conteudo,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#D1D5DB"
        )
        self.painel.pack(
            fill="x",
            padx=30,
            pady=30
        )

        self.texto_painel = ctk.CTkLabel(
            self.painel,
            text="Painel Principal",
            font=("Arial", 22, "bold"),
            text_color="#111827"
        )
        self.texto_painel.pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        self.info_painel = ctk.CTkLabel(
            self.painel,
            text="Selecione uma opção no menu lateral para começar.",
            font=("Arial", 14),
            text_color="#6B7280"
        )
        self.info_painel.pack(
            anchor="w",
            padx=25,
            pady=(0, 30)
        )


if __name__ == "__main__":
    app = SACE()
    app.mainloop()