from src.juego.contador_pintas import ContadorPintas
from src.juego.dado import Dado

def test_constructor():
    dados = [Dado(1), Dado(2), Dado(3), Dado(4), Dado(5)]
    contador = ContadorPintas(dados)
    assert len(contador.dados) == 5


def test_contar_pinta_sin_ases():
    dados = [Dado(2), Dado(2), Dado(3), Dado(4), Dado(5)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(2) == 2


def test_contar_pinta_con_ases_como_comodin():
    dados = [Dado(1), Dado(2), Dado(2), Dado(5), Dado(6)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(2) == 3  # dos doses + un as


def test_contar_pinta_con_varios_ases():
    dados = [Dado(1), Dado(1), Dado(4), Dado(4), Dado(6)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(4) == 4  # dos cuatros + dos ases


def test_contar_pinta_sin_ases_comodines():
    dados = [Dado(1), Dado(2), Dado(2), Dado(5), Dado(6)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(5, usar_ases=False) == 1  # solo un 5


def test_contar_pinta_todos_ases_sin_comodin():
    dados = [Dado(1), Dado(1), Dado(1), Dado(1), Dado(1)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(3, usar_ases=False) == 0  # no hay treses

def test_todos_dados_misma_pinta_sin_ases():
    dados = [Dado(3), Dado(3), Dado(3), Dado(3), Dado(3)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(3) == 5  # todos son tres, sin ases


def test_pinta_no_presente_con_ases_como_comodin():
    dados = [Dado(1), Dado(1), Dado(4), Dado(1), Dado(6)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(5) == 2  # ningún 5, pero dos ases cuentan como comodín


def test_pinta_no_presente_sin_ases_como_comodin():
    dados = [Dado(1), Dado(1), Dado(4), Dado(1), Dado(6)]
    contador = ContadorPintas(dados)
    assert contador.contar_pinta(5, usar_ases=False) == 0  # ningún 5 y ases no cuentan


def test_mezcla_varias_pintas_y_ases():
    dados = [Dado(1), Dado(2), Dado(3), Dado(1), Dado(4)]
    contador = ContadorPintas(dados)

    # contar 2 usando ases
    assert contador.contar_pinta(2) == 2  # un 2 + un as

    # contar 4 usando ases
    assert contador.contar_pinta(4) == 2  # un 4 + un as

    # contar 5 usando ases
    assert contador.contar_pinta(5) == 2  # ningún 5, pero dos ases suman
