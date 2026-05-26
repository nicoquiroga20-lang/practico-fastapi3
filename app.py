from fastapi import FastAPI, Path,Query , HTTPException
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()
app.title = 'Practico 3 Mi API'

STR_CORTITO = Annotated[str, Field(max_length=30)]
PRECIO_VALOR = Annotated[float, Field(lt=1000000)]
BOOL_ACTIVO = Annotated[bool, Field(description='Disponible?')]

class ArticuloSchema(BaseModel):
    id: Annotated[int, Field(gt=0,description='ID del articulo',deprecated=True)]
    categoria: STR_CORTITO
    marca: STR_CORTITO
    articulo: STR_CORTITO
    precio: PRECIO_VALOR
    activo: BOOL_ACTIVO = True

class ArticuloUpdateSchema(BaseModel):
    categoria: STR_CORTITO
    marca: STR_CORTITO
    articulo: STR_CORTITO
    precio: PRECIO_VALOR

not_found = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Artículo no encontrado",
                }
            }
        },
    },
}


articulos = [
    {'id': 1, 'categoria': 'componentes', 'marca':'HyperX', 'articulo':'Mouse', 'precio':80000, 'activo': True},
    {'id': 2, 'categoria': 'componentes', 'marca':'HyperX', 'articulo':'Teclado','precio':120000, 'activo': True},
    {'id': 3, 'categoria': 'componentes', 'marca':'HyperX', 'articulo':'Auriculares','precio':160000, 'activo': True},
    {'id': 4, 'categoria': 'componentes', 'marca':'HyperX', 'articulo':'Microfono','precio':95000, 'activo': True},
    {'id': 5, 'categoria': 'componentes', 'marca':'HyperX', 'articulo':'Mouse Pad','precio':82000, 'activo': True},
    {'id': 6, 'categoria': 'insumos', 'marca':'Artic', 'articulo':'Pasta Termica','precio':30000, 'activo': True},
    {'id': 7, 'categoria': 'insumos', 'marca':'Generic', 'articulo':'Alcohol Isopropilico','precio':17000, 'activo': True},
    {'id': 8, 'categoria': 'conectividad', 'marca':'UPC', 'articulo':'Estabilizador','precio':12000, 'activo': True},
    {'id': 9, 'categoria': 'conectividad', 'marca':'TP-Link', 'articulo':'Placa De Wi-FI','precio':67000, 'activo': True},
    {'id': 10, 'categoria': 'conectividad', 'marca':'TP-Link', 'articulo':'Dongle Bluethoot','precio':30000, 'activo': True}
]

@app.get('/articulos', response_model=list[ArticuloSchema])
async def get_articulo():
    return articulos

@app.get(
        '/articulos/{id}',
        responses = not_found,
        response_model=ArticuloSchema) #agregamos response_model para documentar la respuesta, responses para documentar los posibles errores
async def get_articulo_by_id(
    id: Annotated[int, Path(gt=0, description='ID del articulo')] #path para id | gt para validar que sea mayor a 0 | description para documentar el campo
):
    for articulo in articulos:
        if articulo['id'] == id:
            return articulo
    raise HTTPException(status_code=404, detail='Articulo no encontrado')




@app.post('/articulos', 
          response_model=list[ArticuloSchema]) #agregamos response_model para documentar la respuesta, responses para documentar los posibles errores
async def post_articulo(
    articulo_nuevo: ArticuloSchema
):
    articulos.append(articulo_nuevo.model_dump()) #model_dump para convertir el modelo a un diccionario, ya que articulos es una lista de diccionarios
    return articulos


@app.delete('/articulos/{id}',
            responses = not_found,
            response_model=list[ArticuloSchema]) # ¿Que implica documentar la respuesta de un delete? En este caso, se documenta que la respuesta es una lista de articulos, lo cual implica que se devuelve la lista de articulos actualizada luego de eliminar el articulo solicitado. Esto es importante para que el cliente sepa que esperar como respuesta y pueda manejarla correctamente.    
async def delete_articulo_by_id(
    id: Annotated[int, Path(gt=0, description='ID del articulo')],
    logico: Annotated[bool, Query(description='Eliminar registro?')] = False,
) -> list[ArticuloSchema]:
    for articulo in articulos:
        if articulo['id'] == id:
            if logico:
                articulo['activo'] = False
            else:
                articulos.remove(articulo)
            return articulos
    raise HTTPException(status_code=404, detail='Articulo no encontrado')

@app.put('/articulos/{id}',
         responses = not_found,
         response_model=ArticuloSchema) #agregamos response_model para documentar la respuesta, responses para documentar los posibles errores
async def put_articulo_by_id(
    id: Annotated[int, Path(gt=0, description='ID del articulo')],
    articulo_actualizado: ArticuloUpdateSchema
):
    for articulo in articulos:
        if articulo['id'] == id:
            articulo['categoria'] = articulo_actualizado.categoria
            articulo['marca'] = articulo_actualizado.marca
            articulo['articulo'] = articulo_actualizado.articulo
            articulo['precio'] = articulo_actualizado.precio
            articulo['activo'] = articulo.get('activo', True) #si el articulo no tiene el campo activo se asigna True por defecto
            return articulo
    raise HTTPException(status_code=404, detail='Articulo no encontrado')
