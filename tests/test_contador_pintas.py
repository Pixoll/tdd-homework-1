from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas
from src.juego.dado import Dado


def test_constructor():
    cacho1 = Cacho([Dado(1), Dado(2), Dado(3), Dado(4), Dado(5)])
    cacho2 = Cacho([Dado(2), Dado(3), Dado(4), Dado(5), Dado(6)])
    contador = ContadorPintas([cacho1, cacho2])
    assert len(contador.valores_dados) == 10


def test_contar_pinta_sin_ases():
    cacho1 = Cacho([Dado(2), Dado(2), Dado(3), Dado(4), Dado(5)])
    cacho2 = Cacho([Dado(3), Dado(3), Dado(4), Dado(5), Dado(6)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(2) == 2


def test_contar_pinta_con_ases_como_comodin():
    cacho1 = Cacho([Dado(1), Dado(2), Dado(2), Dado(5), Dado(6)])
    cacho2 = Cacho([Dado(2), Dado(3), Dado(3), Dado(6), Dado(1)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(2) == 5


def test_contar_pinta_con_varios_ases():
    cacho1 = Cacho([Dado(1), Dado(1), Dado(4), Dado(4), Dado(6)])
    cacho2 = Cacho([Dado(2), Dado(2), Dado(5), Dado(5), Dado(1)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(4) == 5


def test_contar_pinta_sin_ases_comodines():
    cacho1 = Cacho([Dado(1), Dado(2), Dado(2), Dado(5), Dado(6)])
    cacho2 = Cacho([Dado(2), Dado(3), Dado(3), Dado(6), Dado(1)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(5, usar_ases=False) == 1


def test_contar_pinta_todos_ases_sin_comodin():
    cacho1 = Cacho([Dado(1), Dado(1), Dado(1), Dado(1), Dado(1)])
    cacho2 = Cacho([Dado(2), Dado(2), Dado(2), Dado(2), Dado(2)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(3, usar_ases=False) == 0


def test_todos_dados_misma_pinta_sin_ases():
    cacho1 = Cacho([Dado(3), Dado(4), Dado(3), Dado(4), Dado(3)])
    cacho2 = Cacho([Dado(4), Dado(3), Dado(4), Dado(3), Dado(4)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(3) == 5


def test_pinta_no_presente_con_ases_como_comodin():
    cacho1 = Cacho([Dado(1), Dado(1), Dado(4), Dado(1), Dado(6)])
    cacho2 = Cacho([Dado(2), Dado(2), Dado(5), Dado(2), Dado(1)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(5) == 5


def test_pinta_no_presente_sin_ases_como_comodin():
    cacho1 = Cacho([Dado(1), Dado(1), Dado(4), Dado(1), Dado(6)])
    cacho2 = Cacho([Dado(2), Dado(2), Dado(5), Dado(2), Dado(1)])
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(5, usar_ases=False) == 1


def test_mezcla_varias_pintas_y_ases():
    cacho1 = Cacho([Dado(1), Dado(2), Dado(3), Dado(1), Dado(4)])
    cacho2 = Cacho([Dado(2), Dado(3), Dado(4), Dado(2), Dado(5)])
    contador = ContadorPintas([cacho1, cacho2])

    assert contador.contar_pinta(2) == 5
    assert contador.contar_pinta(4) == 4
    assert contador.contar_pinta(5) == 3
