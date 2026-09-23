import logging

import pyodbc
from fastapi import APIRouter, HTTPException, Response, status

from app.database import get_connection
from app.models import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoUpdate,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)


def row_to_produto(row):
    return {
        "id": row.id,
        "codigo": row.codigo,
        "descricao": row.descricao,
        "preco": row.preco,
        "estoque": row.estoque,
        "ativo": bool(row.ativo),
        "criado_em": row.criado_em,
    }


@router.get(
    "",
    response_model=list[ProdutoResponse],
)
def listar_produtos():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                codigo,
                descricao,
                preco,
                estoque,
                ativo,
                criado_em
            FROM dbo.produto
            ORDER BY id
            """
        )

        produtos = [
            row_to_produto(row)
            for row in cursor.fetchall()
        ]

        return produtos

    except pyodbc.Error:
        logger.exception("Erro ao listar produtos")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao consultar produtos.",
        )

    finally:
        if connection:
            connection.close()


@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse,
)
def buscar_produto(produto_id: int):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                codigo,
                descricao,
                preco,
                estoque,
                ativo,
                criado_em
            FROM dbo.produto
            WHERE id = ?
            """,
            produto_id,
        )

        produto = cursor.fetchone()

        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado.",
            )

        return row_to_produto(produto)

    except HTTPException:
        raise

    except pyodbc.Error:
        logger.exception("Erro ao buscar produto")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao consultar produto.",
        )

    finally:
        if connection:
            connection.close()


@router.post(
    "",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_produto(produto: ProdutoCreate):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM dbo.produto
            WHERE codigo = ?
            """,
            produto.codigo,
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Já existe um produto com este código.",
            )

        cursor.execute(
            """
            INSERT INTO dbo.produto
            (
                codigo,
                descricao,
                preco,
                estoque,
                ativo
            )
            OUTPUT
                INSERTED.id,
                INSERTED.codigo,
                INSERTED.descricao,
                INSERTED.preco,
                INSERTED.estoque,
                INSERTED.ativo,
                INSERTED.criado_em
            VALUES (?, ?, ?, ?, ?)
            """,
            produto.codigo,
            produto.descricao,
            produto.preco,
            produto.estoque,
            produto.ativo,
        )

        novo_produto = cursor.fetchone()

        connection.commit()

        return row_to_produto(novo_produto)

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except pyodbc.Error:
        if connection:
            connection.rollback()

        logger.exception("Erro ao criar produto")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao criar produto.",
        )

    finally:
        if connection:
            connection.close()


@router.put(
    "/{produto_id}",
    response_model=ProdutoResponse,
)
def atualizar_produto(
    produto_id: int,
    produto: ProdutoUpdate,
):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM dbo.produto
            WHERE id = ?
            """,
            produto_id,
        )

        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado.",
            )

        cursor.execute(
            """
            SELECT id
            FROM dbo.produto
            WHERE codigo = ?
              AND id <> ?
            """,
            produto.codigo,
            produto_id,
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Já existe outro produto com este código.",
            )

        cursor.execute(
            """
            UPDATE dbo.produto
            SET
                codigo = ?,
                descricao = ?,
                preco = ?,
                estoque = ?,
                ativo = ?
            OUTPUT
                INSERTED.id,
                INSERTED.codigo,
                INSERTED.descricao,
                INSERTED.preco,
                INSERTED.estoque,
                INSERTED.ativo,
                INSERTED.criado_em
            WHERE id = ?
            """,
            produto.codigo,
            produto.descricao,
            produto.preco,
            produto.estoque,
            produto.ativo,
            produto_id,
        )

        produto_atualizado = cursor.fetchone()

        connection.commit()

        return row_to_produto(produto_atualizado)

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except pyodbc.Error:
        if connection:
            connection.rollback()

        logger.exception("Erro ao atualizar produto")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao atualizar produto.",
        )

    finally:
        if connection:
            connection.close()


@router.delete(
    "/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_produto(produto_id: int):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM dbo.produto
            WHERE id = ?
            """,
            produto_id,
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado.",
            )

        connection.commit()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except HTTPException:
        if connection:
            connection.rollback()
        raise

    except pyodbc.Error:
        if connection:
            connection.rollback()

        logger.exception("Erro ao excluir produto")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao excluir produto.",
        )

    finally:
        if connection:
            connection.close()