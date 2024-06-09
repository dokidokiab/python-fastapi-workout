from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do Atleta", example="Maria", max_length=100)]
    cpf: Annotated[str, Field(description="CPF do Atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do Atleta", example=30)]
    altura: Annotated[PositiveFloat, Field(description="Altura do Atleta", example=1.79)]
    peso: Annotated[PositiveFloat, Field(description="Peso do Atleta", example=79.5)] #PositiveFloat só aceita Float positivo
    sexo: Annotated[str, Field(description="Sexo do Atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do Atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de Treinamento do Atleta")]

class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do Atleta", example="Maria", max_length=100)]
    idade: Annotated[Optional[int], Field(None, description="Idade do Atleta", example=30)]
    peso: Annotated[Optional[PositiveFloat], Field(None, description="Peso do Atleta", example=79.5)] #PositiveFloat só aceita Float positivo

class AtletaCustomized(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do Atleta", example="Maria", max_length=100)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do Atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de Treinamento do Atleta")]

