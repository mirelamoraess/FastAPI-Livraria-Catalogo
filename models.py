from pydantic import BaseModel
from typing import Optional
 
class Produto(BaseModel):
    id: Optional[int] = None
    titulo: str
    autor: str
    genero: str
    publicacao: str
    preco: float
    preco: float