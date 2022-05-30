from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from tinydb import TinyDB, Query

from models import Obra, Biblioteca


app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Biblioteca')
spec.register(app)
database = TinyDB('../biblioteca.json')


@app.get('/obras')
@spec.validate(resp=Response(HTTP_200=Biblioteca))
def le_obras() -> Biblioteca:
    """Retorna todas as Obras da base de dados"""
    return jsonify(
        Biblioteca(
            biblioteca=database.all(),
            count=len(database.all())
        ).dict()
    )


@app.post('/obras')
@spec.validate(body=Request(Obra), resp=Response(HTTP_201=Obra))
def cria_obra() -> Obra:
    """Insere uma Obra no banco de dados."""
    body = request.context.body.dict()
    del body['id']
    database.insert(body)
    return body


@app.put('/obras/<int:id>')
@spec.validate(body=Request(Obra), resp=Response(HTTP_201=Obra))
def atualiza_obra(id: int) -> Obra:
    """Atualiza uma Obra no banco de dados."""
    obra = Query()
    body = request.context.body.dict()
    del body['id']
    database.update(body, obra.id == id)
    return jsonify(body)


@app.delete('/obras/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def remove_obra(id: int) -> None:
    """Remove uma Obra do banco de dados."""
    obra = Query()
    database.remove(obra.id == id)
    return jsonify({})


if __name__ == '__main__':
    app.run()
