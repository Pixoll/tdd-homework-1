from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from src.juego.cacho import Cacho
from src.juego.dado import Dado


def test_cacho_cantidad_dados_iniciales() -> None:
    cacho = Cacho()
    assert cacho.cantidad_dados == 5


def test_cacho_tirar_dados() -> None:
    cacho = Cacho()
    cacho.tirar_dados()
    assert cacho.cantidad_dados == 5
    assert all(1 <= valor <= 6 for valor in cacho.valores_dados)


def test_cacho_tirar_dados_mock(mocker: MockerFixture) -> None:
    mock_valores_cacho = [1, 2, 3, 4, 5]
    mock_randint = MagicMock(side_effect=mock_valores_cacho)
    mocker.patch("src.juego.dado.randint", mock_randint)

    cacho = Cacho()
    cacho.tirar_dados()
    assert cacho.cantidad_dados == 5
    assert cacho.valores_dados == [1, 2, 3, 4, 5]


def test_cacho_remover_dados() -> None:
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


def test_cacho_agregar_dados() -> None:
    cacho = Cacho()
    cacho.agregar_dado(Dado())
    assert cacho.cantidad_dados == 6


def test_cacho_agregar_y_remover_dados() -> None:
    cacho = Cacho()
    cacho.remover_dado()
    assert cacho.cantidad_dados == 4
    cacho.agregar_dado(Dado())
    assert cacho.cantidad_dados == 5
    cacho.agregar_dado(Dado())
    assert cacho.cantidad_dados == 6
    cacho.remover_dado()
    assert cacho.cantidad_dados == 5
