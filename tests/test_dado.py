from src.juego.dado import Dado


def test_tirar_dado() -> None:
    dado = Dado()
    value = dado.tirar()
    assert 1 <= value <= 6
