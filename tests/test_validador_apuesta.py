from src.validador_apuesta import ValidadorApuesta


def test_pinta_mayor() -> None:
    """Verifica que una pinta mayor a 6 no es válida."""
    pinta = 7
    aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
    assert aceptado == False


def test_pinta_menor() -> None:
    """Verifica que una pinta menor a 1 no es válida."""
    pinta = 0
    aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
    assert aceptado == False


def test_cantidad_menor() -> None:
    """Verifica que cantidades menores a 1 no son válidas."""
    cantidad = -1
    aceptado = ValidadorApuesta.verificar_rango_cantidad(cantidad)
    assert aceptado == False


def test_pinta_valida() -> None:
    """Verifica que las pintas de 1 a 6 son válidas."""
    for pinta in range(1, 7):  # Pintas válidas: 1-6
        aceptado = ValidadorApuesta.verificar_rango_pinta(pinta)
        assert aceptado == True


def test_cantidad_valida() -> None:
    """Verifica que cantidades válidas >=1 son aceptadas."""
    for cantidad in [1, 5, 10, 100]:  # Cantidades válidas
        aceptado = ValidadorApuesta.verificar_rango_cantidad(cantidad)
        assert aceptado == True


def test_constructor() -> None:
    """Verifica que el constructor asigna correctamente pinta y cantidad."""
    validador = ValidadorApuesta(pinta=3, cantidad=5)
    assert validador.pinta == 3
    assert validador.cantidad == 5


def test_cambiar_a_ases_cantidad_par() -> None:
    """Verifica el cálculo al cambiar a ases con cantidad par."""
    cantidad_actual = 8
    cantidad_esperada = 5
    valor = ValidadorApuesta.cambio_a_ases(cantidad_actual)
    assert valor == cantidad_esperada


def test_cambiar_a_ases_cantidad_impar() -> None:
    """Verifica el cálculo al cambiar a ases con cantidad impar."""
    cantidad_actual = 7
    cantidad_esperada = 4
    valor = ValidadorApuesta.cambio_a_ases(cantidad_actual)
    assert valor == cantidad_esperada


def test_cambiar_de_ases_cantidad_par() -> None:
    """Verifica el cálculo al cambiar desde ases con cantidad par."""
    cantidad_actual = 2
    cantidad_esperada = 5
    aceptado = ValidadorApuesta.cambio_desde_ases(cantidad_actual)
    assert aceptado == cantidad_esperada


def test_cambiar_de_ases_cantidad_impar() -> None:
    """Verifica el cálculo al cambiar desde ases con cantidad impar."""
    cantidad_actual = 3
    cantidad_esperada = 7
    aceptado = ValidadorApuesta.cambio_desde_ases(cantidad_actual)
    assert aceptado == cantidad_esperada


def test_no_partir_con_varios_as() -> None:
    """Verifica que no se puede iniciar con varios ases si el jugador no tiene un dado."""
    pinta = 1
    cantidad = 3
    aceptado = ValidadorApuesta.validar_primera_apuesta(pinta, cantidad, jugador_tiene_un_dado=False)
    assert aceptado == False


def test_partir_solo_con_un_as() -> None:
    """Verifica que se puede iniciar con un as si el jugador solo tiene un dado."""
    pinta = 1
    cantidad = 1
    aceptado = ValidadorApuesta.validar_primera_apuesta(pinta, cantidad, jugador_tiene_un_dado=True)
    assert aceptado == True


def test_aumento_misma_pinta_valido() -> None:
    """Verifica que aumentar la cantidad de la misma pinta es válido."""
    pinta_actual = 3
    cantidad_actual = 2
    pinta_nueva = 3
    cantidad_nueva = 4

    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_disminucion_misma_pinta_invalido() -> None:
    """Verifica que disminuir la cantidad de la misma pinta no es válido."""
    pinta_actual = 3
    cantidad_actual = 4
    pinta_nueva = 3
    cantidad_nueva = 2

    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == False


def test_aumento_cantidad_misma_pinta_valido() -> None:
    """Verifica que aumentar cantidad mantiene validez para la misma pinta."""
    pinta_actual = 3
    cantidad_actual = 2
    pinta_nueva = 3
    cantidad_nueva = 5
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_cambio_especial_a_ases() -> None:
    """Verifica el aumento especial cuando se cambia a ases."""
    pinta_actual = 2
    pinta_nueva = 1
    cantidad_actual = 3
    cantidad_nueva = 2
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_cambio_especial_desde_ases() -> None:
    """Verifica el aumento especial cuando se cambia desde ases."""
    pinta_actual = 1
    pinta_nueva = 2
    cantidad_actual = 2
    cantidad_nueva = 5
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True


def test_apuesta_invalida() -> None:
    """Verifica que una apuesta con pinta y cantidad inválidas no es válida."""
    pinta = 0
    cantidad = 0
    valido = ValidadorApuesta.validar_apuesta_general(pinta, cantidad)
    assert valido == False


def test_aumento_apuesta_distintas_cantidades() -> None:
    """Verifica que cambiar a otra pinta con cantidad mayor o igual es válido."""
    pinta_actual = 2
    cantidad_actual = 1
    pinta_nueva = 3
    cantidad_nueva = 1
    valido = ValidadorApuesta.validar_aumento_apuesta(pinta_actual, cantidad_actual, pinta_nueva, cantidad_nueva)
    assert valido == True
