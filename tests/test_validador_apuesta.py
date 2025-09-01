#TEST DE CANTIDADES Y PINTAS
def test_pinta_mayor():
    pinta = 7
    cantidad = 3
    aceptado = ValidadorApuesta.VerificarRangoPinta(pinta)
    assert aceptado == False

def test_pinta_menor():
    pinta = 0
    cantidad = 3
    aceptado = ValidadorApuesta.VerificarRangoPinta(pinta)
    assert aceptado == False

def test_cantidad_menor():
    pinta = 3
    cantidad = -1
    aceptado = ValidadorApuesta.VerificarRangoCantidad(cantidad)
    assert aceptado == False