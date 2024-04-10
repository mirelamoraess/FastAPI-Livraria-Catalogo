from fastapi import FastAPI, HTTPException, status, Response
from models import Produto
import requests
import json

app = FastAPI()

proxies = {
   'http': 'http://127.0.0.1:8080',
   'https': 'http://127.0.0.1:8080',
}

# Busca por produto pelo ID
buscaProduto = {
    1:'FQVDDwAAQBAJ',
    2:'I__4CQAAQBAJ',
    3:'xxLmDwAAQBAJ',
    4:'YfT3EAAAQBAJ',
    5:'6RQ-AQAAQBAJ'
}

# Catálogo de Produtos
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

# Pedidos
pedidos = {
    1: {"cliente": "Cliente 1", "produtos": [1]},
    2: {"cliente": "Cliente 2", "produtos": [2]},
    3: {"cliente": "Cliente 2", "produtos": [3]},
    4: {"cliente": "Cliente 2", "produtos": [4]},
    5: {"cliente": "Cliente 2", "produtos": [5]},
    
}

# Consumindo api de outro computador
@app.get('/produtos_pedidos')
async def get_produtos_pedidos():

    request = requests.get("http://10.234.88.90:8000/pedidos", proxies=proxies)

    print(request.content)
    produtos = json.loads(request.content)
    print(produtos)
    d4  = {}
    for chave in produtos.keys():
        d1 = produtos[chave]
        d2 = pedidos[int(chave)]
        d3 = dict(d1, **d2)
        d4[chave] = d3
    return d4

# Consumindo api online
@app.get('/apilink/{produto_id}')
async def get_produtos_id(produto_id):
    try:
        produto_id = int(produto_id)
        produto = produtos[produto_id]
        produto.update({"id": produto_id})
       
        url = f'https://play.google.com/store/books/details?id={buscaProduto[produto_id]}'
 
        print(url)
       
        res = requests.get(url, proxies=proxies)
 
        data = res.json()
        data_link = data["link"]
        link  = {"link para seus livros no Google Books:": data_link}
        return produto, link
    except KeyError:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='livro não encontrado.')
    except  ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="So aceito inteiros....")

# Rotas GET servirão para recuperar os dados
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

# Rotas POST servirão para enviar dados   
@app.post("/produtos")
async def get_produto(produto: Produto):
    if produto.id not in produtos:
        next_id = len(produtos) + 1
        produtos[next_id] = produto
        return produto
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um produto com o ID")

# Rotas PUT servirá para atualização
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
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)