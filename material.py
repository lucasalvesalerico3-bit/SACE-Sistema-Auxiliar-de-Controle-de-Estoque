# Classe

class Material:
    # List de simulação do DB
    materiais = []

    # Atributos de instância
    def __init__(self, id_material:int, codigo:str, saldo_atual:int, id_estoque:int, descricao:str='Sem descrição',  estoque_minimo:int=1, nome:str='Sem nome',):
        self.__id_material = id_material
        self.__codigo = codigo
        self.__id_estoque = id_estoque
        self._saldo_atual = None
        self._descricao = None
        self._estoque_minimo = None
        self._nome = None

        # Validação
        self.saldo_atual = saldo_atual
        self.descricao = descricao
        self.estoque_minimo = estoque_minimo
        self.nome = nome

    # Getters e Setters
    @property # Id do material
    def id_material(self):
        return self.__id_material

    @id_material.setter
    def id_material(self, id_material:int):
        raise PermissionError('Não é possível mudar o id do material.')

    @property # Código
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo:str):
        raise PermissionError('Não é possível mudar o código do material.')

    @property # Saldo atual
    def saldo_atual(self):
        return self._saldo_atual

    @saldo_atual.setter
    def saldo_atual(self, quantidade:int=0):
        if quantidade >= 0:
            self._saldo_atual = quantidade
        else:
            raise ValueError('Valor informado é inválido.')

    @property # Id do estoque
    def id_estoque(self):
        return self.__id_estoque

    @id_estoque.setter
    def id_estoque(self, id_estoque:int):
        raise PermissionError('Não é possível mudar o id do estoque em que este material pertence.')

    @property # Descrição
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, nova_descricao:str=''):
        if nova_descricao.strip() != '':
            self._descricao = nova_descricao
        else:
            raise ValueError('Nova descrição informada é inválida.')

    @property # Estoque mínimo
    def estoque_minimo(self):
        return self._estoque_minimo

    @estoque_minimo.setter
    def estoque_minimo(self, valor:int):
        if valor > 0:
            self._estoque_minimo = valor
        else:
            raise ValueError('Valor informado é inválido.')

    @property # Nome do material
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome:str=''):
        if novo_nome.strip() != '':
            self._nome = novo_nome
        else:
            raise ValueError('Novo nome informado é inválido.')

    # Métodos
    def cadastrar(self): # Cadastro e Gerenciamento
        for material in Material.materiais:
            if material.id_material == self.id_material:
                raise ValueError('Já existe um material com esse ID.')
            if material.codigo == self.codigo:
                raise ValueError('Já existe um material com esse código.')
        Material.materiais.append(self)

    def atualizar(self, novo_nome:str, nova_descricao:str):
        self.nome = novo_nome
        self.descricao = nova_descricao

    def excluir(self):
        if self in Material.materiais:
            Material.materiais.remove(self)
            return True
        return False

    # Consultas
    @classmethod
    def listar(cls) -> list:
        return cls.materiais

    @classmethod
    def buscar_por_id(cls, id_material:int):
        for material in cls.materiais:
            if material.id_material == id_material:
                return material
        return None

    @classmethod
    def buscar_por_codigo(cls, codigo:int):
        for material in cls.materiais:
            if material.codigo == codigo:
                return material
        return None

    def verificar_estoque_minimo(self):
        if self.saldo_atual <= self.estoque_minimo:
            return True
        return False
