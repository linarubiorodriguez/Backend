from flaskr.modelos import Animal

def test_animal_creation():
    animal = Animal(
        nombre="Perro",
        imagen="perro.jpg",
        estado="Activo"
    )
    assert animal.nombre == "Perro"
    assert animal.imagen == "perro.jpg"
    assert animal.estado == "Activo"