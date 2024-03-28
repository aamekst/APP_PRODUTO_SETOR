from typing import List
from fastapi import APIRouter, Response, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import engine,SessionLocal, get_db
from db.models import Usuarios as UsuariosModel
from schemas.usuario import Usuarios as UsuariosSchema
from schemas.usuario import Usuarios, UsuarioRequest, UsuarioResponse
from repository.usuario import UsuarioRepository

from db.base import Base


#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/usuarios")



@router.post("/addComSchema", status_code=status.HTTP_201_CREATED, description='Adicionar user')
def add_user(request:UsuariosSchema, db: Session = Depends(get_db)):
        # usuario_on_db = UsuariosModel(id=request.id, item=request.item, peso=request.peso, numero_caixas=request.numero_caixas)
        user_on_db_ = UsuariosModel(**request.dict())
        db.add(user_on_db_)
        db.commit()
        db.refresh(user_on_db_)
        return user_on_db_

@router.get("/usuario/listar")
async def get_tarefas(db: Session = Depends(get_db)):
    usuarios= db.query(UsuariosModel).all()
    return usuarios


@router.get("/procurar_por_id/{id}", response_model=UsuarioResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    usuarios = UsuarioRepository.find_by_id(db, id)
    if not usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado"
        )
    return UsuarioResponse.from_orm(usuarios)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not UsuarioRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    UsuarioRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{id}", response_model=UsuarioResponse)
def update(id: int, request: UsuarioRequest, db: Session = Depends(get_db)):
    if not UsuarioRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    usuario = UsuarioRepository.save(db, UsuariosModel(id=id, **request.dict()))
    return UsuarioResponse.from_orm(usuario)