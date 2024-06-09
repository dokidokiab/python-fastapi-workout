from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoAtleta(BaseSchema):
    nome : Annotated[str, Field(description="Nome do Centro de Treinamento", example="CT Queen", max_length=50)]

class CentroTreinamentoIn(BaseSchema):
    nome : Annotated[str, Field(description="Nome do Centro de Treinamento", example="CT Queen", max_length=50)]
    endereco : Annotated[str, Field(description="Endereço do Centro de Treinamento", example="Rua Y, N 888", max_length=60)]
    proprietario : Annotated[str, Field(description="Proprietário do Centro de Treinamento", example="Joana", max_length=30)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="Identificador do Centro de Treinamento")]