from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from src.dado import Dado


def test_tirar_dado() -> None:
    """Verifica que tirar un dado genera un valor entre 1 y 6 y actualiza su valor."""
    dado = Dado()
    valor = dado.tirar()
    assert 1 <= valor <= 6
    assert 1 <= dado.valor <= 6
    assert valor == dado.valor


def test_tirar_dado_pinta(mocker: MockerFixture) -> None:
    """Verifica que cada valor del dado corresponde a la pinta correcta."""
    mock_valores_dado = [1, 2, 3, 4, 5, 6]
    mock_randint = MagicMock(side_effect=mock_valores_dado)
    mocker.patch("src.dado.randint", mock_randint)

    dado = Dado()

    dado.tirar()
    assert dado.valor == 1
    assert dado.pinta == "As"

    dado.tirar()
    assert dado.valor == 2
    assert dado.pinta == "Tonto"

    dado.tirar()
    assert dado.valor == 3
    assert dado.pinta == "Tren"

    dado.tirar()
    assert dado.valor == 4
    assert dado.pinta == "Cuadra"

    dado.tirar()
    assert dado.valor == 5
    assert dado.pinta == "Quina"

    dado.tirar()
    assert dado.valor == 6
    assert dado.pinta == "Sexto"
