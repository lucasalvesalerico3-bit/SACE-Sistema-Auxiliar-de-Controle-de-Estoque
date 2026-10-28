from contextlib import contextmanager, redirect_stdout
from io import StringIO

from mysql.connector import Error

from classes.teste_banco import conectar


@contextmanager
def _cursor(escrita=False):
    # A conexão legada imprime erros de acesso. Não exponha esses detalhes na UI/log.
    with redirect_stdout(StringIO()):
        conexao = conectar()
    if conexao is None:
        raise Error("Não foi possível conectar ao banco de dados.")

    cursor = None
    try:
        cursor = conexao.cursor(dictionary=True)
        yield cursor
        if escrita:
            conexao.commit()
    except Exception:
        if escrita:
            conexao.rollback()
        raise
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conexao.close()


def listar_estoques():
    with _cursor() as cursor:
        cursor.execute("SELECT id_estoque, nome, ativo FROM estoques ORDER BY nome")
        return cursor.fetchall()


_SELECAO_MATERIAIS = """
    SELECT m.id_material, m.codigo, m.nome, m.descricao, m.id_estoque,
           e.nome AS nome_estoque, m.saldo_estoque, m.estoque_minimo, m.ativo
    FROM materiais AS m
    LEFT JOIN estoques AS e ON e.id_estoque = m.id_estoque
"""


def listar_materiais(pesquisa=""):
    # Trate % e _ digitados como texto, não como curingas do LIKE.
    termo = pesquisa.strip().replace("!", "!!").replace("%", "!%").replace("_", "!_")
    padrao = f"%{termo}%"
    with _cursor() as cursor:
        cursor.execute(
            _SELECAO_MATERIAIS + """
            WHERE LOWER(m.nome) LIKE LOWER(%s) ESCAPE '!'
               OR LOWER(m.codigo) LIKE LOWER(%s) ESCAPE '!'
            ORDER BY m.nome, m.codigo, m.id_material
            """,
            (padrao, padrao),
        )
        return cursor.fetchall()


def obter_material(id_material):
    with _cursor() as cursor:
        cursor.execute(
            _SELECAO_MATERIAIS + " WHERE m.id_material = %s", (id_material,)
        )
        material = cursor.fetchone()
        if material is None:
            raise ValueError("Material não encontrado. Atualize a lista.")
        return material


def _verificar_estoque(cursor, id_estoque):
    cursor.execute("SELECT id_estoque FROM estoques WHERE id_estoque = %s", (id_estoque,))
    if cursor.fetchone() is None:
        raise ValueError("O estoque selecionado não existe mais. Atualize a lista.")


def _verificar_material(cursor, id_material):
    cursor.execute(
        "SELECT id_material FROM materiais WHERE id_material = %s FOR UPDATE",
        (id_material,),
    )
    if cursor.fetchone() is None:
        raise ValueError("Material não encontrado. Atualize a lista.")


def cadastrar_material(material):
    material.validar()
    with _cursor(escrita=True) as cursor:
        _verificar_estoque(cursor, material.estoque)
        # Saldo e situação iniciais são definidos aqui, nunca pelo formulário.
        # O índice UNIQUE impede códigos duplicados, inclusive concorrentes.
        cursor.execute(
            """
            INSERT INTO materiais
            (codigo, nome, descricao, id_estoque, estoque_minimo, saldo_estoque, ativo)
            VALUES (%s, %s, %s, %s, %s, 0, 1)
            """,
            (material.codigo, material.nome, material.descricao,
             material.estoque, material.estoque_minimo),
        )
        return cursor.lastrowid


def atualizar_material(id_material, material):
    material.validar()
    with _cursor(escrita=True) as cursor:
        _verificar_material(cursor, id_material)
        _verificar_estoque(cursor, material.estoque)
        cursor.execute(
            """
            UPDATE materiais
            SET codigo = %s, nome = %s, descricao = %s,
                id_estoque = %s, estoque_minimo = %s
            WHERE id_material = %s
            """,
            (material.codigo, material.nome, material.descricao,
             material.estoque, material.estoque_minimo, id_material),
        )


def definir_material_ativo(id_material, ativo):
    with _cursor(escrita=True) as cursor:
        _verificar_material(cursor, id_material)
        cursor.execute(
            "UPDATE materiais SET ativo = %s WHERE id_material = %s",
            (int(bool(ativo)), id_material),
        )


def cadastrar_estoque(nome, descricao):
    with _cursor(escrita=True) as cursor:
        cursor.execute(
            "INSERT INTO estoques (nome, descricao, ativo) VALUES (%s, %s, %s)",
            (nome, descricao, 1),
        )
        return cursor.lastrowid
