from src.juego.validador_apuesta import ValidadorApuesta


# Test constructor y rangos (cantidad y pinta, rework)
def test_pinta_mayor():
    pinta = 7
    cantidad = 3
    aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
    assert aceptado == False


def test_pinta_menor():
    pinta = 0
    cantidad = 3
    aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
    assert aceptado == False


def test_cantidad_menor():
    pinta = 3
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
    pinta_actual = 3
    cantidad_actual = 8

    pinta_nueva = 1
    cantidad_esperada = 5

    confirmado = ValidadorApuesta.cambio_to_ases(pinta_actual, cantidad_actual, pinta_nueva)
    assert confirmado == (cantidad_esperada, True)


def test_cambiar_a_ases_cantidad_impar():
    pinta_actual = 3
    cantidad_actual = 7

    pinta_nueva = 1
    cantidad_esperada = 4

    aceptado = ValidadorApuesta.cambio_to_ases(pinta_actual, cantidad_actual, pinta_nueva)
    assert aceptado == (cantidad_esperada, True)


def test_cambio_a_ases_pinta_distinto_a_1():
    pinta_actual = 3
    cantidad_actual = 8
    pinta_nueva = 2

    resultado = ValidadorApuesta.cambio_to_ases(pinta_actual, cantidad_actual, pinta_nueva)
    assert resultado == (8, False)


def test_cambiar_de_ases_cantidad_par():
    pinta_actual = 1
    cantidad_actual = 2

    pinta_nueva = 3
    cantidad_esperada = 5

    aceptado = ValidadorApuesta.cambio_de_ashes(pinta_actual, cantidad_actual, pinta_nueva)
    assert aceptado == (cantidad_esperada, True)


def test_cambiar_de_ases_cantidad_impar():
    pinta_actual = 1
    cantidad_actual = 3

    pinta_nueva = 3
    cantidad_esperada = 7

    aceptado = ValidadorApuesta.cambio_de_ashes(pinta_actual, cantidad_actual, pinta_nueva)
    assert aceptado == (cantidad_esperada, True)


def test_cambio_de_ases_pinta_distinto_a_1():
    pinta_actual = 2
    cantidad_actual = 5
    pinta_nueva = 3

    resultado = ValidadorApuesta.cambio_de_ashes(pinta_actual, cantidad_actual, pinta_nueva)
    assert resultado == (5, False)


# Test reglas basicas.
def test_no_partir_con_varios_as():
    pinta = 1
    cantidad = 3
    aceptado = ValidadorApuesta.validar_apuesta(pinta, cantidad)
    assert aceptado == False


def test_partir_solo_con_un_as():
    pinta = 1
    cantidad = 1
    aceptado = ValidadorApuesta.validar_apuesta(pinta, cantidad)
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


def test_disminucion_cantidad_misma_pinta_valido():
    pinta_actual = 3
    cantidad_actual = 2
    pinta_nueva = 3
    cantidad_nueva = 2
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_apuesta_invalida():
    pinta = 0
    cantidad = 0
    valido = ValidadorApuesta.validar_apuesta(pinta, cantidad)
    assert valido == False


def test_aumento_apuesta_distintas_cantidades():
    pinta_actual = 2
    cantidad_actual = 1
    pinta_nueva = 3
    cantidad_nueva = 1
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True
