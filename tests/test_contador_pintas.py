from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from src.cacho import Cacho
from src.contador_pintas import ContadorPintas


def test_constructor(mocker: MockerFixture) -> None:
    """Verifica que el contador inicializa correctamente con todos los dados."""
    mock_valores_cacho1 = [1, 2, 3, 4, 5]
    mock_valores_cacho2 = [2, 3, 4, 5, 6]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert len(contador.valores_dados) == 10


def test_contar_pinta_sin_ases(mocker: MockerFixture) -> None:
    """Cuenta correctamente los dados de una pinta sin usar ases."""
    mock_valores_cacho1 = [2, 2, 3, 4, 5]
    mock_valores_cacho2 = [3, 3, 4, 5, 6]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(2) == 2


def test_contar_pinta_con_ases_como_comodin(mocker: MockerFixture) -> None:
    """Cuenta correctamente usando ases como comodines."""
    mock_valores_cacho1 = [1, 2, 2, 5, 6]
    mock_valores_cacho2 = [2, 3, 3, 6, 1]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(2) == 5


def test_contar_pinta_con_varios_ases(mocker: MockerFixture) -> None:
    """Cuenta correctamente cuando hay múltiples ases como comodines."""
    mock_valores_cacho1 = [1, 1, 4, 4, 6]
    mock_valores_cacho2 = [2, 2, 5, 5, 1]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(4) == 5


def test_contar_pinta_sin_ases_comodines(mocker: MockerFixture) -> None:
    """Cuenta correctamente una pinta ignorando los ases como comodines."""
    mock_valores_cacho1 = [1, 2, 2, 5, 6]
    mock_valores_cacho2 = [2, 3, 3, 6, 1]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(5, usar_ases=False) == 1


def test_contar_pinta_todos_ases_sin_comodin(mocker: MockerFixture) -> None:
    """Verifica que ninguna pinta se cuenta si todos los dados son ases y no se usan como comodines."""
    mock_valores_cacho1 = [1, 1, 1, 1, 1]
    mock_valores_cacho2 = [2, 2, 2, 2, 2]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(3, usar_ases=False) == 0


def test_todos_dados_misma_pinta_sin_ases(mocker: MockerFixture) -> None:
    """Cuenta correctamente cuando todos los dados son de la misma pinta sin ases."""
    mock_valores_cacho1 = [3, 4, 3, 4, 3]
    mock_valores_cacho2 = [4, 3, 4, 3, 4]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(3) == 5


def test_pinta_no_presente_con_ases_como_comodin(mocker: MockerFixture) -> None:
    """Cuenta correctamente cuando la pinta no está presente pero los ases se usan como comodines."""
    mock_valores_cacho1 = [1, 1, 4, 1, 6]
    mock_valores_cacho2 = [2, 2, 5, 2, 1]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(5) == 5


def test_pinta_no_presente_sin_ases_como_comodin(mocker: MockerFixture) -> None:
    """Cuenta correctamente cuando la pinta no está presente y los ases no se usan como comodines."""
    mock_valores_cacho1 = [1, 1, 4, 1, 6]
    mock_valores_cacho2 = [2, 2, 5, 2, 1]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])
    assert contador.contar_pinta(5, usar_ases=False) == 1


def test_mezcla_varias_pintas_y_ases(mocker: MockerFixture) -> None:
    """Cuenta correctamente varias pintas en un mismo conjunto de cachos mezclados con ases."""
    mock_valores_cacho1 = [1, 2, 3, 1, 4]
    mock_valores_cacho2 = [2, 3, 4, 2, 5]
    mock_randint = MagicMock(side_effect=mock_valores_cacho1 + mock_valores_cacho2)
    mocker.patch("src.dado.randint", mock_randint)

    cacho1 = Cacho()
    cacho2 = Cacho()
    cacho1.tirar_dados()
    cacho2.tirar_dados()
    contador = ContadorPintas([cacho1, cacho2])

    assert contador.contar_pinta(2) == 5
    assert contador.contar_pinta(4) == 4
    assert contador.contar_pinta(5) == 3
