from classes.teste_banco import conectar
from mysql.connector import Error


def cadastrar_material(material):
    conexao = conectar()

    if conexao is None:
        raise Error("Não foi possível conectar ao banco de dados.")

    cursor = None

    sql = """
        INSERT INTO materiais
        (codigo, nome, descricao, id_estoque, estoque_minimo, saldo_estoque, ativo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        material.codigo,
        material.nome,
        material.descricao,
        material.estoque,
        material.estoque_minimo,
        material.saldo_estoque,
        material.ativo
    )

    try:
        cursor = conexao.cursor()
        cursor.execute(sql, valores)
        conexao.commit()
        print("Material cadastrado com sucesso!")

    except Error as erro:
        conexao.rollback()
        print(f"Erro ao cadastrar material: {erro}")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()


def cadastrar_estoque(nome, descricao):
    conexao = conectar()

    if conexao is None:
        raise Error("Não foi possível conectar ao banco de dados.")

    cursor = None

    sql = """
        INSERT INTO estoques (nome, descricao, ativo)
        VALUES (%s, %s, %s)
    """

    valores = (nome, descricao, 1)

    try:
        cursor = conexao.cursor()
        cursor.execute(sql, valores)
        conexao.commit()
        print("Estoque cadastrado com sucesso!")

    except Error as erro:
        conexao.rollback()
        print(f"Erro ao cadastrar estoque: {erro}")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()
