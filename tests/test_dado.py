from src.juego.dado import Dado


def test_tirar_dado() -> None:
    dado = Dado()
    valor = dado.tirar()
    assert 1 <= valor <= 6
    assert 1 <= dado.valor <= 6
    assert valor == dado.valor
