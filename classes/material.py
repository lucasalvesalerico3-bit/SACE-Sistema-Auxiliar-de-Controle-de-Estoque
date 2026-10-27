class Material:
    def __init__(self, codigo, nome, descricao, estoque, estoque_minimo=0):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.estoque = estoque
        self.estoque_minimo = estoque_minimo
        self.saldo_estoque = 0
        self.ativo = True

    def ativar_material(self):
        self.ativo = True

    def desativar_material(self):
        self.ativo = False

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
