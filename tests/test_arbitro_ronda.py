from src.juego.arbitro_ronda import ArbitroRonda, ResultadoDuda
from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas
from src.juego.dado import Dado


# Test: duda correcta (apuesta menor que cantidad real)
def test_duda_correcta_gana_jugador():
    cacho1 = Cacho([Dado(2), Dado(2), Dado(3), Dado(4), Dado(5)])
    cacho2 = Cacho([Dado(3), Dado(3), Dado(4), Dado(5), Dado(6)])
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == ResultadoDuda.PIERDE


# Test: duda exacta (calzar)
def test_duda_correcta_calzar():
    cacho1 = Cacho([Dado(2), Dado(2), Dado(1), Dado(3), Dado(4)])
    cacho2 = Cacho([Dado(3), Dado(3), Dado(2), Dado(4), Dado(5)])
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 4
    pinta = 3
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == ResultadoDuda.CALZAR


# Test: duda con ases como comodín
def test_duda_con_ases_como_comodin():
    cacho1 = Cacho([Dado(1), Dado(1), Dado(3), Dado(4), Dado(5)])
    cacho2 = Cacho([Dado(2), Dado(2), Dado(4), Dado(5), Dado(6)])
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 3
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == ResultadoDuda.PIERDE


# Test: duda sin ases, apuesta exacta
def test_duda_sin_ases_apuesta_exacta():
    cacho1 = Cacho([Dado(2), Dado(2), Dado(3), Dado(4), Dado(5)])
    cacho2 = Cacho([Dado(3), Dado(3), Dado(4), Dado(5), Dado(6)])
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == ResultadoDuda.CALZAR


# Test: duda con apuesta menor y ases presentes
def test_duda_con_ases_apuesta_menor():
    cacho1 = Cacho([Dado(1), Dado(2), Dado(2), Dado(3), Dado(4)])
    cacho2 = Cacho([Dado(2), Dado(3), Dado(3), Dado(4), Dado(5)])
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == ResultadoDuda.PIERDE


def test_duda_con_ases_apuesta_mayor():
    cacho1 = Cacho([Dado(3), Dado(2), Dado(2), Dado(3), Dado(4)])
    cacho2 = Cacho([Dado(4), Dado(3), Dado(3), Dado(4), Dado(5)])
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 3
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == ResultadoDuda.GANA


def test_si_puede_calzar():
    cacho1 = Cacho([Dado(1), Dado(2), Dado(3), Dado(4), Dado(5)])
    cacho2 = Cacho([Dado(2), Dado(3), Dado(4), Dado(5), Dado(6)])
    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 3
    puede_calzar = arbitro.puede_calzar(cantidad_apostada)
    assert puede_calzar == True


def test_no_puede_calzar():
    cacho1 = Cacho([Dado(1), Dado(2), Dado(3), Dado(4), Dado(5)])
    cacho2 = Cacho([Dado(2), Dado(3), Dado(4), Dado(5), Dado(6)])
    cacho1.remover_dado()
    cacho1.remover_dado()
    cacho1.remover_dado()
    cacho2.remover_dado()
    cacho2.remover_dado()
    cacho2.remover_dado()

    contador = ContadorPintas([cacho1, cacho2])
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 9
    puede_calzar = arbitro.puede_calzar(cantidad_apostada)
    assert puede_calzar == False
