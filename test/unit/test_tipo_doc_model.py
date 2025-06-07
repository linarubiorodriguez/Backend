from flaskr.modelos import TipoDoc

def test_tipo_doc_creation():
    tipo_doc = TipoDoc(
        nombre="CP",
        descripcion="Cédula de prueba"
    )
    assert tipo_doc.nombre == "CP"
    assert tipo_doc.descripcion == "Cédula de prueba"