class Material:
    def __init__(self, codigo, nome, descricao, estoque, estoque_minimo=0):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.estoque = estoque
        self.estoque_minimo = estoque_minimo
        self.saldo_estoque = 0
        self.ativo = True
        self.validar()

    def validar(self):
        self.codigo = self.codigo.strip()
        self.nome = self.nome.strip()
        self.descricao = (self.descricao or "").strip()

        if not self.codigo or not self.nome:
            raise ValueError("Código e nome são obrigatórios.")
        if len(self.codigo) > 50 or len(self.nome) > 50:
            raise ValueError("Código e nome devem ter no máximo 50 caracteres.")
        if len(self.descricao) > 255:
            raise ValueError("A descrição deve ter no máximo 255 caracteres.")
        if type(self.estoque) is not int or self.estoque <= 0:
            raise ValueError("Selecione um estoque existente.")
        if (type(self.estoque_minimo) is not int
                or not 0 <= self.estoque_minimo <= 2147483647):
            raise ValueError(
                "O estoque mínimo deve ser um número inteiro entre 0 e 2147483647."
            )

    def ativar_material(self):
        self.ativo = True

    def desativar_material(self):
        self.ativo = False

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
