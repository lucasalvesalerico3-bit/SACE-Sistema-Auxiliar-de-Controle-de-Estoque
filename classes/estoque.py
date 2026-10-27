
class Estoque:
    def __init__(self, identificador, nome):
        self.identificador = identificador
        self.nome = nome

    def __str__(self):
        return f"{self.identificador} - {self.nome}"
