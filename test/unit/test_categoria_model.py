from flaskr.modelos import Categoria

def test_categoria_creation():
    categoria = Categoria(
        nombre="Juguetes",
        descripcion="Juguetes para mascotas",
        imagen="https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743612220/m5tiluc3fpyujvap7hnx.jpg"
    )
    assert categoria.nombre == "Juguetes"
    assert categoria.descripcion == "Juguetes para mascotas"
    assert categoria.imagen == "https://res.cloudinary.com/dvzzqjlbj/image/upload/v1743612220/m5tiluc3fpyujvap7hnx.jpg"