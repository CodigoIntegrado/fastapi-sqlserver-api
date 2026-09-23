from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    codigo: str = Field(
        ...,
        min_length=1,
        max_length=20,
        examples=["1004"],
    )

    descricao: str = Field(
        ...,
        min_length=2,
        max_length=150,
        examples=["Webcam Full HD"],
    )

    preco: Decimal = Field(
        ...,
        ge=0,
        examples=[199.90],
    )

    estoque: int = Field(
        default=0,
        ge=0,
        examples=[15],
    )

    ativo: bool = True


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int
    criado_em: datetime