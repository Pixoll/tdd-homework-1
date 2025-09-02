from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.contador_pintas import ContadorPintas
from src.juego.dado import Dado

# Helper para crear dados con valores fijos
def crear_dados(valores):
    return [Dado(valor=v) for v in valores]

# Test: duda correcta (apuesta menor que cantidad real)
def test_duda_correcta_gana_jugador():
    dados = crear_dados([2, 2, 3, 4, 5])
    contador = ContadorPintas(dados)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    # 2 de pinta 2 + 0 As como comodín > 1, jugador que duda pierde
    assert resultado == "jugador_pierde"

# Test: duda exacta (calzar)
def test_duda_correcta_calzar():
    dados = crear_dados([2, 2, 1, 3, 4])
    contador = ContadorPintas(dados)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 3  # 2 de pinta 2 + 1 As como comodín
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == "calzar"

# Test: duda con ases como comodín
def test_duda_con_ases_como_comodin():
    dados = crear_dados([1, 1, 3, 4, 5])
    contador = ContadorPintas(dados)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 3
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    # 1 de pinta 3 + 2 ases (comodín máximo) = 3 > 2, jugador que duda pierde
    assert resultado == "jugador_pierde"

# Test: duda sin ases, apuesta exacta
def test_duda_sin_ases_apuesta_exacta():
    dados = crear_dados([2, 2, 3, 4, 5])
    contador = ContadorPintas(dados)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 2
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    assert resultado == "calzar"

# Test: duda con apuesta menor y ases presentes
def test_duda_con_ases_apuesta_menor():
    dados = crear_dados([1, 2, 2, 3, 4])
    contador = ContadorPintas(dados)
    arbitro = ArbitroRonda(contador)

    cantidad_apostada = 1
    pinta = 2
    resultado = arbitro.dudar(cantidad_apostada, pinta)
    # 2 de pinta 2 + 1 As como comodín = 3 > 1, jugador que duda pierde
    assert resultado == "jugador_pierde"
