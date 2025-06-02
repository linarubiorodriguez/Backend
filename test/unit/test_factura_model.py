from flaskr.modelos import Factura
from datetime import datetime, timedelta

def test_factura_creation():
    factura = Factura(
        fecha_factura=datetime.utcnow(),
        total=100000.0,
        iva_total=16000.0,
        estado="Pendiente",
        fecha_vencimiento=datetime.utcnow() + timedelta(days=7),
        id_cliente=1
    )
    
    assert factura.total == 100000.0
    assert factura.iva_total == 16000.0
    assert factura.estado == "Pendiente"
    assert factura.id_cliente == 1