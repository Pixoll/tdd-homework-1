from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas
from src.juego.dado import Dado


# Test: duda correcta (apuesta menor que cantidad real)
def test_duda_correcta_gana_jugador():
    cacho = Cacho([Dado(2), Dado(2), Dado(3), Dado(4), Dado(5)])
    contador = ContadorPintas(cacho)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    # 2 de pinta 2 + 0 As como comodín > 1, jugador que duda pierde
    assert resultado == "jugador_pierde"


# Test: duda exacta (calzar)
def test_duda_correcta_calzar():
    cacho = Cacho([Dado(2), Dado(2), Dado(1), Dado(3), Dado(4)])
    contador = ContadorPintas(cacho)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 3  # 2 de pinta 2 + 1 As como comodín
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == "calzar"


# Test: duda con ases como comodín
def test_duda_con_ases_como_comodin():
    cacho = Cacho([Dado(1), Dado(1), Dado(3), Dado(4), Dado(5)])
    contador = ContadorPintas(cacho)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 3
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    # 1 de pinta 3 + 2 ases (comodín máximo) = 3 > 2, jugador que duda pierde
    assert resultado == "jugador_pierde"


# Test: duda sin ases, apuesta exacta
def test_duda_sin_ases_apuesta_exacta():
    cacho = Cacho([Dado(2), Dado(2), Dado(3), Dado(4), Dado(5)])
    contador = ContadorPintas(cacho)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == "calzar"


# Test: duda con apuesta menor y ases presentes
def test_duda_con_ases_apuesta_menor():
    cacho = Cacho([Dado(1), Dado(2), Dado(2), Dado(3), Dado(4)])
    contador = ContadorPintas(cacho)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    # 2 de pinta 2 + 1 As como comodín = 3 > 1, jugador que duda pierde
    assert resultado == "jugador_pierde"


def test_duda_con_ases_apuesta_mayor():
    cacho = Cacho([Dado(3), Dado(2), Dado(2), Dado(3), Dado(4)])
    contador = ContadorPintas(cacho)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 3
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == "jugador_gana"
