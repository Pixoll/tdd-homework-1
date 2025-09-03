from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas


def test_cantidad_total_dados() -> None:
    cacho1 = Cacho()
    cacho2 = Cacho()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)
    assert arbitro.total_dados_en_juego == 10


def test_cantidad_total_dados_tras_remover() -> None:
    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.remover_dado()
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)
    assert arbitro.total_dados_en_juego == 9


# Test: duda correcta (apuesta menor que cantidad real)
def test_duda_correcta_gana_jugador(mocker: MockerFixture) -> None:
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


# Test: duda con ases como comodín
def test_duda_con_ases_como_comodin(mocker: MockerFixture) -> None:
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


# Test: duda sin ases, apuesta exacta
def test_duda_sin_ases_apuesta_exacta(mocker: MockerFixture) -> None:
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


# Test: duda con apuesta menor y ases presentes
def test_duda_con_ases_apuesta_menor(mocker: MockerFixture) -> None:
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
