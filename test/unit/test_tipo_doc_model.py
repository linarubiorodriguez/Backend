from flaskr.modelos import TipoDoc

def test_tipo_doc_creation():
    tipo_doc = TipoDoc(
        Nombre="CP",
        Descripcion="Cédula de prueba"
    )
    assert tipo_doc.Nombre == "CP"
    assert tipo_doc.Descripcion == "Cédula de prueba"