from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaCustomized, AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post(
        '/', 
        summary="Criar um atleta",
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut
        )

async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn=Body(...)):
    
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    if not categoria:
               raise HTTPException(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       detail=f'A Categoria {atleta_in.categoria.nome} não foi encontrada.')
    

    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    if not centro_treinamento:
               raise HTTPException(
                       status_code=status.HTTP_400_BAD_REQUEST,
                       detail=f'O Centro de Treinamento {atleta_in.centro_treinamento.nome} não foi encontrado.')
        
    cpf = (await db_session.execute(select(AtletaModel).filter_by(nome=atleta_in.cpf))).scalars().first()
    if cpf:
        raise IntegrityError(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f'Já existe um atleta cadastrado com o cpf: {cpf}')


    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except Exception:
        raise HTTPException(
                       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                       detail='Ocorreu um erro ao inserir os dados no banco')
        
    return atleta_out


@router.get(
        '/', 
        summary="Consultar todos os atletas",
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaCustomized],
        
        )

async def query(
    db_session: DatabaseDependency, limit: int = 100, offset: int = 0
    ) -> list[AtletaCustomized]:
        atletas : list[AtletaCustomized] = (await db_session.execute(select(AtletaModel).limit(limit).offset(offset))).scalars().all()
        
        return [AtletaCustomized.model_validate(atleta) for atleta in atletas]



@router.get(
        '/{id}', 
        summary="Consultar um Atleta pelo id",
        status_code=status.HTTP_200_OK,
        response_model= AtletaOut,
        
        )

async def get(id: UUID4,
    db_session: DatabaseDependency,
    limit: int = 100, 
    offset: int = 0
    ) -> AtletaOut:
        atleta : AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
                                    ).scalars().first()

        if not atleta:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id {id}')
        
        return atleta

@router.get(
        '/{id}', 
        summary="Consultar um Atleta pelo id",
        status_code=status.HTTP_200_OK,
        response_model= AtletaOut,
        
        )

async def get(id: UUID4,
    db_session: DatabaseDependency,
    ) -> AtletaOut:
        atleta : AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
                                    ).scalars().first()

        if not atleta:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id {id}')
        
        return atleta

@router.get(
        '/cpf/{cpf}', 
        summary="Consultar um Atleta pelo cpf",
        status_code=status.HTTP_200_OK,
        response_model= AtletaOut,
        
        )

async def get(cpf: str,
    db_session: DatabaseDependency,
    ) -> AtletaOut:
        atleta : AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))
                                    ).scalars().first()

        if not atleta:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no cpf {cpf}')
        
        return atleta


@router.get(
        '/nome/{nome}', 
        summary="Consultar um Atleta pelo nome",
        status_code=status.HTTP_200_OK,
        response_model= AtletaOut,
        
        )

async def get(nome: str,
    db_session: DatabaseDependency,
    ) -> AtletaOut:
        atleta : AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(nome=nome))
                                    ).scalars().first()

        if not atleta:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado pelo nome {nome}')
        
        return atleta

@router.patch(
        '/{id}', 
        summary="Editar um Atleta pelo id",
        status_code=status.HTTP_200_OK,
        response_model= AtletaOut,
        
        )

async def query(id: UUID4,
    db_session: DatabaseDependency,
    atleta_up:AtletaUpdate=Body(...)
    ) -> AtletaOut:
        
        atleta : AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
                                    ).scalars().first()

        if not atleta:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id {id}')
        
        atleta_update = atleta_up.model_dump(exclude_unset=True)
        for key, value in atleta_update.items():
               setattr(atleta, key, value)

        await db_session.commit()
        await db_session.update(atleta)
               
        return atleta


@router.delete(
        '/{id}', 
        summary="Deletar um Atleta pelo id",
        status_code=status.HTTP_204_NO_CONTENT,
        )

async def get(id: UUID4,
    db_session: DatabaseDependency,
    ) -> None:
        atleta : AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
                                    ).scalars().first()

        if not atleta:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id {id}')
       
        await db_session.delete(atleta)
        await db_session.commit()