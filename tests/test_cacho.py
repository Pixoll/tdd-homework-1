import pytest

from src.juego.cacho import Cacho
from src.juego.dado import Dado


def test_cacho_cantidad_dados_iniciales():
    cacho = Cacho()
    assert cacho.cantidad_dados == 5


def test_cacho_valores_dados_iniciales():
    cacho = Cacho([Dado(1), Dado(2), Dado(3), Dado(4), Dado(5)])
    assert cacho.cantidad_dados == 5
    assert cacho.valores_dados == [1, 2, 3, 4, 5]


def test_cacho_cantidad_invalida_dados_iniciales():
    with pytest.raises(Exception):
        cacho = Cacho([])


def test_cacho_tirar_dados():
    cacho = Cacho()
    cacho.tirar_dados()
    assert cacho.cantidad_dados == 5
    assert all(1 <= valor <= 6 for valor in cacho.valores_dados)


def test_cacho_remover_dados():
    cacho = Cacho()
    cacho.remover_dado()
    assert cacho.cantidad_dados == 4
    cacho.remover_dado()
    assert cacho.cantidad_dados == 3
    cacho.remover_dado()
    assert cacho.cantidad_dados == 2
    cacho.remover_dado()
    assert cacho.cantidad_dados == 1
    cacho.remover_dado()
    assert cacho.cantidad_dados == 0
