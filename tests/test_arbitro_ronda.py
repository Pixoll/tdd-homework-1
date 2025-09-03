from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas


def test_cantidad_total_dados() -> None:
    """Verifica que al iniciar dos cachos haya 10 dados en juego."""
    cacho1 = Cacho()
    cacho2 = Cacho()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)
    assert arbitro.total_dados_en_juego == 10


def test_cantidad_total_dados_tras_remover() -> None:
    """Verifica que al remover un dado se reduzca el total en juego."""
    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.remover_dado()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)
    assert arbitro.total_dados_en_juego == 9


def test_duda_correcta_gana_jugador(mocker: MockerFixture) -> None:
    """Dudar falla cuando la apuesta es menor que la cantidad real."""
    mock_valores_cacho1 = [2, 2, 3, 4, 5]
    mock_valores_cacho2 = [3, 3, 4, 5, 6]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta, usar_ases=True)
    assert resultado == False


def test_duda_con_ases_como_comodin(mocker: MockerFixture) -> None:
    """Dudar considera ases como comodines cuando usar_ases=True."""
    mock_valores_cacho1 = [1, 1, 3, 4, 5]
    mock_valores_cacho2 = [2, 2, 4, 5, 6]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 3
    resultado = arbitro.dudar(cantidad_apostada, pinta, usar_ases=True)
    assert resultado == False


def test_duda_sin_ases_apuesta_exacta(mocker: MockerFixture) -> None:
    """Dudar falla cuando la apuesta coincide exactamente sin ases."""
    mock_valores_cacho1 = [2, 2, 3, 4, 5]
    mock_valores_cacho2 = [3, 3, 4, 5, 6]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta, usar_ases=False)
    assert resultado == False


def test_duda_con_ases_apuesta_menor(mocker: MockerFixture) -> None:
    """Dudar falla cuando la apuesta es menor y hay ases de comodín."""
    mock_valores_cacho1 = [1, 2, 2, 3, 4]
    mock_valores_cacho2 = [2, 3, 3, 4, 5]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta, usar_ases=True)
    assert resultado == False


def test_duda_con_ases_apuesta_mayor(mocker: MockerFixture) -> None:
    """Dudar resulta verdadero si la apuesta excede la cantidad real."""
    mock_valores_cacho1 = [3, 2, 2, 3, 4]
    mock_valores_cacho2 = [4, 3, 3, 4, 5]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 3
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta, usar_ases=True)
    assert resultado == True


def test_si_puede_calzar(mocker: MockerFixture) -> None:
    """Verifica que se pueda calzar cuando la apuesta es suficiente."""
    mock_valores_cacho1 = [1, 2, 2, 2, 2]
    mock_valores_cacho2 = [2, 3, 3, 3, 3]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 5
    dados_jugador = 5
    puede_calzar = arbitro.puede_calzar(cantidad_apostada, dados_jugador)
    assert puede_calzar == True


def test_no_puede_calzar(mocker: MockerFixture) -> None:
    """Verifica que no se pueda calzar cuando la apuesta es insuficiente."""
    mock_valores_cacho1 = [1, 2, 2, 2, 2]
    mock_valores_cacho2 = [2, 3, 3, 3, 3]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 4
    dados_jugador = 5
    puede_calzar = arbitro.puede_calzar(cantidad_apostada, dados_jugador)
    assert puede_calzar == False


def test_calzar_correcto_sin_ases(mocker: MockerFixture) -> None:
    """Calzar es correcto cuando la cantidad coincide sin ases."""
    mock_valores_cacho1 = [1, 2, 2, 2, 2]
    mock_valores_cacho2 = [2, 3, 3, 3, 3]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 5
    pinta = 2
    resultado = arbitro.calzar(cantidad_apostada, pinta, usar_ases=False)
    assert resultado == True


def test_calzar_correcto_con_ases(mocker: MockerFixture) -> None:
    """Calzar es correcto cuando la cantidad coincide usando ases."""
    mock_valores_cacho1 = [1, 2, 2, 2, 2]
    mock_valores_cacho2 = [2, 3, 3, 3, 3]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 6
    pinta = 2
    resultado = arbitro.calzar(cantidad_apostada, pinta, usar_ases=True)
    assert resultado == True


def test_calzar_incorrecto_sin_ases(mocker: MockerFixture) -> None:
    """Calzar falla cuando la cantidad no coincide sin ases."""
    mock_valores_cacho1 = [1, 2, 2, 2, 2]
    mock_valores_cacho2 = [2, 3, 3, 3, 3]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 5
    pinta = 3
    resultado = arbitro.calzar(cantidad_apostada, pinta, usar_ases=False)
    assert resultado == False


def test_calzar_incorrecto_con_ases(mocker: MockerFixture) -> None:
    """Calzar falla cuando la cantidad no coincide aun con ases."""
    mock_valores_cacho1 = [1, 2, 2, 2, 2]
    mock_valores_cacho2 = [2, 3, 3, 3, 3]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 4
    pinta = 3
    resultado = arbitro.calzar(cantidad_apostada, pinta, usar_ases=True)
    assert resultado == False
