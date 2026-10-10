from datetime import datetime

class Usuario:
    def init(self, usuario, senha_hash, nome):
        self.usuario = usuario
        self.senha_hash = senha_hash
        self.nome = nome
        self.ativo =True
        self.cadastro = datetime.now()

    def ativar_usuario(self):
        self.ativo = False

    def desativar_usuario(self):
        self.ativo = False

    def str(self):
        return f"{self.nome} ({self.usuario})"