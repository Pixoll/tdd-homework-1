from src.juego.validador_apuesta import ValidadorApuesta

#Test constructor y rangos(cantidad y pinta, rework)
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

def test_pinta_valida():
    for pinta in range(1, 7):  # Pintas válidas: 1-6
        aceptado = ValidadorApuesta.VerificarRangoPinta(pinta)
        assert aceptado == True

def test_cantidad_valida():
    for cantidad in [1, 5, 10, 100]:  # Cantidades válidas
        aceptado = ValidadorApuesta.VerificarRangoCantidad(cantidad)
        assert aceptado == True

def test_constructor():
    validador = ValidadorApuesta(pinta=3, cantidad=5)
    assert validador.pinta == 3
    assert validador.cantidad == 5