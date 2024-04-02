from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
 
app = FastAPI()
 
produtos = {
    1: {"nome": "Produto 1", "preco": 27.60},
    2: {"nome": "Produto 2", "preco": 48.70},
    3: {"nome": "Produto 3", "preco": 34.99},
    4: {"nome": "Produto 4", "preco": 45.50},
    5: {"nome": "Produto 5", "preco": 52.80}
}
 
class Pedido(BaseModel):
    cliente: str
    produtos: List[int]
 
pedidos = {
    1: {"cliente": "Cliente 1", "produtos": [1, 3]},
    2: {"cliente": "Cliente 2", "produtos": [2]}
}
 
@app.get('/pedidos', response_model=List[Pedido])
def get_orders():
    return pedidos
 
@app.post('/pedidos', response_model=Pedido)
def create_pedido(pedido: Pedido):
    pedidos[len(pedidos) + 1] = pedido.dict()
    return pedido
 
@app.get('/pedidos/{pedido_id}', response_model=Pedido)
def get_pedido(pedido_id: int):
    if pedido_id in pedidos:
        return pedidos[pedido_id]
    raise HTTPException(status_code=404, detail="Pedido não encontrado")
 
@app.put('/pedidos/{order_id}', response_model=Pedido)
def update_pedido(pedido_id: int, pedido: Pedido):
    if pedido_id in pedidos:
        pedidos[pedido_id] = pedido.dict()
        return pedidos[pedido_id]
    raise HTTPException(status_code=404, detail="Pedido não encontrado")
 
@app.delete("/pedidos/{pedido_id}")
async def delete_pedidos(pedido_id: int):
    if pedido_id in pedidos:
        del pedidos[pedido_id]
        return {"message": "Pedido excluído com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")