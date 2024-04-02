from fastapi import FastAPI, HTTPException, status, Response
from models import Produto

app = FastAPI()

produtos = {
    1: {
        "titulo": "A princesa salva a si mesma neste livro",
        "autor": 'Amanda Lovelace',
        "genero": 'Poesia', 
        "publicacao": 2016,
        "preco": 27.60
    },
    
    2: {
        "titulo": "A Rainha Vermelha",
        "autor": 'Victoria Aveyard',
        "genero": 'Distopia', 
        "publicacao": 2015,
        "preco": 48.70
    },
    3: {
        "titulo": "Coraline",
        "autor": 'Neil Gaiman',
        "genero": 'Fantasia',
        "publicacao": 2002,
        "preco": 34.99
    },
    4: {
        "titulo": "The Amityville Horror",
        "autor": 'Jay Anson',
        "genero": 'Terror', 
        "publicacao": 1977,
        "preco": 45.50
    },    
    5: {
        "titulo": "Divina Comédia",
        "autor": 'Dante Alighier',
        "genero": 'Filosofia', 
        "publicacao": 1314,
        "preco": 52.80
    }
}

@app.get('/produtos')
async def get_produtos():
    return produtos

@app.get('/produtos/{produto_id}')
async def get_produto(produto_id):
    try:
        produto_id = int(produto_id)
        produto = produtos[produto_id]
        produto.update({"id": produto_id})
        return produto
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='O valor deve ser inteiro')
    
@app.post("/produtos")
async def get_produto(produto: Produto):
    if produto.id not in produtos:
        next_id = len(produtos) + 1
        produtos[next_id] = produto
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um produto com o ID")

@app.put('/produtos/{produto_id}')
async def get_produto(produto_id: int, produto: Produto):
    if produto_id in produtos:
        produto [produto_id]= produto
        produto.id = produto_id
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado')
    
@app.delete('/produtos/{produto_id}')
async def delete_produto(produto_id: int):
    if produto_id in produtos:
        del produtos[produto_id]
        return{'message': 'Produto excluído com sucesso!'}
    else:
        return{"error": "Produto não encontrado!"}
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)