from src.juego.validador_apuesta import ValidadorApuesta


# Test constructor y rangos (cantidad y pinta, rework)
def test_pinta_mayor():
    pinta = 7
    aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
    assert aceptado == False


def test_pinta_menor():
    pinta = 0
    aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
    assert aceptado == False


def test_cantidad_menor():
    cantidad = -1
    aceptado = ValidadorApuesta.verificar_rango_cantidad(cantidad)
    assert aceptado == False


def test_pinta_valida():
    for pinta in range(1, 7):  # Pintas válidas: 1-6
        aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
        assert aceptado == True


def test_cantidad_valida():
    for cantidad in [1, 5, 10, 100]:  # Cantidades válidas
        aceptado = ValidadorApuesta.verificar_rango_cantidad(cantidad)
        assert aceptado == True


def test_constructor():
    validador = ValidadorApuesta(pinta=3, cantidad=5)
    assert validador.pinta == 3
    assert validador.cantidad == 5


# Test regla de los Ases
def test_cambiar_a_ases_cantidad_par():
    cantidad_actual = 8
    cantidad_esperada = 5
    valor = ValidadorApuesta.cambio_a_ases(cantidad_actual)
    assert valor == cantidad_esperada


def test_cambiar_a_ases_cantidad_impar():
    cantidad_actual = 7
    cantidad_esperada = 4
    valor = ValidadorApuesta.cambio_a_ases(cantidad_actual)
    assert valor == cantidad_esperada


def test_cambiar_de_ases_cantidad_par():
    cantidad_actual = 2
    cantidad_esperada = 5
    aceptado = ValidadorApuesta.cambio_desde_ases(cantidad_actual)
    assert aceptado == cantidad_esperada


def test_cambiar_de_ases_cantidad_impar():
    cantidad_actual = 3
    cantidad_esperada = 7
    aceptado = ValidadorApuesta.cambio_desde_ases(cantidad_actual)
    assert aceptado == cantidad_esperada


# Test reglas basicas.
def test_no_partir_con_varios_as():
    pinta = 1
    cantidad = 3
    aceptado = ValidadorApuesta.validar_primera_apuesta(pinta, cantidad, jugador_tiene_un_dado=False)
    assert aceptado == False


def test_partir_solo_con_un_as():
    pinta = 1
    cantidad = 1
    aceptado = ValidadorApuesta.validar_primera_apuesta(pinta, cantidad, jugador_tiene_un_dado=True)
    assert aceptado == True


def test_aumento_misma_pinta_valido():
    pinta_actual = 3
    cantidad_actual = 2
    pinta_nueva = 3
    cantidad_nueva = 4

    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_disminucion_misma_pinta_invalido():
    pinta_actual = 3
    cantidad_actual = 4
    pinta_nueva = 3
    cantidad_nueva = 2

    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == False


def test_aumento_cantidad_misma_pinta_valido():
    pinta_actual = 3
    cantidad_actual = 2
    pinta_nueva = 3
    cantidad_nueva = 5
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_cambio_especial_a_ases():
    pinta_actual = 2
    pinta_nueva = 1
    cantidad_actual = 3
    cantidad_nueva = 2
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_cambio_especial_desde_ases():
    pinta_actual = 1
    pinta_nueva = 2
    cantidad_actual = 2
    cantidad_nueva = 5
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_apuesta_invalida():
    pinta = 0
    cantidad = 0
    valido = ValidadorApuesta.validar_apuesta_general(pinta, cantidad)
    assert valido == False


def test_aumento_apuesta_distintas_cantidades():
    pinta_actual = 2
    cantidad_actual = 1
    pinta_nueva = 3
    cantidad_nueva = 1
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True
