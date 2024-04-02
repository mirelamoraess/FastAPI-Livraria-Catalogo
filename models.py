from pydantic import BaseModel
from typing import Optional
 
class Produto(BaseModel):
    id: Optional[int] = None
    titulo: str
    autor: str
    genero: str
    publicacao: str
    preco: float
 
class Pedidos(BaseModel):
    id: int
    products: List[str]
    status: str
 
class UpdateStatus(BaseModel):
    status: str