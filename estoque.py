# Classe

class Estoque:
    # Lista de simulação do DB
    estoques = []

    def __init__(self, id_estoque:int, nome:str='Sem nome', descricao:str='Sem descrição'):
        # Atributos instância
        self.__id_estoque = id_estoque
        self._nome = None
        self._descricao = None

        # Validação
        self.nome = nome
        self.descricao = descricao

    # getters e setters
    #nome
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome:str=''):
        if novo_nome.strip() != '':
            self._nome = novo_nome
    #descrição
    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, nova_descricao:str=''):
        if nova_descricao.strip() != '':
            self._descricao = nova_descricao
    #id do estoque
    @property
    def id_estoque(self):
        return self.__id_estoque

    @id_estoque.setter
    def id_estoque(self, id_estoque:int):
        raise PermissionError('Não é possível mudar o id do estoque.')

    # Métodos
    def cadastrar(self): # Cadastro e Gerenciamento
        for estoque in Estoque.estoques:
            if estoque.id_estoque == self.id_estoque:
                raise ValueError('Já existe um estoque com esse ID')
        Estoque.estoques.append(self)

    def atualizar(self, novo_nome:str, nova_descricao:str):
        self.nome = novo_nome
        self.descricao = nova_descricao

    def excluir(self):
        if self in Estoque.estoques:
            Estoque.estoques.remove(self)
            return True
        return False

    @classmethod # Listando estoques
    def listar(cls) -> list:
        return cls.estoques

    @classmethod # Buscar por estoque
    def buscar_por_id(cls, id_estoque:int):
        for estoque in cls.estoques:
            if estoque.id_estoque == id_estoque:
                return estoque
        return None

    def lista_materiais(self): # Lista de materais
        pass
