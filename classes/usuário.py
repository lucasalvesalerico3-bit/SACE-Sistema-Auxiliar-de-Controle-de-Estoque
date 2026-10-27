from datetime import datetime

class Usuario:
    def __init__(self, usuario, senha_hash, nome):
        self.usuario = usuario
        self.senha_hash = senha_hash
        self.nome = nome
        self.ativo =True
        self.cadastro = datetime.now()

    def ativar_usuario(self):
        self.ativo = True

    def desativar_usuario(self):
        self.ativo = False

    def verificar_status(self):
        if self.ativo:
            return "Ativo"
        else:
            return "Inativo"

    def __str__(self):
        return f"{self.nome} ({self.usuario})"